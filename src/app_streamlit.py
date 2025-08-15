import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Local modules
from core.generator import LLM
from core.prompt_templates import StudyPlanPrompt, ExplanationPrompt, QuizPrompt
from core.rag import EnhancedRAG

# Load environment variables
load_dotenv()

# Helper functions for quiz functionality
def parse_quiz_data(quiz_text, num_questions):
    """Parse AI-generated quiz text into structured format"""
    try:
        lines = quiz_text.strip().split('\n')
        questions = []
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for question start
            if line.startswith('Q') and line[1].isdigit():
                if current_question:
                    questions.append(current_question)
                
                current_question = {
                    'question': '',
                    'options': [],
                    'correct': '',
                    'explanation': ''
                }
                
                # Extract question text
                question_text = line.split('.', 1)[1].strip() if '.' in line else line
                current_question['question'] = question_text
                
            # Check for options
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                option_text = line.split(')', 1)[1].strip()
                current_question['options'].append(option_text)
                
            # Check for correct answer
            elif line.startswith('Correct:'):
                correct = line.split(':', 1)[1].strip()
                current_question['correct'] = correct
                
            # Check for explanation
            elif line.startswith('Explanation:'):
                explanation = line.split(':', 1)[1].strip()
                current_question['explanation'] = explanation
        
        # Add the last question
        if current_question:
            questions.append(current_question)
        
        # Validate we have the right number of questions
        if len(questions) == num_questions and all(len(q['options']) == 4 for q in questions):
            return questions
        else:
            return None
            
    except Exception as e:
        st.error(f"Error parsing quiz: {e}")
        return None

def grade_quiz(questions, user_answers):
    """Grade the quiz and return score and results"""
    total_questions = len(questions)
    correct_answers = 0
    results = []
    
    for i, question in enumerate(questions, 1):
        user_answer = user_answers.get(i, "Not answered")
        correct_answer_letter = question['correct']  # e.g., "A", "B", "C", "D"
        
        # Map user's selected option text to the corresponding letter
        user_answer_letter = None
        if user_answer != "Not answered":
            for idx, option in enumerate(question['options']):
                if option == user_answer:
                    user_answer_letter = chr(65 + idx)  # Convert 0,1,2,3 to A,B,C,D
                    break
        
        # Compare the letters
        is_correct = user_answer_letter == correct_answer_letter
        
        if is_correct:
            correct_answers += 1
            
        results.append({
            'question_num': i,
            'user_answer': user_answer,
            'user_answer_letter': user_answer_letter,
            'correct_answer_letter': correct_answer_letter,
            'correct': is_correct
        })
    
    score = int((correct_answers / total_questions) * 100)
    return score, results

def get_score_message(score):
    """Get a motivational message based on score"""
    if score >= 90:
        return "🎉 Outstanding! You're a master of this subject!"
    elif score >= 80:
        return "🌟 Excellent work! You have a strong understanding!"
    elif score >= 70:
        return "👍 Good job! You're on the right track!"
    elif score >= 60:
        return "📚 Not bad! Keep studying to improve!"
    else:
        return "💪 Keep practicing! Every mistake is a learning opportunity!"

