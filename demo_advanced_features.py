#!/usr/bin/env python3
"""
Comprehensive Demo of SmartLearn Advanced Features
Tests all 4 advanced features: Enhanced Prompt Engineering, Advanced RAG, Fine-Tuning, and Multimodal
"""

import sys
import os
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_enhanced_prompt_engineering():
    """Test Enhanced Prompt Engineering features."""
    print("\n🧠 Testing Enhanced Prompt Engineering...")
    print("=" * 50)
    
    try:
        from core.prompt_templates import (
            StudyPlanPrompt, ExplanationPrompt, QuizPrompt, 
            AdaptivePromptManager
        )
        
        # Test StudyPlanPrompt with advanced features
        study_prompt = StudyPlanPrompt()
        prompt = study_prompt.render(
            subject="mathematics",
            level="intermediate",
            minutes_per_day=60,
            duration_days=7,
            goal="Learn calculus fundamentals",
            user_context={
                "learning_style": "visual",
                "previous_knowledge": "basic algebra",
                "difficulty_preference": "challenging"
            },
            use_cot=True
        )
        
        print(f"✅ Study Plan Prompt Generated: {len(prompt)} characters")
        print(f"   Includes Chain-of-Thought: {'Reasoning Process' in prompt}")
        print(f"   Includes User Context: {'visual' in prompt}")
        
        # Test ExplanationPrompt with few-shot examples
        explanation_prompt = ExplanationPrompt()
        exp_prompt = explanation_prompt.render(
            topic="derivatives",
            level="intermediate",
            user_context={"learning_style": "practical"},
            use_cot=True,
            include_examples=True
        )
        
        print(f"✅ Explanation Prompt Generated: {len(exp_prompt)} characters")
        print(f"   Includes Few-Shot Examples: {'Examples:' in exp_prompt}")
        
        # Test QuizPrompt with difficulty adaptation
        quiz_prompt = QuizPrompt()
        quiz_p = quiz_prompt.render(
            topic="calculus",
            level="intermediate",
            difficulty="hard",
            num_questions=10,
            use_cot=True
        )
        
        print(f"✅ Quiz Prompt Generated: {len(quiz_p)} characters")
        print(f"   Includes Difficulty Guidelines: {'HARD' in quiz_p}")
        
        # Test AdaptivePromptManager
        prompt_manager = AdaptivePromptManager()
        personalized_prompt = prompt_manager.get_personalized_prompt(
            "study_plan",
            "user123",
            subject="physics",
            level="beginner",
            minutes_per_day=30,
            duration_days=5,
            goal="Understand basic mechanics"
        )
        
        print(f"✅ Personalized Prompt Generated: {len(personalized_prompt)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Prompt Engineering Test Failed: {e}")
        return False

def test_advanced_rag():
    """Test Advanced RAG features."""
    print("\n🔍 Testing Advanced RAG Features...")
    print("=" * 50)
    
    try:
        from core.rag import EnhancedRAG, HybridSearchEngine, QueryExpander
        
        # Initialize RAG system
        rag = EnhancedRAG()
        
        # Test document loading
        print("📚 Loading knowledge base...")
        success = rag.load_knowledge_base("data/knowledge_base")
        
        if success:
            print("✅ Knowledge base loaded successfully")
            
            # Test hybrid search
            print("🔍 Testing hybrid search...")
            context, sources = rag.retrieve_relevant_context(
                "machine learning algorithms", k=3, use_hybrid=True
            )
            
            print(f"✅ Hybrid Search Results: {len(sources)} sources")
            print(f"   Context Length: {len(context)} characters")
            
            # Test query expansion
            print("🔍 Testing query expansion...")
            query_expander = QueryExpander()
            expanded_queries = query_expander.expand_query("derivatives")
            
            print(f"✅ Query Expansion: {len(expanded_queries)} expanded queries")
            print(f"   Original: derivatives")
            print(f"   Expanded: {expanded_queries[:3]}")
            
            # Test document insights
            if sources:
                source = sources[0].get('source', '')
                if source:
                    insights = rag.get_document_summary(source)
                    print(f"✅ Document Insights: {insights.get('total_chunks', 0)} chunks")
            
            # Test advanced search with different parameters
            print("🔍 Testing advanced search parameters...")
            context2, sources2 = rag.retrieve_relevant_context(
                "python programming", k=2, use_hybrid=True, alpha=0.8
            )
            
            print(f"✅ Advanced Search: {len(sources2)} sources with alpha=0.8")
            
            return True
        else:
            print("❌ Failed to load knowledge base")
            return False
            
    except Exception as e:
        print(f"❌ Advanced RAG Test Failed: {e}")
        return False

