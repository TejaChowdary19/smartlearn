"""
Fine-tuning pipeline for SmartLearn AI models.
This module handles data collection, preparation, training, and evaluation.
"""

import json
import os
import pickle
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    TrainingArguments, Trainer,
    DataCollatorForLanguageModeling
)
import evaluate

@dataclass
class TrainingExample:
    """Represents a single training example."""
    input_text: str
    target_text: str
    subject: str
    difficulty: str
    user_rating: Optional[float] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class TrainingMetrics:
    """Training and evaluation metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    loss: float
    perplexity: float
    training_time: float
    timestamp: str

class SmartLearnDataset(Dataset):
    """Custom dataset for SmartLearn training data."""
    
    def __init__(self, examples: List[TrainingExample], tokenizer, max_length: int = 512):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        
        # Combine input and target
        full_text = f"Input: {example.input_text}\nOutput: {example.target_text}"
        
        # Tokenize
        encoding = self.tokenizer(
            full_text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": encoding["input_ids"].squeeze()
        }

class DataCollector:
    """Collects and manages training data from user interactions."""
    
    def __init__(self, data_dir: str = "data/training"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.examples: List[TrainingExample] = []
        self.load_existing_data()
    
    def add_example(self, example: TrainingExample):
        """Add a new training example."""
        self.examples.append(example)
        self.save_data()
    
    def add_batch_examples(self, examples: List[TrainingExample]):
        """Add multiple training examples at once."""
        self.examples.extend(examples)
        self.save_data()
    
    def load_existing_data(self):
        """Load existing training data from disk."""
        data_file = os.path.join(self.data_dir, "training_data.json")
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.examples = [TrainingExample(**ex) for ex in data]
                print(f"✅ Loaded {len(self.examples)} existing training examples")
            except Exception as e:
                print(f"❌ Error loading training data: {e}")
                self.examples = []
    
    def save_data(self):
        """Save training data to disk."""
        data_file = os.path.join(self.data_dir, "training_data.json")
        try:
            with open(data_file, 'w') as f:
                json.dump([asdict(ex) for ex in self.examples], f, indent=2)
        except Exception as e:
            print(f"❌ Error saving training data: {e}")
    
    def get_subject_data(self, subject: str) -> List[TrainingExample]:
        """Get training examples for a specific subject."""
        return [ex for ex in self.examples if ex.subject.lower() == subject.lower()]
    
    def get_difficulty_data(self, difficulty: str) -> List[TrainingExample]:
        """Get training examples for a specific difficulty level."""
        return [ex for ex in self.examples if ex.difficulty.lower() == difficulty.lower()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the training data."""
        if not self.examples:
            return {"total_examples": 0}
        
        subjects = {}
        difficulties = {}
        ratings = []
        
        for ex in self.examples:
            subjects[ex.subject] = subjects.get(ex.subject, 0) + 1
            difficulties[ex.difficulty] = difficulties.get(ex.difficulty, 0) + 1
            if ex.user_rating:
                ratings.append(ex.user_rating)
        
        return {
            "total_examples": len(self.examples),
            "subjects": subjects,
            "difficulties": difficulties,
            "avg_rating": np.mean(ratings) if ratings else 0,
            "total_ratings": len(ratings)
        }

