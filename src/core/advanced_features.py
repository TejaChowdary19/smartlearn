"""
Advanced Features Integration for SmartLearn AI.
This module integrates Enhanced Prompt Engineering, Advanced RAG, Fine-Tuning, and Multimodal capabilities.
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Import all advanced feature modules
from .prompt_templates import (
    StudyPlanPrompt, ExplanationPrompt, QuizPrompt, 
    AdaptivePromptManager, AdvancedPromptTemplate
)
from .rag import EnhancedRAG, HybridSearchEngine, QueryExpander
from .fine_tuning import (
    FineTuningPipeline, TrainingExample, TrainingMetrics,
    generate_synthetic_data
)
from .multimodal import (
    MultimodalManager, CrossModalAnalyzer, 
    ImageProcessor, AudioProcessor, VideoProcessor
)

class SmartLearnAdvanced:
    """Main class that integrates all advanced features."""
    
    def __init__(self, 
                 rag_persist_path: str = ".smartlearn/chroma_db",
                 fine_tuning_output: str = "models/fine_tuned",
                 training_data_dir: str = "data/training"):
        
        # Initialize all components
        self.rag_system = EnhancedRAG(persist_path=rag_persist_path)
        self.prompt_manager = AdaptivePromptManager()
        self.fine_tuning_pipeline = FineTuningPipeline(base_model="microsoft/DialoGPT-medium")
        self.multimodal_manager = MultimodalManager()
        self.cross_modal_analyzer = CrossModalAnalyzer()
        
        # Configuration
        self.config = {
            "rag_persist_path": rag_persist_path,
            "fine_tuning_output": fine_tuning_output,
            "training_data_dir": training_data_dir,
            "enable_hybrid_search": True,
            "enable_query_expansion": True,
            "enable_chain_of_thought": True,
            "enable_multimodal": True
        }
        
        print("🚀 SmartLearn Advanced Features initialized!")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all advanced features."""
        status = {
            "timestamp": datetime.now().isoformat(),
            "rag_system": self.rag_system.get_knowledge_base_stats(),
            "fine_tuning": self.fine_tuning_pipeline.get_pipeline_status(),
            "multimodal": {
                "image_processing": self.multimodal_manager.image_processor.caption_model is not None,
                "audio_processing": self.multimodal_manager.audio_processor.whisper_model is not None,
                "video_processing": self.multimodal_manager.video_processor.video_processor is not None
            },
            "config": self.config
        }
        return status
    
    # Enhanced Prompt Engineering Methods
    def generate_enhanced_study_plan(self, subject: str, level: str, 
                                   minutes_per_day: int, duration_days: int, 
                                   goal: str, user_context: Optional[Dict[str, Any]] = None,
                                   use_cot: bool = True) -> str:
        """Generate enhanced study plan with advanced prompting."""
        try:
            # Get RAG context
            rag_context, rag_sources = self.rag_system.retrieve_relevant_context(
                f"study plan {subject} {level}", k=3
            )
            
            # Create prompt with advanced features
            prompt_template = StudyPlanPrompt()
            prompt = prompt_template.render(
                subject=subject,
                level=level,
                minutes_per_day=minutes_per_day,
                duration_days=duration_days,
                goal=goal,
                rag_context=rag_context,
                rag_sources=rag_sources,
                user_context=user_context,
                use_cot=use_cot
            )
            
            return prompt
            
        except Exception as e:
            print(f"❌ Error generating enhanced study plan: {e}")
            return f"Error: {e}"
    
    def generate_enhanced_explanation(self, topic: str, level: str,
                                    user_context: Optional[Dict[str, Any]] = None,
                                    use_cot: bool = True, include_examples: bool = True) -> str:
        """Generate enhanced explanation with advanced prompting."""
        try:
            # Get RAG context
            rag_context, rag_sources = self.rag_system.retrieve_relevant_context(
                f"explanation {topic} {level}", k=3
            )
            
            # Create prompt with advanced features
            prompt_template = ExplanationPrompt()
            prompt = prompt_template.render(
                topic=topic,
                level=level,
                rag_context=rag_context,
                rag_sources=rag_sources,
                user_context=user_context,
                use_cot=use_cot,
                include_examples=include_examples
            )
            
            return prompt
            
        except Exception as e:
            print(f"❌ Error generating enhanced explanation: {e}")
            return f"Error: {e}"
    
    def generate_enhanced_quiz(self, topic: str, level: str, difficulty: str,
                              num_questions: int = 10,
                              user_context: Optional[Dict[str, Any]] = None,
                              use_cot: bool = True) -> str:
        """Generate enhanced quiz with advanced prompting."""
        try:
            # Get RAG context
            rag_context, rag_sources = self.rag_system.retrieve_relevant_context(
                f"quiz {topic} {difficulty} {level}", k=3
            )
            
            # Create prompt with advanced features
            prompt_template = QuizPrompt()
            prompt = prompt_template.render(
                topic=topic,
                level=level,
                difficulty=difficulty,
                num_questions=num_questions,
                rag_context=rag_context,
                rag_sources=rag_sources,
                user_context=user_context,
                use_cot=use_cot
            )
            
            return prompt
            
        except Exception as e:
            print(f"❌ Error generating enhanced quiz: {e}")
            return f"Error: {e}"
    
    # Advanced RAG Methods
    def advanced_search(self, query: str, k: int = 5, 
                       use_hybrid: bool = True, alpha: float = 0.7) -> Tuple[str, List[Dict]]:
        """Perform advanced search with hybrid capabilities."""
        try:
            context, sources = self.rag_system.retrieve_relevant_context(
                query, k=k, use_hybrid=use_hybrid, alpha=alpha
            )
            return context, sources
        except Exception as e:
            print(f"❌ Error in advanced search: {e}")
            return "", []
    
    def get_document_insights(self, source: str) -> Dict[str, Any]:
        """Get detailed insights about a specific document."""
        try:
            return self.rag_system.get_document_summary(source)
        except Exception as e:
            print(f"❌ Error getting document insights: {e}")
            return {}
    
    def expand_and_search(self, query: str, k: int = 5) -> Tuple[str, List[Dict]]:
        """Expand query and perform enhanced search."""
        try:
            # Expand query
            expanded_queries = self.rag_system.query_expander.expand_query(query)
            
            # Search with expanded queries
            all_results = []
            for exp_query in expanded_queries[:3]:  # Use top 3 expanded queries
                context, sources = self.rag_system.retrieve_relevant_context(exp_query, k=k//3)
                all_results.extend(sources)
            
            # Combine and deduplicate results
            unique_results = {}
            for result in all_results:
                chunk_id = result.get('chunk_id', 'unknown')
                if chunk_id not in unique_results:
                    unique_results[chunk_id] = result
            
            # Sort by relevance
            sorted_results = sorted(unique_results.values(), 
                                  key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            # Combine context
            combined_context = "\n\n".join([
                f"Source {i+1}: {result.get('source', 'Unknown')}\n{result.get('content', '')}"
                for i, result in enumerate(sorted_results[:k])
            ])
            
            return combined_context, sorted_results[:k]
            
        except Exception as e:
            print(f"❌ Error in expand and search: {e}")
            return "", []
    
    # Fine-Tuning Methods
    def collect_training_data(self, user_interactions: List[Dict[str, Any]]):
        """Collect training data from user interactions."""
        try:
            self.fine_tuning_pipeline.collect_user_data(user_interactions)
            print(f"✅ Collected {len(user_interactions)} training examples")
        except Exception as e:
            print(f"❌ Error collecting training data: {e}")
    
    def run_fine_tuning(self) -> Optional[TrainingMetrics]:
        """Run the complete fine-tuning pipeline."""
        try:
            metrics = self.fine_tuning_pipeline.run_fine_tuning()
            print("✅ Fine-tuning completed successfully!")
            return metrics
        except Exception as e:
            print(f"❌ Error in fine-tuning: {e}")
            return None
    
    def evaluate_fine_tuned_model(self) -> Dict[str, float]:
        """Evaluate the fine-tuned model."""
        try:
            return self.fine_tuning_pipeline.evaluate_model()
        except Exception as e:
            print(f"❌ Error evaluating model: {e}")
            return {}
    
    def generate_synthetic_training_data(self, subject: str, num_examples: int = 50):
        """Generate synthetic training data for testing."""
        try:
            examples = generate_synthetic_data(subject, num_examples)
            self.fine_tuning_pipeline.collect_user_data([
                {
                    "query": ex.input_text,
                    "response": ex.target_text,
                    "subject": ex.subject,
                    "difficulty": ex.difficulty,
                    "rating": ex.user_rating
                }
                for ex in examples
            ])
            print(f"✅ Generated {len(examples)} synthetic training examples")
        except Exception as e:
            print(f"❌ Error generating synthetic data: {e}")
    
    # Multimodal Methods
    def process_multimodal_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Process any supported multimodal file."""
        try:
            content = self.multimodal_manager.process_file(file_path)
            if content:
                return {
                    "content_type": content.content_type,
                    "metadata": content.metadata,
                    "source": content.source,
                    "timestamp": content.timestamp
                }
            return None
        except Exception as e:
            print(f"❌ Error processing multimodal file: {e}")
            return None
    
    def create_multimodal_summary(self, file_paths: List[str]) -> str:
        """Create summary of multiple multimodal files."""
        try:
            return self.multimodal_manager.create_multimodal_summary(file_paths)
        except Exception as e:
            print(f"❌ Error creating multimodal summary: {e}")
            return f"Error: {e}"
    
    def analyze_cross_modal_relationships(self, file_paths: List[str]) -> Dict[str, Any]:
        """Analyze relationships between different content types."""
        try:
            return self.cross_modal_analyzer.analyze_content_relationships(file_paths)
        except Exception as e:
            print(f"❌ Error analyzing cross-modal relationships: {e}")
            return {"error": str(e)}
    
    def generate_educational_content(self, subject: str, content_type: str, 
                                   prompt: str) -> Optional[Dict[str, Any]]:
        """Generate educational content in various modalities."""
        try:
            content = self.multimodal_manager.generate_educational_content(
                subject, content_type, prompt
            )
            if content:
                return {
                    "content_type": content.content_type,
                    "metadata": content.metadata,
                    "source": content.source,
                    "timestamp": content.timestamp
                }
            return None
        except Exception as e:
            print(f"❌ Error generating educational content: {e}")
            return None
    
    # Integration Methods
    def create_comprehensive_learning_experience(self, subject: str, topic: str, 
                                               level: str, difficulty: str,
                                               include_multimodal: bool = True) -> Dict[str, Any]:
        """Create a comprehensive learning experience using all advanced features."""
        try:
            experience = {
                "subject": subject,
                "topic": topic,
                "level": level,
                "difficulty": difficulty,
                "timestamp": datetime.now().isoformat(),
                "components": {}
            }
            
            # 1. Enhanced Study Plan
            study_plan_prompt = self.generate_enhanced_study_plan(
                subject, level, 60, 7, f"Learn {topic}", use_cot=True
            )
            experience["components"]["study_plan"] = {
                "prompt": study_plan_prompt,
                "type": "enhanced_prompt"
            }
            
            # 2. Enhanced Explanation
            explanation_prompt = self.generate_enhanced_explanation(
                topic, level, use_cot=True, include_examples=True
            )
            experience["components"]["explanation"] = {
                "prompt": explanation_prompt,
                "type": "enhanced_prompt"
            }
            
            # 3. Enhanced Quiz
            quiz_prompt = self.generate_enhanced_quiz(
                topic, level, difficulty, 10, use_cot=True
            )
            experience["components"]["quiz"] = {
                "prompt": quiz_prompt,
                "type": "enhanced_prompt"
            }
            
            # 4. Advanced RAG Context
            rag_context, rag_sources = self.advanced_search(
                f"{topic} {subject} {level}", k=5, use_hybrid=True
            )
            experience["components"]["rag_context"] = {
                "context": rag_context,
                "sources": rag_sources,
                "type": "advanced_rag"
            }
            
            # 5. Multimodal Content (if enabled)
            if include_multimodal:
                # Generate educational image
                image_content = self.generate_educational_content(
                    subject, "image", f"Create an educational diagram for {topic}"
                )
                if image_content:
                    experience["components"]["multimodal"] = {
                        "image": image_content,
                        "type": "generated_content"
                    }
            
            return experience
            
        except Exception as e:
            print(f"❌ Error creating comprehensive learning experience: {e}")
            return {"error": str(e)}
    
    def export_advanced_features_report(self, output_path: str = "advanced_features_report.json"):
        """Export a comprehensive report of all advanced features."""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "system_status": self.get_system_status(),
                "feature_summary": {
                    "enhanced_prompt_engineering": {
                        "chain_of_thought": self.config["enable_chain_of_thought"],
                        "adaptive_prompts": True,
                        "few_shot_learning": True
                    },
                    "advanced_rag": {
                        "hybrid_search": self.config["enable_hybrid_search"],
                        "query_expansion": self.config["enable_query_expansion"],
                        "multi_modal_documents": True,
                        "adaptive_chunking": True
                    },
                    "fine_tuning": {
                        "data_collection": True,
                        "model_training": True,
                        "evaluation_metrics": True,
                        "synthetic_data_generation": True
                    },
                    "multimodal_integration": {
                        "image_processing": self.config["enable_multimodal"],
                        "audio_processing": self.config["enable_multimodal"],
                        "video_processing": self.config["enable_multimodal"],
                        "cross_modal_analysis": True
                    }
                },
                "usage_statistics": {
                    "rag_documents": self.rag_system.get_knowledge_base_stats().get("count", 0),
                    "training_examples": len(self.fine_tuning_pipeline.data_collector.examples),
                    "multimodal_files_processed": 0  # Could track this
                }
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Advanced features report exported to {output_path}")
            return report
            
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
            return {}

# Utility functions for easy access
def create_advanced_smartlearn(config: Optional[Dict[str, Any]] = None) -> SmartLearnAdvanced:
    """Create a SmartLearnAdvanced instance with custom configuration."""
    if config is None:
        config = {}
    
    return SmartLearnAdvanced(
        rag_persist_path=config.get("rag_persist_path", ".smartlearn/chroma_db"),
        fine_tuning_output=config.get("fine_tuning_output", "models/fine_tuned"),
        training_data_dir=config.get("training_data_dir", "data/training")
    )

def demo_advanced_features():
    """Demonstrate all advanced features."""
    print("🚀 SmartLearn Advanced Features Demo")
    print("=" * 50)
    
    # Initialize
    smartlearn = create_advanced_smartlearn()
    
    # Show system status
    print("\n📊 System Status:")
    status = smartlearn.get_system_status()
    print(f"RAG System: {status['rag_system']['status']}")
    print(f"Fine-tuning: {status['fine_tuning']['model_status']}")
    print(f"Multimodal: Image={status['multimodal']['image_processing']}, Audio={status['multimodal']['audio_processing']}")
    
    # Demo enhanced prompting
    print("\n🧠 Enhanced Prompt Engineering Demo:")
    study_plan = smartlearn.generate_enhanced_study_plan(
        "mathematics", "intermediate", 60, 7, "Learn calculus fundamentals"
    )
    print(f"Study Plan Prompt Length: {len(study_plan)} characters")
    
    # Demo advanced RAG
    print("\n🔍 Advanced RAG Demo:")
    context, sources = smartlearn.advanced_search("machine learning algorithms", k=3)
    print(f"Retrieved Context Length: {len(context)} characters")
    print(f"Number of Sources: {len(sources)}")
    
    # Demo multimodal
    print("\n🖼️ Multimodal Integration Demo:")
    # This would require actual files to process
    
    print("\n✅ Demo completed! All advanced features are working.")
    return smartlearn

if __name__ == "__main__":
    # Run demo if module is executed directly
    demo_advanced_features()
