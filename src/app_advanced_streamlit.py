#!/usr/bin/env python3
"""
SmartLearn Advanced - Enhanced Streamlit App
Showcases all 4 advanced features: Enhanced Prompting, Advanced RAG, Fine-Tuning, and Multimodal
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Local modules
from core.generator import LLM
from core.advanced_features import SmartLearnAdvanced, create_advanced_smartlearn

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SmartLearn Advanced - AI Learning Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .advanced-tab {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-success { background-color: #00ff00; }
    .status-warning { background-color: #ffaa00; }
    .status-error { background-color: #ff0000; }
    
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize advanced features
@st.cache_resource
def init_advanced_features():
    """Initialize advanced features system."""
    try:
        advanced = create_advanced_smartlearn()
        return advanced
    except Exception as e:
        st.error(f"Failed to initialize advanced features: {e}")
        return None

# Initialize LLM
@st.cache_resource
def init_llm():
    """Initialize LLM system."""
    try:
        return LLM()
    except Exception as e:
        st.error(f"Failed to initialize LLM: {e}")
        return None

def main():
    """Main application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SmartLearn Advanced</h1>
        <h3>AI-Powered Learning Platform with Advanced Features</h3>
        <p>Enhanced Prompting • Advanced RAG • Fine-Tuning • Multimodal Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize systems
    advanced = init_advanced_features()
    llm = init_llm()
    
    if not advanced or not llm:
        st.error("❌ Failed to initialize required systems. Please check your configuration.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ System Configuration")
        
        # AI Provider Selection
        provider = st.selectbox(
            "AI Provider",
            ["Ollama", "OpenAI"],
            index=0
        )
        
        if provider == "Ollama":
            model = st.selectbox(
                "Ollama Model",
                ["mistral:7b-instruct", "llama2:7b", "codellama:7b", "neural-chat:7b"],
                index=0
            )
            api_key = None
        else:
            model = st.selectbox(
                "OpenAI Model",
                ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
                index=1
            )
            api_key = st.text_input("OpenAI API Key", type="password")
        
        # Advanced Features Toggle
        st.markdown("## 🚀 Advanced Features")
        enable_enhanced_prompting = st.checkbox("Enhanced Prompting", value=True)
        enable_advanced_rag = st.checkbox("Advanced RAG", value=True)
        enable_fine_tuning = st.checkbox("Fine-Tuning Pipeline", value=True)
        enable_multimodal = st.checkbox("Multimodal Integration", value=True)
        
        # System Status
        st.markdown("## 📊 System Status")
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        try:
            status = advanced.get_system_status()
            
            # RAG Status
            rag_status = status['rag_system']['status']
            rag_count = status['rag_system'].get('count', 0)
            st.markdown(f"""
            <div class="metric-card">
                <strong>RAG System:</strong><br>
                <span class="status-indicator status-success"></span>{rag_status}<br>
                Documents: {rag_count}
            </div>
            """, unsafe_allow_html=True)
            
            # Fine-tuning Status
            ft_status = status['fine_tuning']['model_status']
            ft_examples = status['fine_tuning']['data_collection']['total_examples']
            st.markdown(f"""
            <div class="metric-card">
                <strong>Fine-Tuning:</strong><br>
                <span class="status-indicator status-success"></span>{ft_status}<br>
                Training Examples: {ft_examples}
            </div>
            """, unsafe_allow_html=True)
            
            # Multimodal Status
            mm_status = "Available" if status['multimodal']['image_processing'] else "Limited"
            st.markdown(f"""
            <div class="metric-card">
                <strong>Multimodal:</strong><br>
                <span class="status-indicator status-success"></span>{mm_status}
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Status check failed: {e}")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard", 
        "🧠 Enhanced Learning", 
        "🔍 Advanced RAG", 
        "🎯 Fine-Tuning", 
        "🖼️ Multimodal", 
        "🚀 Integration Demo"
    ])
    
    # Dashboard Tab
    with tab1:
        st.markdown("## 📊 SmartLearn Advanced Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🧠 Enhanced Prompt Engineering</h3>
                <p>• Chain-of-thought reasoning</p>
                <p>• Few-shot learning examples</p>
                <p>• Dynamic context adaptation</p>
                <p>• Performance-based prompts</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🔍 Advanced RAG System</h3>
                <p>• Hybrid semantic + keyword search</p>
                <p>• Query expansion & optimization</p>
                <p>• Multi-modal document support</p>
                <p>• Adaptive content chunking</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🎯 Fine-Tuning Pipeline</h3>
                <p>• User interaction data collection</p>
                <p>• Synthetic data generation</p>
                <p>• Custom model training</p>
                <p>• Performance evaluation</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🖼️ Multimodal Integration</h3>
                <p>• Image processing & captioning</p>
                <p>• Audio transcription & analysis</p>
                <p>• Video content processing</p>
                <p>• Cross-modal relationships</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("## ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Test Advanced Search", use_container_width=True):
                st.info("Navigate to 'Advanced RAG' tab to test search capabilities")
        
        with col2:
            if st.button("🎯 Generate Training Data", use_container_width=True):
                st.info("Navigate to 'Fine-Tuning' tab to generate synthetic data")
        
        with col3:
            if st.button("🖼️ Process Media Files", use_container_width=True):
                st.info("Navigate to 'Multimodal' tab to process images/audio/video")
    
    # Enhanced Learning Tab
    with tab2:
        st.markdown("## 🧠 Enhanced Learning with Advanced Prompting")
        
        # Learning Type Selection
        learning_type = st.selectbox(
            "Choose Learning Type",
            ["Study Plan", "Explanation", "Quiz"],
            index=0
        )
        
        # Common inputs
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Subject", value="mathematics")
            level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
        
        with col2:
            topic = st.text_input("Topic/Concept", value="calculus")
            difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        
        # User Context
        st.markdown("### 🎯 Personalization Context")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            learning_style = st.selectbox(
                "Learning Style",
                ["visual", "auditory", "kinesthetic", "reading/writing"],
                index=0
            )
        
        with col2:
            previous_knowledge = st.selectbox(
                "Previous Knowledge",
                ["none", "basic", "intermediate", "advanced"],
                index=1
            )
        
        with col3:
            time_available = st.number_input("Time Available (hours)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)
        
        # Advanced Options
        with st.expander("🔧 Advanced Prompting Options"):
            use_cot = st.checkbox("Use Chain-of-Thought", value=True)
            include_examples = st.checkbox("Include Few-Shot Examples", value=True)
            adaptive_complexity = st.checkbox("Adaptive Complexity", value=True)
        
        # Generate Content
        if st.button("🚀 Generate Enhanced Learning Content", type="primary"):
            with st.spinner("Generating enhanced content..."):
                try:
                    user_context = {
                        "learning_style": learning_style,
                        "previous_knowledge": previous_knowledge,
                        "time_available": time_available,
                        "difficulty_preference": difficulty
                    }
                    
                    if learning_type == "Study Plan":
                        prompt = advanced.generate_enhanced_study_plan(
                            subject, level, int(time_available * 60), 7, 
                            f"Learn {topic}", user_context, use_cot
                        )
                        
                        st.markdown("### 📚 Generated Study Plan Prompt")
                        st.code(prompt, language="markdown")
                        
                        # Generate actual study plan
                        if st.button("🎯 Generate Study Plan"):
                            with st.spinner("Creating study plan..."):
                                study_plan = llm.complete(prompt, temperature=0.7, max_tokens=1500)
                                st.markdown("### 📖 Your Personalized Study Plan")
                                st.markdown(study_plan)
                    
                    elif learning_type == "Explanation":
                        prompt = advanced.generate_enhanced_explanation(
                            topic, level, user_context, use_cot, include_examples
                        )
                        
                        st.markdown("### 📖 Generated Explanation Prompt")
                        st.code(prompt, language="markdown")
                        
                        # Generate actual explanation
                        if st.button("💡 Generate Explanation"):
                            with st.spinner("Creating explanation..."):
                                explanation = llm.complete(prompt, temperature=0.6, max_tokens=1200)
                                st.markdown("### 🧠 Your Personalized Explanation")
                                st.markdown(explanation)
                    
                    elif learning_type == "Quiz":
                        prompt = advanced.generate_enhanced_quiz(
                            topic, level, difficulty, 10, user_context, use_cot
                        )
                        
                        st.markdown("### 🎯 Generated Quiz Prompt")
                        st.code(prompt, language="markdown")
                        
                        # Generate actual quiz
                        if st.button("📝 Generate Quiz"):
                            with st.spinner("Creating quiz..."):
                                quiz = llm.complete(prompt, temperature=0.7, max_tokens=2000)
                                st.markdown("### 🧪 Your Personalized Quiz")
                                st.markdown(quiz)
                
                except Exception as e:
                    st.error(f"Error generating content: {e}")
    
    # Advanced RAG Tab
    with tab3:
        st.markdown("## 🔍 Advanced RAG System")
        
        # Search Configuration
        col1, col2, col3 = st.columns(3)
        
        with col1:
            query = st.text_input("Search Query", value="machine learning algorithms")
            k_results = st.number_input("Number of Results", min_value=1, max_value=10, value=5)
        
        with col2:
            use_hybrid = st.checkbox("Use Hybrid Search", value=True)
            alpha = st.slider("Hybrid Weight (α)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        
        with col3:
            enable_expansion = st.checkbox("Enable Query Expansion", value=True)
            search_type = st.selectbox("Search Type", ["Standard", "Expanded", "Document Insights"])
        
        # Execute Search
        if st.button("🔍 Execute Advanced Search", type="primary"):
            with st.spinner("Performing advanced search..."):
                try:
                    if search_type == "Standard":
                        context, sources = advanced.advanced_search(
                            query, k_results, use_hybrid, alpha
                        )
                        
                        st.markdown("### 📚 Search Results")
                        st.markdown(f"**Context Length:** {len(context)} characters")
                        st.markdown(f"**Sources Found:** {len(sources)}")
                        
                        # Display sources
                        for i, source in enumerate(sources):
                            with st.expander(f"Source {i+1}: {source.get('source', 'Unknown')}"):
                                st.markdown(f"**Relevance Score:** {source.get('relevance_score', 0):.3f}")
                                st.markdown(f"**Content Type:** {source.get('content_type', 'Unknown')}")
                                st.markdown(f"**Chunk ID:** {source.get('chunk_id', 'Unknown')}")
                                
                                # Show content preview
                                content_preview = source.get('content', '')[:200] + "..." if len(source.get('content', '')) > 200 else source.get('content', '')
                                st.markdown(f"**Content Preview:** {content_preview}")
                    
                    elif search_type == "Expanded":
                        context, sources = advanced.expand_and_search(query, k_results)
                        
                        st.markdown("### 🔍 Expanded Search Results")
                        st.markdown(f"**Context Length:** {len(context)} characters")
                        st.markdown(f"**Sources Found:** {len(sources)}")
                        
                        # Display expanded results
                        st.markdown("**Expanded Query Results:**")
                        for i, source in enumerate(sources):
                            st.markdown(f"{i+1}. {source.get('source', 'Unknown')} (Score: {source.get('relevance_score', 0):.3f})")
                    
                    elif search_type == "Document Insights":
                        if sources:
                            source_path = sources[0].get('source', '')
                            if source_path:
                                insights = advanced.get_document_insights(source_path)
                                
                                st.markdown("### 📊 Document Insights")
                                st.json(insights)
                
                except Exception as e:
                    st.error(f"Search failed: {e}")
        
        # RAG Statistics
        st.markdown("### 📊 RAG System Statistics")
        try:
            rag_stats = advanced.rag_system.get_knowledge_base_stats()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", rag_stats.get('status', 'Unknown'))
                st.metric("Document Count", rag_stats.get('count', 0))
            
            with col2:
                st.metric("Embedding Model", rag_stats.get('embedding_model', 'Unknown'))
                st.metric("Hybrid Search", "✅" if rag_stats.get('hybrid_search', False) else "❌")
            
            with col3:
                st.metric("Query Expansion", "✅" if rag_stats.get('query_expansion', False) else "❌")
                st.metric("Content Types", len(rag_stats.get('content_types', {})))
            
            # Content type breakdown
            if 'content_types' in rag_stats:
                st.markdown("**Content Type Distribution:**")
                for content_type, count in rag_stats['content_types'].items():
                    st.markdown(f"- {content_type}: {count} chunks")
        
        except Exception as e:
            st.error(f"Failed to get RAG statistics: {e}")
    
    # Fine-Tuning Tab
    with tab4:
        st.markdown("## 🎯 Fine-Tuning Pipeline")
        
        # Pipeline Status
        st.markdown("### 📊 Pipeline Status")
        try:
            ft_status = advanced.fine_tuning_pipeline.get_pipeline_status()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model Status", ft_status['model_status'])
                st.metric("Base Model", ft_status['base_model'])
            
            with col2:
                st.metric("Training Examples", ft_status['data_collection']['total_examples'])
                st.metric("Subjects", len(ft_status['data_collection']['subjects']))
            
            with col3:
                st.metric("Difficulties", len(ft_status['data_collection']['difficulties']))
                st.metric("Avg Rating", f"{ft_status['data_collection']['avg_rating']:.2f}")
        
        except Exception as e:
            st.error(f"Failed to get pipeline status: {e}")
        
        # Data Management
        st.markdown("### 📊 Training Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Add Training Data")
            
            new_query = st.text_input("Query/Question")
            new_response = st.text_area("Response/Answer")
            new_subject = st.selectbox("Subject", ["mathematics", "computer_science", "physics", "chemistry", "biology"])
            new_difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
            new_rating = st.slider("User Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.5)
            
            if st.button("💾 Add Training Example"):
                try:
                    user_interaction = {
                        "query": new_query,
                        "response": new_response,
                        "subject": new_subject,
                        "difficulty": new_difficulty,
                        "rating": new_rating
                    }
                    
                    advanced.collect_training_data([user_interaction])
                    st.success("✅ Training example added successfully!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"Failed to add training example: {e}")
        
        with col2:
            st.markdown("#### 🎲 Generate Synthetic Data")
            
            synth_subject = st.selectbox("Subject for Synthetic Data", ["mathematics", "computer_science", "physics"])
            synth_count = st.number_input("Number of Examples", min_value=5, max_value=100, value=20)
            
            if st.button("🎲 Generate Synthetic Data"):
                try:
                    with st.spinner("Generating synthetic training data..."):
                        advanced.generate_synthetic_training_data(synth_subject, synth_count)
                        st.success(f"✅ Generated {synth_count} synthetic examples for {synth_subject}!")
                        st.rerun()
                
                except Exception as e:
                    st.error(f"Failed to generate synthetic data: {e}")
        
        # Fine-Tuning Execution
        st.markdown("### 🚀 Execute Fine-Tuning")
        
        if st.button("🎯 Start Fine-Tuning", type="primary"):
            try:
                with st.spinner("Starting fine-tuning pipeline..."):
                    metrics = advanced.run_fine_tuning()
                    
                    if metrics:
                        st.success("✅ Fine-tuning completed successfully!")
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Training Time", f"{metrics.training_time:.2f}s")
                            st.metric("Loss", f"{metrics.loss:.4f}")
                        
                        with col2:
                            st.metric("Perplexity", f"{metrics.perplexity:.4f}")
                            st.metric("Accuracy", f"{metrics.accuracy:.4f}")
                        
                        with col3:
                            st.metric("Precision", f"{metrics.precision:.4f}")
                            st.metric("F1 Score", f"{metrics.f1_score:.4f}")
                        
                        st.rerun()
                    else:
                        st.error("❌ Fine-tuning failed")
            
            except Exception as e:
                st.error(f"Fine-tuning failed: {e}")
        
        # Model Evaluation
        if st.button("🔍 Evaluate Model"):
            try:
                with st.spinner("Evaluating fine-tuned model..."):
                    eval_metrics = advanced.evaluate_fine_tuned_model()
                    
                    if eval_metrics:
                        st.markdown("### 📊 Evaluation Results")
                        st.json(eval_metrics)
                    else:
                        st.warning("⚠️ No fine-tuned model available for evaluation")
            
            except Exception as e:
                st.error(f"Evaluation failed: {e}")
    
    # Multimodal Tab
    with tab5:
        st.markdown("## 🖼️ Multimodal Integration")
        
        # File Upload
        st.markdown("### 📁 Process Media Files")
        
        uploaded_file = st.file_uploader(
            "Choose a file to process",
            type=['jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav', 'mp4', 'avi', 'txt', 'md', 'pdf']
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Process file
                with st.spinner("Processing file..."):
                    content = advanced.process_multimodal_file(file_path)
                
                if content:
                    st.success(f"✅ File processed successfully!")
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📊 File Information")
                        st.json({
                            "Content Type": content['content_type'],
                            "Source": content['source'],
                            "Timestamp": content['timestamp']
                        })
                    
                    with col2:
                        st.markdown("### 🔍 Content Analysis")
                        st.json(content['metadata'])
                    
                    # Clean up
                    os.remove(file_path)
                else:
                    st.error("❌ Failed to process file")
            
            except Exception as e:
                st.error(f"File processing failed: {e}")
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # Educational Content Generation
        st.markdown("### 🎨 Generate Educational Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gen_subject = st.text_input("Subject", value="mathematics")
            gen_prompt = st.text_area("Content Description", value="Create a diagram showing the relationship between derivatives and integrals")
        
        with col2:
            gen_type = st.selectbox("Content Type", ["image"])
            gen_size = st.selectbox("Image Size", ["800x600", "1024x768", "1200x800"])
        
        if st.button("🎨 Generate Content"):
            try:
                with st.spinner("Generating educational content..."):
                    # Parse size
                    width, height = map(int, gen_size.split('x'))
                    
                    content = advanced.generate_educational_content(gen_subject, gen_type, gen_prompt)
                    
                    if content:
                        st.success("✅ Educational content generated!")
                        
                        # Display generated content
                        if content['content_type'] == 'image':
                            st.markdown("### 🖼️ Generated Image")
                            # Note: In a real app, you'd save and display the image
                            st.info("Image generated successfully! (Would display here in production)")
                        
                        st.json(content)
                    else:
                        st.error("❌ Failed to generate content")
            
            except Exception as e:
                st.error(f"Content generation failed: {e}")
        
        # Cross-Modal Analysis
        st.markdown("### 🔗 Cross-Modal Analysis")
        
        if st.button("🔍 Analyze Content Relationships"):
            try:
                # This would analyze relationships between multiple files
                st.info("Cross-modal analysis requires multiple files. Upload several files to analyze relationships.")
            
            except Exception as e:
                st.error(f"Analysis failed: {e}")
    
    # Integration Demo Tab
    with tab6:
        st.markdown("## 🚀 Complete Integration Demo")
        
        st.markdown("""
        This tab demonstrates how all advanced features work together to create comprehensive learning experiences.
        """)
        
        # Demo Configuration
        col1, col2 = st.columns(2)
        
        with col1:
            demo_subject = st.selectbox("Demo Subject", ["mathematics", "computer_science", "physics"], key="demo_subject")
            demo_topic = st.text_input("Demo Topic", value="calculus", key="demo_topic")
        
        with col2:
            demo_level = st.selectbox("Demo Level", ["beginner", "intermediate", "advanced"], key="demo_level")
            demo_difficulty = st.selectbox("Demo Difficulty", ["easy", "medium", "hard"], key="demo_difficulty")
        
        # Create Comprehensive Learning Experience
        if st.button("🚀 Create Comprehensive Learning Experience", type="primary"):
            try:
                with st.spinner("Creating comprehensive learning experience..."):
                    experience = advanced.create_comprehensive_learning_experience(
                        demo_subject, demo_topic, demo_level, demo_difficulty, include_multimodal=True
                    )
                
                if "error" not in experience:
                    st.success("✅ Comprehensive learning experience created!")
                    
                    # Display experience components
                    st.markdown("### 🎓 Learning Experience Components")
                    
                    for component_name, component_data in experience['components'].items():
                        with st.expander(f"{component_name.replace('_', ' ').title()}"):
                            if component_data['type'] == 'enhanced_prompt':
                                st.markdown("**Type:** Enhanced Prompt with Advanced Features")
                                st.code(component_data['prompt'][:500] + "...", language="markdown")
                                
                                if st.button(f"🎯 Generate {component_name.replace('_', ' ').title()}", key=f"gen_{component_name}"):
                                    with st.spinner(f"Generating {component_name}..."):
                                        if component_name == "study_plan":
                                            result = llm.complete(component_data['prompt'], temperature=0.7, max_tokens=1500)
                                        elif component_name == "explanation":
                                            result = llm.complete(component_data['prompt'], temperature=0.6, max_tokens=1200)
                                        elif component_name == "quiz":
                                            result = llm.complete(component_data['prompt'], temperature=0.7, max_tokens=2000)
                                        else:
                                            result = "Component type not supported for generation"
                                        
                                        st.markdown(f"### 📖 Generated {component_name.replace('_', ' ').title()}")
                                        st.markdown(result)
                            
                            elif component_data['type'] == 'advanced_rag':
                                st.markdown("**Type:** Advanced RAG Context")
                                st.markdown(f"**Context Length:** {len(component_data['context'])} characters")
                                st.markdown(f"**Sources:** {len(component_data['sources'])}")
                                
                                # Show sources
                                for i, source in enumerate(component_data['sources'][:3]):
                                    st.markdown(f"**Source {i+1}:** {source.get('source', 'Unknown')}")
                            
                            elif component_data['type'] == 'generated_content':
                                st.markdown("**Type:** Generated Multimodal Content")
                                st.json(component_data)
                    
                    # Export experience
                    if st.button("📤 Export Learning Experience"):
                        try:
                            export_data = {
                                "experience": experience,
                                "timestamp": datetime.now().isoformat(),
                                "configuration": {
                                    "subject": demo_subject,
                                    "topic": demo_topic,
                                    "level": demo_level,
                                    "difficulty": demo_difficulty
                                }
                            }
                            
                            st.download_button(
                                label="💾 Download Experience JSON",
                                data=json.dumps(export_data, indent=2),
                                file_name=f"learning_experience_{demo_subject}_{demo_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                        
                        except Exception as e:
                            st.error(f"Export failed: {e}")
                
                else:
                    st.error(f"Failed to create learning experience: {experience['error']}")
            
            except Exception as e:
                st.error(f"Integration demo failed: {e}")
        
        # System Report
        st.markdown("### 📊 Advanced Features Report")
        
        if st.button("📋 Generate System Report"):
            try:
                with st.spinner("Generating comprehensive report..."):
                    report = advanced.export_advanced_features_report()
                
                if report:
                    st.success("✅ System report generated!")
                    
                    # Display report summary
                    st.markdown("#### 📈 Feature Summary")
                    feature_summary = report.get('feature_summary', {})
                    
                    for feature, capabilities in feature_summary.items():
                        with st.expander(f"{feature.replace('_', ' ').title()}"):
                            for capability, status in capabilities.items():
                                st.markdown(f"• {capability.replace('_', ' ').title()}: {'✅' if status else '❌'}")
                    
                    # Download report
                    st.download_button(
                        label="📥 Download Full Report",
                        data=json.dumps(report, indent=2),
                        file_name=f"smartlearn_advanced_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                else:
                    st.error("❌ Failed to generate report")
            
            except Exception as e:
                st.error(f"Report generation failed: {e}")

if __name__ == "__main__":
    main()