class DataPreprocessor:
    """Preprocesses training data for fine-tuning."""
    
    def __init__(self, tokenizer, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def preprocess_examples(self, examples: List[TrainingExample]) -> Tuple[List, List]:
        """Preprocess examples into input and target sequences."""
        inputs = []
        targets = []
        
        for example in examples:
            # Format input
            input_text = f"Subject: {example.subject}\nDifficulty: {example.difficulty}\nQuery: {example.input_text}"
            inputs.append(input_text)
            
            # Format target
            target_text = example.target_text
            targets.append(target_text)
        
        return inputs, targets
    
    def create_training_data(self, examples: List[TrainingExample]) -> SmartLearnDataset:
        """Create training dataset from examples."""
        return SmartLearnDataset(examples, self.tokenizer, self.max_length)
    
    def split_data(self, examples: List[TrainingExample], 
                   train_ratio: float = 0.8, val_ratio: float = 0.1) -> Tuple[List, List, List]:
        """Split data into train/validation/test sets."""
        total = len(examples)
        train_size = int(total * train_ratio)
        val_size = int(total * val_ratio)
        
        # Shuffle examples
        np.random.shuffle(examples)
        
        train_examples = examples[:train_size]
        val_examples = examples[train_size:train_size + val_size]
        test_examples = examples[train_size + val_size:]
        
        return train_examples, val_examples, test_examples

class FineTuner:
    """Handles the fine-tuning process."""
    
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium", 
                 output_dir: str = "models/fine_tuned"):
        self.base_model = base_model
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.tokenizer = None
        self.model = None
        self.trainer = None
        
        self.load_model()
    
    def load_model(self):
        """Load the base model and tokenizer."""
        try:
            print(f"🔄 Loading base model: {self.base_model}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
            self.model = AutoModelForCausalLM.from_pretrained(self.base_model)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def prepare_training_data(self, examples: List[TrainingExample]) -> Tuple[SmartLearnDataset, SmartLearnDataset]:
        """Prepare training and validation datasets."""
        preprocessor = DataPreprocessor(self.tokenizer)
        train_examples, val_examples, _ = preprocessor.split_data(examples)
        
        train_dataset = preprocessor.create_training_data(train_examples)
        val_dataset = preprocessor.create_training_data(val_examples)
        
        return train_dataset, val_dataset
    
    def setup_training(self, train_dataset: SmartLearnDataset, val_dataset: SmartLearnDataset):
        """Setup training configuration."""
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=1,  # Reduced for memory
            per_device_train_batch_size=1,  # Minimal batch size
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=8,  # Add gradient accumulation
            warmup_steps=50,
            weight_decay=0.01,
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=50,
            eval_strategy="steps",
            eval_steps=200,
            save_steps=200,  # Must be multiple of eval_steps
            save_total_limit=1,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            dataloader_pin_memory=False,  # Disable for M3
            dataloader_num_workers=0,     # Single worker
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
        )
    
    def train(self, examples: List[TrainingExample]) -> TrainingMetrics:
        """Execute the fine-tuning process."""
        if not examples:
            raise ValueError("No training examples provided")
        
        print(f"🚀 Starting fine-tuning with {len(examples)} examples")
        start_time = datetime.now()
        
        # Prepare data
        train_dataset, val_dataset = self.prepare_training_data(examples)
        self.setup_training(train_dataset, val_dataset)
        
        # Train
        print("🔄 Training in progress...")
        train_result = self.trainer.train()
        
        # Evaluate
        print("🔍 Evaluating model...")
        eval_result = self.trainer.evaluate()
        
        # Calculate metrics
        end_time = datetime.now()
        training_time = (end_time - start_time).total_seconds()
        
        metrics = TrainingMetrics(
            accuracy=eval_result.get("eval_loss", 0),  # Simplified for now
            precision=0.0,  # Would need classification labels for proper calculation
            recall=0.0,
            f1_score=0.0,
            loss=eval_result.get("eval_loss", 0),
            perplexity=np.exp(eval_result.get("eval_loss", 0)),
            training_time=training_time,
            timestamp=datetime.now().isoformat()
        )
        
        # Save model
        self.save_model()
        
        print(f"✅ Fine-tuning completed in {training_time:.2f} seconds")
        return metrics
    
    def save_model(self):
        """Save the fine-tuned model."""
        try:
            model_path = os.path.join(self.output_dir, "final_model")
            self.trainer.save_model(model_path)
            self.tokenizer.save_pretrained(model_path)
            print(f"✅ Model saved to {model_path}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")
    
    def load_fine_tuned_model(self, model_path: str):
        """Load a fine-tuned model."""
        try:
            full_path = os.path.join(self.output_dir, model_path)
            self.model = AutoModelForCausalLM.from_pretrained(full_path)
            self.tokenizer = AutoTokenizer.from_pretrained(full_path)
            print(f"✅ Fine-tuned model loaded from {full_path}")
        except Exception as e:
            print(f"❌ Error loading fine-tuned model: {e}")

class ModelEvaluator:
    """Evaluates fine-tuned model performance."""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def evaluate_examples(self, test_examples: List[TrainingExample]) -> Dict[str, float]:
        """Evaluate model on test examples."""
        if not test_examples:
            return {}
        
        predictions = []
        targets = []
        
        for example in test_examples:
            # Generate prediction
            input_text = f"Subject: {example.subject}\nDifficulty: {example.difficulty}\nQuery: {example.input_text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=512,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            predictions.append(prediction)
            targets.append(example.target_text)
        
        # Calculate metrics (simplified for now)
        # In a real implementation, you'd use proper evaluation metrics
        metrics = {
            "num_examples": len(test_examples),
            "avg_prediction_length": np.mean([len(p) for p in predictions]),
            "avg_target_length": np.mean([len(t) for t in targets])
        }
        
        return metrics

