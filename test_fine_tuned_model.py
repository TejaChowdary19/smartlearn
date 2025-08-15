#!/usr/bin/env python3
"""
Test Script for Fine-Tuned SmartLearn Model
Compare base model vs. fine-tuned model performance
"""

import sys
import os
sys.path.append('src')

from src.core.generator import LLM
from src.core.fine_tuning import FineTuningPipeline
import torch

def test_models():
    print("🧪 Testing Fine-Tuned vs. Base Model Performance")
    print("=" * 60)
    
    # Test questions
    test_questions = [
        "Explain derivatives in calculus",
        "How do I solve quadratic equations?",
        "What is the difference between a function and a relation?",
        "Explain the concept of limits in mathematics",
        "How do I implement a binary search algorithm?"
    ]
    
    print("\n📚 Test Questions:")
    for i, question in enumerate(test_questions, 1):
        print(f"   {i}. {question}")
    
    print("\n" + "=" * 60)
    
    # Test base model
    print("\n🔵 Testing Base Model (microsoft/DialoGPT-medium)...")
    try:
        base_llm = LLM(provider="ollama", model="microsoft/DialoGPT-medium")
        
        for i, question in enumerate(test_questions[:2], 1):  # Test first 2 questions
            print(f"\n   Question {i}: {question}")
            print("   Base Model Response:")
            
            try:
                response = base_llm.complete(question, temperature=0.7, max_tokens=200)
                print(f"   {response[:200]}...")
            except Exception as e:
                print(f"   Error: {e}")
                
    except Exception as e:
        print(f"   Base model error: {e}")
    
    print("\n" + "=" * 60)
    
    # Test fine-tuned model
    print("\n🟢 Testing Fine-Tuned Model...")
    try:
        # Check if fine-tuned model exists
        model_path = "models/fine_tuned/final_model"
        if os.path.exists(model_path):
            print(f"   ✅ Fine-tuned model found at: {model_path}")
            
            # Load fine-tuned model
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            print("   🔄 Loading fine-tuned model...")
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(model_path)
            
            print("   ✅ Fine-tuned model loaded successfully!")
            
            # Test fine-tuned model
            for i, question in enumerate(test_questions[:2], 1):
                print(f"\n   Question {i}: {question}")
                print("   Fine-Tuned Model Response:")
                
                try:
                    # Prepare input
                    inputs = tokenizer(question, return_tensors="pt", truncation=True, max_length=512)
                    
                    # Generate response
                    with torch.no_grad():
                        outputs = model.generate(
                            **inputs,
                            max_length=512,
                            num_return_sequences=1,
                            temperature=0.7,
                            do_sample=True,
                            pad_token_id=tokenizer.eos_token_id
                        )
                    
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    print(f"   {response[:200]}...")
                    
                except Exception as e:
                    print(f"   Error: {e}")
                    
        else:
            print("   ❌ Fine-tuned model not found!")
            
    except Exception as e:
        print(f"   Fine-tuned model error: {e}")
    
    print("\n" + "=" * 60)
    
    # Performance comparison
    print("\n📊 Performance Summary:")
    print("   Base Model: microsoft/DialoGPT-medium")
    print("   Fine-Tuned Model: Custom SmartLearn model")
    print("   Training Data: 1,576 examples")
    print("   Training Time: 27 minutes 40 seconds")
    print("   Final Loss: 0.1957")
    print("   Perplexity: 1.2161")
    
    print("\n🎯 Next Steps:")
    print("   1. ✅ Fine-tuning completed successfully")
    print("   2. 🔍 Test model performance (above)")
    print("   3. 🌐 Integrate with your Streamlit app")
    print("   4. 📈 Monitor real-world performance")
    print("   5. 🔄 Iterate and improve")

if __name__ == "__main__":
    test_models()
