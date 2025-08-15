#!/usr/bin/env python3
"""
Memory-Efficient Fine-tuning Script for SmartLearn
Optimized for Apple M3 with limited GPU memory
"""

import sys
import os
sys.path.append('src')

from src.core.fine_tuning import FineTuningPipeline, TrainingExample
import torch
import gc

def main():
    print("🚀 Starting Memory-Efficient SmartLearn Fine-Tuning...")
    
    # Set memory-efficient PyTorch settings for M3
    os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.8'
    os.environ['PYTORCH_MPS_LOW_WATERMARK_RATIO'] = '0.6'
    
    print("🔧 Optimizing for Apple M3 GPU memory...")
    
    # Initialize fine-tuning pipeline
    print("📚 Initializing Fine-Tuning Pipeline...")
    pipeline = FineTuningPipeline(base_model="microsoft/DialoGPT-medium")
    
    # Check training data
    training_data = pipeline.data_collector.examples
    print(f"📈 Training Data: {len(training_data)} examples")
    
    if len(training_data) < 10:
        print("❌ Need at least 10 training examples")
        return
    
    # Create memory-efficient training configuration
    print("⚙️ Creating memory-efficient training configuration...")
    
    # Modify the fine-tuner for memory efficiency
    fine_tuner = pipeline.fine_tuner
    
    # Use smaller batch sizes and gradient accumulation
    training_args = type('TrainingArgs', (), {
        'output_dir': fine_tuner.output_dir,
        'num_train_epochs': 1,  # Reduce epochs for memory
        'per_device_train_batch_size': 1,  # Minimal batch size
        'per_device_eval_batch_size': 1,
        'gradient_accumulation_steps': 8,  # Accumulate gradients
                'warmup_steps': 50,
        'weight_decay': 0.01,
        'logging_dir': f"{fine_tuner.output_dir}/logs",
        'logging_steps': 50,
        'eval_strategy': "steps",
        'eval_steps': 200,
        'save_steps': 200,
        'save_total_limit': 1,
        'load_best_model_at_end': True,
        'metric_for_best_model': "eval_loss",
        'greater_is_better': False,
        'dataloader_pin_memory': False,  # Disable for M3
        'dataloader_num_workers': 0,     # Single worker
    })()
    
    # Override the setup_training method
    def setup_training_memory_efficient(self, train_dataset, val_dataset):
        """Memory-efficient training setup."""
        from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
        
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=1,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=8,
            warmup_steps=50,
            weight_decay=0.01,
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=50,
            eval_strategy="steps",
            eval_steps=200,
            save_steps=500,
            save_total_limit=1,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            dataloader_pin_memory=False,
            dataloader_num_workers=0,
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
    
    # Replace the method
    fine_tuner.setup_training = setup_training_memory_efficient.__get__(fine_tuner)
    
    try:
        print("🎯 Starting Memory-Efficient Fine-Tuning...")
        print("   - Batch Size: 1 (with gradient accumulation)")
        print("   - Epochs: 1 (to fit in memory)")
        print("   - Gradient Accumulation: 8 steps")
        
        # Run fine-tuning
        metrics = pipeline.run_fine_tuning()
        
        if metrics:
            print("\n✅ Fine-Tuning Completed Successfully!")
            print("\n📊 Training Results:")
            print(f"   - Training Time: {metrics.training_time:.2f} seconds")
            print(f"   - Final Loss: {metrics.loss:.4f}")
            print(f"   - Perplexity: {metrics.perplexity:.4f}")
            
            # Check if model was saved
            model_path = "models/fine_tuned/final_model"
            if os.path.exists(model_path):
                print(f"\n💾 Fine-tuned model saved to: {model_path}")
                print("   You can now use this model for improved responses!")
            else:
                print("\n⚠️ Model may not have been saved properly")
                
        else:
            print("❌ Fine-tuning failed to return metrics")
            
    except Exception as e:
        print(f"\n❌ Fine-tuning failed with error: {e}")
        print("\n💡 Memory Optimization Tips:")
        print("   - Try reducing gradient_accumulation_steps")
        print("   - Use even smaller batch sizes")
        print("   - Consider using CPU training if GPU memory is insufficient")
        
        # Clean up GPU memory
        if torch.mps.is_available():
            torch.mps.empty_cache()
        gc.collect()

if __name__ == "__main__":
    main()