class FineTuningPipeline:
    """Complete fine-tuning pipeline for SmartLearn."""
    
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium"):
        self.data_collector = DataCollector()
        self.fine_tuner = FineTuner(base_model)
        self.evaluator = None
    
    def collect_user_data(self, user_interactions: List[Dict[str, Any]]):
        """Collect training data from user interactions."""
        examples = []
        
        for interaction in user_interactions:
            example = TrainingExample(
                input_text=interaction.get("query", ""),
                target_text=interaction.get("response", ""),
                subject=interaction.get("subject", "general"),
                difficulty=interaction.get("difficulty", "medium"),
                user_rating=interaction.get("rating"),
                timestamp=datetime.now().isoformat(),
                metadata=interaction.get("metadata", {})
            )
            examples.append(example)
        
        self.data_collector.add_batch_examples(examples)
        print(f"✅ Collected {len(examples)} training examples")
    
    def run_fine_tuning(self) -> TrainingMetrics:
        """Run the complete fine-tuning pipeline."""
        examples = self.data_collector.examples
        
        if len(examples) < 10:
            raise ValueError(f"Need at least 10 training examples, got {len(examples)}")
        
        print(f"🚀 Starting fine-tuning pipeline with {len(examples)} examples")
        
        # Run fine-tuning
        metrics = self.fine_tuner.train(examples)
        
        # Setup evaluator
        self.evaluator = ModelEvaluator(self.fine_tuner.model, self.fine_tuner.tokenizer)
        
        return metrics
    
    def evaluate_model(self) -> Dict[str, float]:
        """Evaluate the fine-tuned model."""
        if not self.evaluator:
            raise ValueError("Model not fine-tuned yet")
        
        # Get test examples
        _, _, test_examples = DataPreprocessor(self.fine_tuner.tokenizer).split_data(
            self.data_collector.examples
        )
        
        return self.evaluator.evaluate_examples(test_examples)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current status of the fine-tuning pipeline."""
        data_stats = self.data_collector.get_statistics()
        
        return {
            "data_collection": data_stats,
            "model_status": "fine_tuned" if self.evaluator else "not_fine_tuned",
            "base_model": self.fine_tuner.base_model,
            "output_directory": self.fine_tuner.output_dir
        }

# Utility functions for data generation
def generate_synthetic_data(subject: str, num_examples: int = 50) -> List[TrainingExample]:
    """Generate synthetic training data for testing purposes."""
    examples = []
    
    # Template-based generation
    templates = {
        "mathematics": [
            ("Explain the concept of {topic}", "Here's a comprehensive explanation of {topic}..."),
            ("How do I solve {problem_type} problems?", "To solve {problem_type} problems, follow these steps..."),
            ("What is the difference between {concept1} and {concept2}?", "The key differences between {concept1} and {concept2} are...")
        ],
        "computer_science": [
            ("How do I implement {algorithm}?", "Here's how to implement {algorithm}..."),
            ("Explain {concept} in programming", "In programming, {concept} refers to..."),
            ("What are the best practices for {topic}?", "Best practices for {topic} include...")
        ]
    }
    
    subject_templates = templates.get(subject.lower(), templates["mathematics"])
    
    for i in range(num_examples):
        template = subject_templates[i % len(subject_templates)]
        example = TrainingExample(
            input_text=template[0].format(
                topic=f"topic_{i}",
                problem_type=f"problem_type_{i}",
                concept1=f"concept_{i}",
                concept2=f"concept_{i+1}",
                algorithm=f"algorithm_{i}",
                concept=f"concept_{i}"
            ),
            target_text=template[1].format(
                topic=f"topic_{i}",
                problem_type=f"problem_type_{i}",
                concept1=f"concept_{i}",
                concept2=f"concept_{i+1}",
                algorithm=f"algorithm_{i}",
                concept=f"concept_{i}"
            ),
            subject=subject,
            difficulty=["easy", "medium", "hard"][i % 3],
            user_rating=np.random.uniform(3.5, 5.0),
            timestamp=datetime.now().isoformat()
        )
        examples.append(example)
    
    return examples