# Page configuration
st.set_page_config(
    page_title="SmartLearn Pro - AI-Powered Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Professional Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main app styling - Ultra Dark Theme */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
        padding: 0;
        color: #ffffff;
    }
    
    /* Ultra Professional header */
    .pro-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
        padding: 4rem 0;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 3rem 3rem;
        box-shadow: 0 25px 80px rgba(0,0,0,0.6);
        position: relative;
        overflow: hidden;
    }
    
    .pro-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="15" height="15" patternUnits="userSpaceOnUse"><path d="M 15 0 L 0 0 0 15" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.3"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.4;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        text-align: center;
        color: white;
    }
    
    .header-title {
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
        margin-bottom: 2rem;
        color: #e2e8f0;
        letter-spacing: 0.01em;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 1rem 2rem;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Ultra Professional sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%);
        border-right: 1px solid #404040;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        padding: 2rem 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 12px 40px rgba(255, 107, 107, 0.4);
    }
    
    .sidebar-header h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .settings-card {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border: 1px solid #505050;
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }
    
    .settings-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
    }
    
    .settings-card h4 {
        color: #ffffff;
        margin-bottom: 1.5rem;
        font-size: 1.2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Ultra Professional tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: 3px solid #404040;
        padding: 0 0 1.5rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%);
        border-radius: 16px 16px 0 0;
        border: 2px solid #505050;
        border-bottom: none;
        padding: 1.2rem 2rem;
        font-weight: 700;
        color: #cbd5e1;
        transition: all 0.4s ease;
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        border-color: #ff6b6b;
        box-shadow: 0 8px 30px rgba(255, 107, 107, 0.4);
        transform: translateY(-3px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #505050;
        transform: translateY(-2px);
        color: #ffffff;
        border-color: #ff6b6b;
    }
    
    /* Ultra Professional inputs */
    .stTextInput > div > div > input {
        border-radius: 16px;
        border: 2px solid #505050;
        padding: 16px 20px;
        font-size: 1rem;
        transition: all 0.4s ease;
        background: #1a1a1a;
        color: #ffffff;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.2);
        outline: none;
        background: #2d2d2d;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #808080;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 16px;
        border: 2px solid #505050;
        padding: 20px;
        font-size: 1rem;
        transition: all 0.4s ease;
        background: #1a1a1a;
        color: #ffffff;
        min-height: 140px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.2);
        outline: none;
        background: #2d2d2d;
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #808080;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 16px;
        border: 2px solid #505050;
        padding: 16px 20px;
        font-size: 1rem;
        transition: all 0.4s ease;
        background: #1a1a1a;
        color: #ffffff;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.2);
        outline: none;
        background: #2d2d2d;
        transform: translateY(-2px);
    }
    
    .stSelectbox > div > div > div {
        border-radius: 16px;
        border: 2px solid #505050;
        padding: 12px 20px;
        font-size: 1rem;
        transition: all 0.4s ease;
        background: #1a1a1a;
        color: #ffffff;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stSelectbox > div > div > div:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.2);
        outline: none;
        background: #2d2d2d;
        transform: translateY(-2px);
    }
    
    /* Ultra Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 18px 40px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.01em;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 45px rgba(255, 107, 107, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-2px);
    }
    
    /* Secondary button style */
    .btn-secondary {
        background: linear-gradient(135deg, #808080 0%, #606060 100%) !important;
        box-shadow: 0 12px 35px rgba(128, 128, 128, 0.4) !important;
    }
    
    .btn-secondary:hover {
        box-shadow: 0 20px 45px rgba(128, 128, 128, 0.5) !important;
    }
    
    /* Ultra Professional content cards */
    .content-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 16px 50px rgba(0,0,0,0.4);
        border: 1px solid #404040;
        position: relative;
        overflow: hidden;
        color: #ffffff;
    }
    
    .content-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
    }
    
    .content-card h3 {
        color: #ffffff;
        margin-bottom: 1.5rem;
        font-size: 1.8rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 1rem;
        letter-spacing: -0.01em;
    }
    
    .content-card p {
        color: #e2e8f0;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Grid layout */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .grid-item {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border: 1px solid #404040;
        transition: all 0.4s ease;
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }
    
    .grid-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(135deg, #4ecdc4 0%, #45b7d1 100%);
    }
    
    .grid-item:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        border-color: #ff6b6b;
    }
    
    .grid-item h4 {
        color: #ffffff;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .grid-item p {
        color: #e2e8f0;
        margin-bottom: 0.75rem;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Label styling */
    .stTextInput > label, .stTextArea > label, .stNumberInput > label, .stSelectbox > label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > div > label {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Success and error messages */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.4);
        border: none;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.4);
        border: none;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border: 4px solid #404040;
        border-top: 4px solid #ff6b6b;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        
        .header-subtitle {
            font-size: 1.2rem;
        }
        
        .content-card {
            padding: 2rem;
        }
        
        .grid-container {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Ultra Professional header
st.markdown("""
<div class="pro-header">
    <div class="header-content">
        <h1 class="header-title">🎓 SmartLearn Pro</h1>
        <p class="header-subtitle">Ultra-Professional AI-Powered Study Assistant</p>
        <div class="header-badge">Powered by Advanced LLM Technology</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>⚙️ Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="settings-card">
        <h4>🔧 AI Provider Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    provider = st.selectbox(
        "AI Provider",
        ["Ollama", "OpenAI"],
        help="Choose your preferred AI provider for generating content"
    )
    
    if provider == "Ollama":
        model = st.text_input(
            "Model Name",
            value="mistral:7b-instruct",
            help="Enter the Ollama model name (e.g., mistral:7b-instruct, llama2:7b)"
        )
        base_url = st.text_input(
            "Base URL",
            value="http://localhost:11434",
            help="Ollama server URL (default: http://localhost:11434)"
        )
    else:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key"
        )
        model = st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo"],
            help="Select OpenAI model"
        )
    
    st.markdown("""
    <div class="settings-card">
        <h4>📚 Study Preferences</h4>
    </div>
    """, unsafe_allow_html=True)
    
    use_rag = st.checkbox(
        "Enable RAG (Knowledge Base)",
        value=False,
        help="Use your knowledge base for more accurate responses"
    )
    
    if use_rag:
        knowledge_base_path = st.text_input(
            "Knowledge Base Path",
            value="data/knowledge_base/",
            help="Path to your knowledge base directory"
        )

# Initialize RAG system
rag_system = None
if use_rag:
    try:
        rag_system = EnhancedRAG()
        if st.button("🔄 Load Knowledge Base", type="secondary"):
            with st.spinner("Loading knowledge base documents..."):
                success = rag_system.load_knowledge_base(knowledge_base_path)
                if success:
                    st.success("✅ Knowledge base loaded successfully!")
                    # Store RAG system in session state
                    st.session_state.rag_system = rag_system
                else:
                    st.error("❌ Failed to load knowledge base")
        else:
            # Check if RAG system is already loaded
            if 'rag_system' in st.session_state:
                rag_system = st.session_state.rag_system
                stats = rag_system.get_knowledge_base_stats()
                if stats['status'] == "Documents loaded" and stats['count'] > 0:
                    st.success(f"✅ Knowledge base ready ({stats['count']} chunks)")
                else:
                    st.info("ℹ️ Click 'Load Knowledge Base' to initialize")
    except Exception as e:
        st.error(f"❌ Error initializing RAG: {str(e)}")

# RAG Status Display
if use_rag:
    st.markdown("""
    <div class="settings-card">
        <h4>🔍 RAG Status</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if 'rag_system' in st.session_state:
        rag_system = st.session_state.rag_system
        stats = rag_system.get_knowledge_base_stats()
        
        if stats['status'] == "Documents loaded" and stats['count'] > 0:
            st.success(f"✅ Knowledge Base Active")
            st.info(f"📊 {stats['count']} document chunks loaded")
            st.info(f"🤖 Using: {stats['embedding_model']}")
            
            # Add a search functionality
            search_query = st.text_input(
                "🔍 Search Knowledge Base",
                placeholder="Search for specific topics...",
                help="Search your knowledge base for relevant information"
            )
            
            if search_query:
                if st.button("🔍 Search", type="secondary"):
                    with st.spinner("Searching knowledge base..."):
                        results = rag_system.search_similar_documents(search_query, k=3)
                        if results:
                            st.success(f"Found {len(results)} relevant documents")
                            for i, result in enumerate(results, 1):
                                with st.expander(f"📄 Source {i}: {result['source']}", expanded=False):
                                    st.markdown(f"**Relevance:** {result['relevance']:.2f}")
                                    st.markdown(f"**Content:** {result['content']}")
                        else:
                            st.info("No relevant documents found")
        else:
            st.warning("⚠️ Knowledge base not loaded")
            st.info("Click 'Load Knowledge Base' to initialize")
    else:
        st.info("ℹ️ RAG system ready to initialize")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Study Plan", "💡 Explanations", "🧠 Adaptive Quiz", "📊 Progress Tracker"])

# Study Plan Tab
with tab1:
    st.markdown("""
    <div class="content-card">
        <h3>🎯 Personalized Study Plan Generator</h3>
        <p>Create comprehensive, AI-powered study plans tailored to your learning goals and schedule.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        subject = st.text_input(
            "Subject/Topic",
            placeholder="e.g., Machine Learning, Organic Chemistry, World History",
            help="Enter the subject or specific topic you want to study"
        )
        
        learning_goals = st.text_area(
            "Learning Goals",
            placeholder="What do you want to achieve? What skills should you develop?",
            help="Describe your specific learning objectives and desired outcomes"
        )
        
        time_available = st.number_input(
            "Time Available (hours per week)",
            min_value=1,
            max_value=40,
            value=10,
            help="How many hours can you dedicate to studying each week?"
        )
        
        difficulty_level = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"],
            help="Select your current proficiency level"
        )
    
    with col2:
        st.markdown("""
        <div class="grid-item">
            <h4>📊 Quick Stats</h4>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Time:</strong> {time_available}h/week</p>
            <p><strong>Level:</strong> {difficulty_level}</p>
        </div>
        """.format(subject=subject or "Not specified", time_available=time_available, difficulty_level=difficulty_level), unsafe_allow_html=True)
    
    if st.button("🚀 Generate Study Plan", type="primary"):
        if subject and learning_goals:
            with st.spinner("🤖 AI is crafting your personalized study plan..."):
                try:
                    # Initialize LLM with proper parameters
                    if provider == "Ollama":
                        llm = LLM(provider="ollama", model=model)
                    else:
                        st.error("OpenAI integration not yet implemented")
                        st.stop()
                    
                    # RAG Integration: Retrieve relevant context from knowledge base
                    rag_context = ""
                    rag_sources = []
                    if rag_system and 'rag_system' in st.session_state:
                        try:
                            # Retrieve relevant context for the subject
                            rag_context, rag_sources = rag_system.retrieve_relevant_context(
                                f"study plan {subject} {difficulty_level} {learning_goals}", 
                                k=3
                            )
                            if rag_context:
                                st.info(f"🔍 Found {len(rag_sources)} relevant knowledge base sources")
                        except Exception as e:
                            st.warning(f"⚠️ RAG retrieval failed: {str(e)}")
                    
                    # Create enhanced prompt using the prompt template
                    from core.prompt_templates import StudyPlanPrompt
                    prompt_template = StudyPlanPrompt()
                    
                    # Calculate duration in days (assuming 7 days per week)
                    duration_days = max(7, (time_available * 4) // 60)  # Convert hours to days
                    
                    custom_prompt = prompt_template.render(
                        subject=subject,
                        level=difficulty_level,
                        minutes_per_day=time_available * 60 // 7,  # Convert to minutes per day
                        duration_days=duration_days,
                        goal=learning_goals,
                        rag_context=rag_context,
                        rag_sources=rag_sources
                    )
                    
                    study_plan = llm.complete(custom_prompt, temperature=0.7, max_tokens=1500)
                    
                    # Display the study plan
                    st.markdown("""
                    <div class="content-card">
                        <h3>📋 Your Personalized Study Plan</h3>
                        <div style="background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%); padding: 2rem; border-radius: 20px; border-left: 4px solid #ff6b6b; color: #ffffff; line-height: 1.8;">
                            {plan}
                        </div>
                    </div>
                    """.format(plan=study_plan.replace('\n', '<br>')), unsafe_allow_html=True)
                    
                    # Display RAG sources if available
                    if rag_sources:
                        with st.expander("🔍 Knowledge Base Sources Used", expanded=False):
                            st.markdown("**Sources that enhanced your study plan:**")
                            for i, source in enumerate(rag_sources, 1):
                                st.markdown(f"""
                                **Source {i}:** {source['source']}
                                - Relevance: {source['relevance_score']:.2f}
                                - Chunk ID: {source['chunk_id']}
                                """)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Study Plan",
                        data=study_plan,
                        file_name=f"study_plan_{subject.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error generating study plan: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields to generate a study plan.")

# Explanations Tab
with tab2:
    st.markdown("""
    <div class="content-card">
        <h3>💡 AI-Powered Concept Explanations</h3>
        <p>Get clear, comprehensive explanations of complex concepts with examples and analogies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        concept = st.text_input(
            "Concept to Explain",
            placeholder="e.g., Quantum entanglement, Photosynthesis, Derivatives in calculus",
            help="Enter the concept you'd like explained"
        )
        
        explanation_type = st.selectbox(
            "Explanation Style",
            ["Simple", "Detailed", "With Examples", "With Analogies"],
            help="Choose how you'd like the concept explained"
        )
        
        background_level = st.selectbox(
            "Your Background",
            ["Complete Beginner", "Some Knowledge", "Intermediate", "Advanced"],
            help="Select your current understanding level"
        )
    
    with col2:
        st.markdown("""
        <div class="grid-item">
            <h4>🎯 Explanation Preferences</h4>
            <p><strong>Style:</strong> {style}</p>
            <p><strong>Background:</strong> {background}</p>
        </div>
        """.format(style=explanation_type, background=background_level), unsafe_allow_html=True)
    
    if st.button("💡 Explain Concept", type="primary"):
        if concept:
            with st.spinner("🤖 AI is crafting your explanation..."):
                try:
                    # Initialize LLM with proper parameters
                    if provider == "Ollama":
                        llm = LLM(provider="ollama", model=model)
                    else:
                        st.error("OpenAI integration not yet implemented")
                        st.stop()
                    
                    # RAG Integration: Retrieve relevant context from knowledge base
                    rag_context = ""
                    rag_sources = []
                    if rag_system and 'rag_system' in st.session_state:
                        try:
                            # Retrieve relevant context for the concept
                            rag_context, rag_sources = rag_system.retrieve_relevant_context(
                                f"{concept} {explanation_type} {background_level}", 
                                k=3
                            )
                            if rag_context:
                                st.info(f"🔍 Found {len(rag_sources)} relevant knowledge base sources")
                        except Exception as e:
                            st.warning(f"⚠️ RAG retrieval failed: {str(e)}")
                    
                    # Create enhanced prompt using the prompt template
                    from core.prompt_templates import ExplanationPrompt
                    prompt_template = ExplanationPrompt()
                    
                    # Map background level to template level
                    level_mapping = {
                        "Complete Beginner": "beginner",
                        "Some Knowledge": "intermediate", 
                        "Intermediate": "intermediate",
                        "Advanced": "advanced"
                    }
                    template_level = level_mapping.get(background_level, "intermediate")
                    
                    custom_prompt = prompt_template.render(
                        topic=concept,
                        level=template_level,
                        rag_context=rag_context,
                        rag_sources=rag_sources
                    )
                    
                    explanation = llm.complete(custom_prompt, temperature=0.6, max_tokens=1200)
                    
                    # Display the explanation
                    st.markdown("""
                    <div class="content-card">
                        <h3>📚 Concept Explanation: {concept}</h3>
                        <div style="background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%); padding: 2rem; border-radius: 20px; border-left: 4px solid #4ecdc4; color: #ffffff; line-height: 1.8;">
                            {explanation}
                        </div>
                    </div>
                    """.format(concept=concept, explanation=explanation.replace('\n', '<br>')), unsafe_allow_html=True)
                    
                    # Display RAG sources if available
                    if rag_sources:
                        with st.expander("🔍 Knowledge Base Sources Used", expanded=False):
                            st.markdown("**Sources that enhanced your explanation:**")
                            for i, source in enumerate(rag_sources, 1):
                                st.markdown(f"""
                                **Source {i}:** {source['source']}
                                - Relevance: {source['relevance_score']:.2f}
                                - Chunk ID: {source['chunk_id']}
                                """)
                    
                except Exception as e:
                    st.error(f"❌ Error generating explanation: {str(e)}")
        else:
            st.warning("⚠️ Please enter a concept to explain.")

# Interactive Quiz Tab
with tab3:
    st.markdown("""
    <div class="content-card">
        <h3>🧠 Interactive Quiz System</h3>
        <p>Test your knowledge with AI-generated quizzes. Answer questions and get instant feedback!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Define difficulty guidelines at the tab level so they can be accessed throughout
    difficulty_guidelines = {
        "Easy": {
            "concepts": "basic concepts, definitions, simple facts",
            "complexity": "straightforward questions with obvious answers",
            "examples": "What is X? Which of these is correct? Basic terminology",
            "description": "Beginner-friendly questions focusing on fundamental knowledge"
        },
        "Medium": {
            "concepts": "intermediate concepts, applications, moderate complexity",
            "complexity": "questions requiring some understanding and reasoning",
            "examples": "How does X work? Which scenario demonstrates Y? Compare and contrast",
            "description": "Intermediate questions requiring understanding and application"
        },
        "Hard": {
            "concepts": "advanced concepts, analysis, synthesis, complex scenarios",
            "complexity": "challenging questions requiring deep understanding and critical thinking",
            "examples": "Analyze this scenario, What would happen if, Complex problem-solving",
            "description": "Advanced questions requiring analysis and critical thinking"
        }
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        quiz_subject = st.text_input(
            "Quiz Subject",
            placeholder="e.g., Python Programming, Biology, Mathematics",
            help="Enter the subject for your quiz"
        )
        
        num_questions = st.number_input(
            "Number of Questions",
            min_value=3,
            max_value=10,
            value=5,
            help="Choose how many questions you want in your quiz"
        )
        
        difficulty = st.selectbox(
            "Starting Difficulty",
            ["Easy", "Medium", "Hard"],
            help="Select the initial difficulty level",
            key="difficulty_selector"
        )
        
        # Difficulty comparison tooltip
        with st.expander("📊 Difficulty Level Guide", expanded=False):
            st.markdown("""
            **🎯 Easy Level:**
            - Basic concepts and definitions
            - Simple recall questions
            - Obvious answer choices
            - Perfect for beginners
            
            **🎯 Medium Level:**
            - Understanding and application
            - Moderate reasoning required
            - Plausible but incorrect options
            - Good for intermediate learners
            
            **🎯 Hard Level:**
            - Advanced concepts and analysis
            - Critical thinking required
            - Very plausible incorrect options
            - Challenging for advanced learners
            """)
    
    with col2:
        st.markdown("""
        <div class="grid-item">
            <h4>🎯 Quiz Configuration</h4>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Questions:</strong> {questions}</p>
            <p><strong>Difficulty:</strong> {difficulty}</p>
        </div>
        """.format(subject=quiz_subject or "Not specified", questions=num_questions, difficulty=difficulty), unsafe_allow_html=True)
    
    # Quiz controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 Generate Quiz", type="primary"):
            if quiz_subject:
                with st.spinner("🤖 AI is generating your interactive quiz..."):
                    try:
                        # Initialize LLM with proper parameters
                        if provider == "Ollama":
                            llm = LLM(provider="ollama", model=model)
                        else:
                            st.error("OpenAI integration not yet implemented")
                            st.stop()
                        
                        # RAG Integration: Retrieve relevant context from knowledge base
                        rag_context = ""
                        rag_sources = []
                        if rag_system and 'rag_system' in st.session_state:
                            try:
                                # Retrieve relevant context for the quiz subject
                                rag_context, rag_sources = rag_system.retrieve_relevant_context(
                                    f"{quiz_subject} {difficulty} level quiz", 
                                    k=3
                                )
                                if rag_context:
                                    st.info(f"🔍 Found {len(rag_sources)} relevant knowledge base sources for quiz")
                            except Exception as e:
                                st.warning(f"⚠️ RAG retrieval failed: {str(e)}")
                        
                        # Create enhanced prompt using the prompt template
                        from core.prompt_templates import QuizPrompt
                        prompt_template = QuizPrompt()
                        
                        custom_prompt = prompt_template.render(
                            topic=quiz_subject,
                            level="intermediate",  # Default level, can be enhanced later
                            difficulty=difficulty,
                            num_questions=num_questions,
                            rag_context=rag_context,
                            rag_sources=rag_sources
                        )
                        
                        quiz_data = llm.complete(custom_prompt, temperature=0.7, max_tokens=2000)
                        
                        # Parse quiz data into structured format
                        questions = parse_quiz_data(quiz_data, num_questions)
                        
                        if questions:
                            # Store parsed quiz data
                            st.session_state.quiz_questions = questions
                            st.session_state.quiz_generated = True
                            st.session_state.quiz_submitted = False
            st.session_state.user_answers = {}
                            st.success("✅ Interactive quiz generated successfully!")
                            
                            # Display RAG sources if available
                            if rag_sources:
                                with st.expander("🔍 Knowledge Base Sources Used", expanded=False):
                                    st.markdown("**Sources that enhanced your quiz:**")
                                    for i, source in enumerate(rag_sources, 1):
                                        st.markdown(f"""
                                        **Source {i}:** {source['source']}
                                        - Relevance: {source['relevance_score']:.2f}
                                        - Chunk ID: {source['chunk_id']}
                                        """)
                        else:
                            st.error("❌ Failed to parse quiz data. Please try again.")
                        
        except Exception as e:
                        st.error(f"❌ Error generating quiz: {str(e)}")
            else:
                st.warning("⚠️ Please enter a quiz subject.")
    
    with col2:
        if st.button("📝 Submit Quiz", type="secondary", disabled=not st.session_state.get('quiz_generated', False)):
            if 'quiz_questions' in st.session_state and st.session_state.get('user_answers'):
                # Grade the quiz
                score, results = grade_quiz(st.session_state.quiz_questions, st.session_state.user_answers)
                st.session_state.quiz_score = score
                st.session_state.quiz_results = results
                st.session_state.quiz_submitted = True
                st.success(f"✅ Quiz submitted! Score: {score}%")
            else:
                st.warning("⚠️ Please answer all questions before submitting.")
    
    with col3:
        if st.button("🗑️ Clear Quiz", type="secondary"):
            # Clear all quiz-related session state
            for key in ['quiz_questions', 'quiz_generated', 'quiz_submitted', 'user_answers', 'quiz_score', 'quiz_results']:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("✅ Quiz cleared!")
    
    # Display interactive quiz if generated
    if st.session_state.get('quiz_generated', False) and 'quiz_questions' in st.session_state:
        # Difficulty indicator with color coding
        difficulty_colors = {
            "Easy": "#10b981",      # Green
            "Medium": "#f59e0b",    # Orange
            "Hard": "#ef4444"       # Red
        }
        
        difficulty_color = difficulty_colors.get(difficulty, "#6b7280")
        
        st.markdown(f"""
        <div class="content-card">
            <h3>📝 Quiz: {quiz_subject}</h3>
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <p><strong>Questions:</strong> {num_questions}</p>
                <div style="
                    background: {difficulty_color}; 
                    color: white; 
                    padding: 0.5rem 1rem; 
                    border-radius: 20px; 
                    font-weight: 700;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    🎯 {difficulty} Level
                </div>
            </div>
            <div style="
                background: linear-gradient(135deg, {difficulty_color}20 0%, {difficulty_color}10 100%);
                border-left: 4px solid {difficulty_color};
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
            ">
                <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem;">
                    <strong>Difficulty Focus:</strong> {difficulty_guidelines[difficulty]['description']}
                </p>
            </div>
        </div>
        """.format(quiz_subject=quiz_subject, num_questions=num_questions, difficulty=difficulty, difficulty_colors=difficulty_colors, difficulty_guidelines=difficulty_guidelines), unsafe_allow_html=True)
        
        # Display interactive quiz questions
        if 'quiz_questions' in st.session_state:
            questions = st.session_state.quiz_questions
            
            for i, question_data in enumerate(questions, 1):
                st.markdown(f"""
                <div class="grid-item" style="margin-bottom: 2rem;">
                    <h4 style="color: #ff6b6b; margin-bottom: 1rem;">Question {i}</h4>
                    <p style="color: #ffffff; font-size: 1.1rem; margin-bottom: 1.5rem;">{question_data['question']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create radio buttons for options
                options = question_data['options']
                user_answer = st.radio(
                    f"Select your answer for Question {i}:",
                    options,
                    key=f"q{i}",
                    label_visibility="collapsed"
                )
                
                # Store user's answer
                st.session_state.user_answers[i] = user_answer
                
                st.markdown("<hr style='margin: 2rem 0; border-color: #404040;'>", unsafe_allow_html=True)
    
    # Display results if quiz was submitted
    if st.session_state.get('quiz_submitted', False) and 'quiz_results' in st.session_state:
        st.markdown("""
        <div class="content-card">
            <h3>🎯 Quiz Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display score
        score = st.session_state.quiz_score
        st.markdown(f"""
        <div class="grid-item" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); text-align: center; margin-bottom: 2rem;">
            <h4 style="color: white; font-size: 2rem; margin-bottom: 1rem;">🎯 Your Score</h4>
            <div style="font-size: 4rem; font-weight: 900; color: white; margin-bottom: 1rem;">{score}%</div>
            <p style="color: white; opacity: 0.9;">{get_score_message(score)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display detailed results
        results = st.session_state.quiz_results
        for i, result in enumerate(results, 1):
            question_data = st.session_state.quiz_questions[i-1]
            user_answer = st.session_state.user_answers.get(i, "Not answered")
            user_answer_letter = result.get('user_answer_letter', '?')
            correct_answer_letter = result.get('correct_answer_letter', '?')
            is_correct = result['correct']
            
            # Get the full text for the correct answer
            correct_answer_text = "Unknown"
            if correct_answer_letter and correct_answer_letter in ['A', 'B', 'C', 'D']:
                idx = ord(correct_answer_letter) - 65  # Convert A,B,C,D to 0,1,2,3
                if 0 <= idx < len(question_data['options']):
                    correct_answer_text = question_data['options'][idx]
            
            # Color coding for correct/incorrect answers
            status_color = "#10b981" if is_correct else "#ef4444"
            status_icon = "✅" if is_correct else "❌"
            
            st.markdown(f"""
            <div class="grid-item" style="border-left: 4px solid {status_color};">
                <h4 style="color: {status_color}; margin-bottom: 1rem;">{status_icon} Question {i}</h4>
                <p style="color: #ffffff; margin-bottom: 1rem;"><strong>Question:</strong> {question_data['question']}</p>
                <p style="color: #e2e8f0; margin-bottom: 0.5rem;"><strong>Your Answer:</strong> {user_answer} ({user_answer_letter})</p>
                <p style="color: #10b981; margin-bottom: 0.5rem;"><strong>Correct Answer:</strong> {correct_answer_text} ({correct_answer_letter})</p>
                <p style="color: #4ecdc4; margin-bottom: 0;"><strong>Explanation:</strong> {question_data['explanation']}</p>
                
                <!-- Debug information -->
                <details style="margin-top: 1rem; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 8px;">
                    <summary style="color: #808080; cursor: pointer; font-size: 0.9rem;">🔍 Debug Info</summary>
                    <div style="font-size: 0.8rem; color: #808080; margin-top: 0.5rem;">
                        <p><strong>Raw User Answer:</strong> "{user_answer}"</p>
                        <p><strong>Raw Correct Answer:</strong> "{correct_answer_letter}"</p>
                        <p><strong>Options:</strong> {question_data['options']}</p>
                        <p><strong>Mapped User Letter:</strong> {user_answer_letter}</p>
                        <p><strong>Comparison:</strong> {user_answer_letter} == {correct_answer_letter} = {is_correct}</p>
                    </div>
                </details>
            </div>
            """, unsafe_allow_html=True)

# Progress Tracker Tab
with tab4:
    st.markdown("""
    <div class="content-card">
        <h3>📊 Learning Progress Dashboard</h3>
        <p>Track your learning journey, monitor achievements, and analyze your study patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize progress tracking in session state
    if 'study_sessions' not in st.session_state:
        st.session_state.study_sessions = []
    if 'completed_topics' not in st.session_state:
        st.session_state.completed_topics = []
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Log Study Session")
        
        session_subject = st.text_input(
            "Subject/Topic",
            placeholder="e.g., Calculus, Python Programming",
            key="session_subject"
        )
        
        session_duration = st.number_input(
            "Duration (minutes)",
            min_value=15,
            max_value=480,
            value=60,
            step=15,
            key="session_duration"
        )
        
        session_activities = st.multiselect(
            "Activities Completed",
            ["Reading", "Practice Problems", "Quiz", "Project Work", "Review", "Note-taking"],
            key="session_activities"
        )
        
        session_notes = st.text_area(
            "Session Notes",
            placeholder="What did you learn? Any challenges?",
            key="session_notes"
        )
        
        if st.button("💾 Save Session", type="primary"):
            if session_subject:
                from datetime import datetime
                
                new_session = {
                    "subject": session_subject,
                    "duration": session_duration,
                    "activities": session_activities,
                    "notes": session_notes,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.study_sessions.append(new_session)
                st.success(f"✅ Study session saved! Total time: {session_duration} minutes")
                
                # Note: Form will be cleared on next page refresh
            else:
                st.warning("⚠️ Please enter a subject for your study session.")
    
    with col2:
        st.markdown("### 🎯 Quick Stats")
        
        total_sessions = len(st.session_state.study_sessions)
        total_time = sum(session["duration"] for session in st.session_state.study_sessions)
        unique_subjects = len(set(session["subject"] for session in st.session_state.study_sessions))
        
        st.metric("Total Sessions", total_sessions)
        st.metric("Total Study Time", f"{total_time} min")
        st.metric("Subjects Studied", unique_subjects)
        
        if total_time > 0:
            avg_session = total_time / total_sessions
            st.metric("Avg Session Length", f"{avg_session:.1f} min")
    
    # Progress Analytics
    if st.session_state.study_sessions:
        st.markdown("### 📈 Progress Analytics")
        
        # Study time by subject
        subject_time = {}
        for session in st.session_state.study_sessions:
            subject = session["subject"]
            if subject not in subject_time:
                subject_time[subject] = 0
            subject_time[subject] += session["duration"]
        
        if subject_time:
            st.markdown("#### ⏱️ Study Time by Subject")
            for subject, time in sorted(subject_time.items(), key=lambda x: x[1], reverse=True):
                hours = time / 60
                st.markdown(f"""
                <div class="grid-item" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; color: #ffffff;">{subject}</span>
                        <span style="color: #4ecdc4; font-weight: 700;">{hours:.1f}h</span>
                    </div>
                    <div style="background: #404040; height: 8px; border-radius: 4px; margin-top: 0.5rem;">
                        <div style="background: linear-gradient(90deg, #ff6b6b, #4ecdc4); height: 100%; border-radius: 4px; width: {min(100, (time / max(subject_time.values())) * 100)}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent sessions
        st.markdown("#### 📅 Recent Study Sessions")
        recent_sessions = st.session_state.study_sessions[-5:]  # Last 5 sessions
        
        for session in reversed(recent_sessions):
            st.markdown(f"""
            <div class="grid-item" style="margin-bottom: 1rem; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <h5 style="color: #ff6b6b; margin: 0;">{session['subject']}</h5>
                    <span style="color: #4ecdc4; font-size: 0.9rem;">{session['timestamp']}</span>
                </div>
                <p style="color: #e2e8f0; margin: 0.5rem 0; font-size: 0.9rem;">
                    <strong>Duration:</strong> {session['duration']} minutes
                </p>
                <p style="color: #cbd5e1; margin: 0.5rem 0; font-size: 0.9rem;">
                    <strong>Activities:</strong> {', '.join(session['activities'])}
                </p>
                {f"<p style='color: #a0aec0; margin: 0.5rem 0; font-size: 0.9rem;'><strong>Notes:</strong> {session['notes']}</p>" if session['notes'] else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Quiz History
    if st.session_state.get('quiz_history'):
        st.markdown("### 🧠 Quiz Performance History")
        
        for quiz in st.session_state.quiz_history:
            st.markdown(f"""
            <div class="grid-item" style="margin-bottom: 1rem; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h5 style="color: #4ecdc4; margin: 0;">{quiz['subject']}</h5>
                    <span style="color: #ff6b6b; font-weight: 700; font-size: 1.2rem;">{quiz['score']}%</span>
                </div>
                <p style="color: #e2e8f0; margin: 0.5rem 0; font-size: 0.9rem;">
                    <strong>Difficulty:</strong> {quiz['difficulty']} | <strong>Questions:</strong> {quiz['total_questions']}
                </p>
                <p style="color: #cbd5e1; margin: 0.5rem 0; font-size: 0.9rem;">
                    <strong>Date:</strong> {quiz['date']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Export Progress
    if st.session_state.study_sessions:
        st.markdown("### 📤 Export Progress")
        
        import json
        progress_data = {
            "study_sessions": st.session_state.study_sessions,
            "completed_topics": st.session_state.completed_topics,
            "quiz_history": st.session_state.get('quiz_history', []),
            "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.download_button(
            label="📥 Download Progress Report (JSON)",
            data=json.dumps(progress_data, indent=2),
            file_name=f"smartlearn_progress_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
        
        # Clear all data button
        if st.button("🗑️ Clear All Progress Data", type="secondary"):
            st.session_state.study_sessions = []
            st.session_state.completed_topics = []
            st.session_state.quiz_history = []
            st.success("✅ All progress data cleared!")
            st.rerun()

# Professional footer
st.markdown("""
<div style="background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 100%); color: white; padding: 3rem 0; margin: 4rem -1rem -1rem -1rem; text-align: center; border-radius: 3rem 3rem 0 0;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; text-align: left;">
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 1.2rem; font-weight: 700; color: #ff6b6b;">🚀 SmartLearn Pro</h4>
                <p style="opacity: 0.8; line-height: 1.6;">Ultra-professional AI-powered study assistant designed for serious learners and educational institutions.</p>
            </div>
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 1.2rem; font-weight: 700; color: #4ecdc4;">🔧 Technology</h4>
                <p style="opacity: 0.8; line-height: 1.6;">Built with Streamlit, powered by advanced LLM technology including Ollama and OpenAI integration.</p>
            </div>
            <div>
                <h4 style="margin-bottom: 1rem; font-size: 1.2rem; font-weight: 700; color: #45b7d1;">📚 Features</h4>
                <p style="opacity: 0.8; line-height: 1.6;">Personalized study plans, AI explanations, interactive quizzes, and RAG-powered knowledge base integration.</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True) 
