#!/usr/bin/env python3
"""
Fine-tuning Execution Script for SmartLearn
This script will actually run the fine-tuning process using your collected training data.
"""

import sys
import os
sys.path.append('src')

from src.core.advanced_features import SmartLearnAdvanced
from src.core.fine_tuning import FineTuningPipeline, TrainingExample
import json

def main():
    print("🚀 Starting SmartLearn Fine-Tuning Process...")
    
    # Initialize advanced features
    print("📚 Initializing SmartLearn Advanced Features...")
    advanced = SmartLearnAdvanced()
    
    # Check current status
    print("\n📊 Current System Status:")
    status = advanced.get_system_status()
    print(f"   - RAG System: {status['rag_system']}")
    print(f"   - Fine-tuning: {status['fine_tuning']}")
    print(f"   - Multimodal: {status['multimodal']}")
    
    # Check training data
    print("\n📈 Training Data Status:")
    training_data = advanced.fine_tuning_pipeline.data_collector.examples
    print(f"   - Total Examples: {len(training_data)}")
    
    if len(training_data) < 10:
        print("❌ Need at least 10 training examples to start fine-tuning")
        return
    
    # Display sample training examples
    print("\n🔍 Sample Training Examples:")
    for i, example in enumerate(training_data[:3]):
        print(f"   Example {i+1}:")
        print(f"     Input: {example.input_text[:100]}...")
        print(f"     Target: {example.target_text[:100]}...")
        print(f"     Subject: {example.subject}, Difficulty: {example.difficulty}")
        print()
    
    # Start fine-tuning
    print("🎯 Starting Fine-Tuning Process...")
    print("   This may take several hours depending on your data size and hardware.")
    print("   The model will be saved to 'models/fine_tuned/' directory.")
    
    try:
        # Run fine-tuning
        metrics = advanced.run_fine_tuning()
        
        if metrics:
            print("\n✅ Fine-Tuning Completed Successfully!")
            print("\n📊 Training Results:")
            print(f"   - Training Time: {metrics.training_time:.2f} seconds")
            print(f"   - Final Loss: {metrics.loss:.4f}")
            print(f"   - Perplexity: {metrics.perplexity:.4f}")
            print(f"   - Accuracy: {metrics.accuracy:.4f}")
            print(f"   - Precision: {metrics.precision:.4f}")
            print(f"   - Recall: {metrics.recall:.4f}")
            print(f"   - F1 Score: {metrics.f1_score:.4f}")
            
            # Evaluate the fine-tuned model
            print("\n🔍 Evaluating Fine-Tuned Model...")
            eval_metrics = advanced.evaluate_fine_tuned_model()
            
            if eval_metrics:
                print("\n📈 Evaluation Results:")
                for key, value in eval_metrics.items():
                    print(f"   - {key}: {value}")
            
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
        print("   Check the error details above and ensure you have sufficient resources.")
        print("   Fine-tuning requires significant computational resources and time.")

if __name__ == "__main__":
    main()