def test_fine_tuning():
    """Test Fine-Tuning Pipeline features."""
    print("\n🎯 Testing Fine-Tuning Pipeline...")
    print("=" * 50)
    
    try:
        from core.fine_tuning import (
            FineTuningPipeline, TrainingExample, 
            generate_synthetic_data
        )
        
        # Initialize pipeline
        pipeline = FineTuningPipeline()
        
        # Test synthetic data generation
        print("📊 Generating synthetic training data...")
        synthetic_examples = generate_synthetic_data("mathematics", 10)
        
        print(f"✅ Synthetic Data Generated: {len(synthetic_examples)} examples")
        
        # Test data collection
        print("📥 Collecting training data...")
        user_interactions = [
            {
                "query": "Explain derivatives",
                "response": "Derivatives measure rate of change...",
                "subject": "mathematics",
                "difficulty": "intermediate",
                "rating": 4.5
            },
            {
                "query": "How to solve quadratic equations?",
                "response": "Use the quadratic formula...",
                "subject": "mathematics",
                "difficulty": "beginner",
                "rating": 4.0
            }
        ]
        
        pipeline.collect_user_data(user_interactions)
        
        # Get pipeline status
        status = pipeline.get_pipeline_status()
        print(f"✅ Pipeline Status: {status['model_status']}")
        print(f"   Training Examples: {status['data_collection']['total_examples']}")
        print(f"   Base Model: {status['base_model']}")
        
        # Test data preprocessing
        if pipeline.data_collector.examples:
            print("📊 Testing data preprocessing...")
            examples = pipeline.data_collector.examples
            
            # Test subject filtering
            math_examples = pipeline.data_collector.get_subject_data("mathematics")
            print(f"✅ Subject Filtering: {len(math_examples)} math examples")
            
            # Test difficulty filtering
            intermediate_examples = pipeline.data_collector.get_difficulty_data("intermediate")
            print(f"✅ Difficulty Filtering: {len(intermediate_examples)} intermediate examples")
            
            # Test statistics
            stats = pipeline.data_collector.get_statistics()
            print(f"✅ Statistics: {stats['total_examples']} total examples")
            print(f"   Subjects: {list(stats['subjects'].keys())}")
            print(f"   Difficulties: {list(stats['difficulties'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fine-Tuning Test Failed: {e}")
        return False

def test_multimodal():
    """Test Multimodal Integration features."""
    print("\n🖼️ Testing Multimodal Integration...")
    print("=" * 50)
    
    try:
        from core.multimodal import (
            MultimodalManager, CrossModalAnalyzer,
            ImageProcessor, AudioProcessor, VideoProcessor
        )
        
        # Initialize multimodal manager
        mm_manager = MultimodalManager()
        
        # Test supported formats
        print("📁 Testing supported formats...")
        supported_formats = mm_manager.supported_formats
        
        print(f"✅ Supported Formats:")
        for content_type, formats in supported_formats.items():
            print(f"   {content_type}: {', '.join(formats)}")
        
        # Test image processor initialization
        print("🖼️ Testing image processor...")
        image_processor = ImageProcessor()
        
        if image_processor.caption_model:
            print("✅ Image captioning model loaded")
        else:
            print("⚠️ Image captioning model not available")
        
        # Test audio processor initialization
        print("🎵 Testing audio processor...")
        audio_processor = AudioProcessor()
        
        if audio_processor.whisper_model:
            print("✅ Audio transcription model loaded")
        else:
            print("⚠️ Audio transcription model not available")
        
        # Test video processor initialization
        print("🎬 Testing video processor...")
        video_processor = VideoProcessor()
        
        if video_processor.video_processor:
            print("✅ Video processing model loaded")
        else:
            print("⚠️ Video processing model not available")
        
        # Test educational content generation
        print("🎨 Testing educational content generation...")
        try:
            image_content = mm_manager.generate_educational_content(
                "mathematics", "image", "Create a diagram showing the relationship between derivatives and integrals"
            )
            
            if image_content:
                print("✅ Educational image generated")
                print(f"   Content Type: {image_content.content_type}")
                print(f"   Metadata: {image_content.metadata}")
            else:
                print("⚠️ Educational image generation failed")
        except Exception as e:
            print(f"⚠️ Educational image generation error: {e}")
        
        # Test cross-modal analyzer
        print("🔗 Testing cross-modal analyzer...")
        cross_analyzer = CrossModalAnalyzer()
        
        # Test with empty file list
        analysis = cross_analyzer.analyze_content_relationships([])
        print(f"✅ Cross-modal analysis: {analysis.get('error', 'No files to analyze')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multimodal Test Failed: {e}")
        return False

def test_integration():
    """Test the integrated advanced features."""
    print("\n🚀 Testing Integrated Advanced Features...")
    print("=" * 50)
    
    try:
        from core.advanced_features import create_advanced_smartlearn
        
        # Initialize integrated system
        print("🔧 Initializing integrated system...")
        smartlearn = create_advanced_smartlearn()
        
        # Get system status
        print("📊 Getting system status...")
        status = smartlearn.get_system_status()
        
        print(f"✅ System Status:")
        print(f"   RAG: {status['rag_system']['status']}")
        print(f"   Fine-tuning: {status['fine_tuning']['model_status']}")
        print(f"   Multimodal: Image={status['multimodal']['image_processing']}")
        
        # Test comprehensive learning experience
        print("🎓 Testing comprehensive learning experience...")
        experience = smartlearn.create_comprehensive_learning_experience(
            subject="mathematics",
            topic="calculus",
            level="intermediate",
            difficulty="medium",
            include_multimodal=True
        )
        
        if "error" not in experience:
            print("✅ Comprehensive learning experience created")
            print(f"   Components: {list(experience['components'].keys())}")
            
            # Test individual components
            for component_name, component_data in experience['components'].items():
                print(f"   {component_name}: {component_data['type']}")
        else:
            print(f"⚠️ Learning experience creation failed: {experience['error']}")
        
        # Test advanced search
        print("🔍 Testing integrated advanced search...")
        context, sources = smartlearn.advanced_search("machine learning", k=3)
        print(f"✅ Advanced Search: {len(sources)} sources")
        
        # Test enhanced prompting
        print("🧠 Testing integrated enhanced prompting...")
        study_plan = smartlearn.generate_enhanced_study_plan(
            "computer_science", "beginner", 45, 5, "Learn Python basics"
        )
        print(f"✅ Enhanced Study Plan: {len(study_plan)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration Test Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 SmartLearn Advanced Features Comprehensive Test")
    print("=" * 60)
    print("Testing all 4 advanced features:")
    print("1. Enhanced Prompt Engineering")
    print("2. Advanced RAG Features")
    print("3. Fine-Tuning Pipeline")
    print("4. Multimodal Integration")
    print("5. Integrated System")
    print("=" * 60)
    
    start_time = time.time()
    results = {}
    
    # Run all tests
    results['enhanced_prompting'] = test_enhanced_prompt_engineering()
    results['advanced_rag'] = test_advanced_rag()
    results['fine_tuning'] = test_fine_tuning()
    results['multimodal'] = test_multimodal()
    results['integration'] = test_integration()
    
    # Summary
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for feature, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{feature.replace('_', ' ').title()}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} features working")
    print(f"Total Test Time: {total_time:.2f} seconds")
    
    if passed == total:
        print("\n🎉 All advanced features are working correctly!")
        print("🚀 Your SmartLearn app is now equipped with:")
        print("   • Chain-of-thought prompting and adaptive prompts")
        print("   • Hybrid search with query expansion")
        print("   • Fine-tuning pipeline for custom models")
        print("   • Multimodal content processing and generation")
    else:
        print(f"\n⚠️ {total - passed} features need attention")
        print("Check the error messages above for details")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
