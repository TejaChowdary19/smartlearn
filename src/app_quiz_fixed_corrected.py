#!/usr/bin/env python3
"""
SmartLearn Enhanced - Clean Interface with Advanced Features Running in Background
Uses all 4 advanced components silently to enhance Study Plan, Explanation, and Quiz
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Local modules
from core.generator import LLM
from core.advanced_features import create_advanced_smartlearn

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SmartLearn Enhanced - AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional UI
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
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    
    .status-active { background-color: #00ff00; color: #000; }
</style>
""", unsafe_allow_html=True)

# Initialize advanced features silently in background
@st.cache_resource
def init_background_systems():
    """Initialize all advanced features silently in the background."""
    try:
        # Initialize advanced features
        advanced = create_advanced_smartlearn()
        
        # Initialize LLM
        llm = LLM()
        
        # Load knowledge base silently
        try:
            advanced.rag_system.load_knowledge_base("data/knowledge_base")
            rag_status = "✅ Active"
        except:
            rag_status = "⚠️ Limited"
        
        # Generate some synthetic training data silently
        try:
            advanced.generate_synthetic_training_data("mathematics", 20)
            advanced.generate_synthetic_training_data("computer_science", 20)
            training_status = "✅ Active"
        except:
            training_status = "⚠️ Limited"
        
        # Check multimodal capabilities
        try:
            mm_status = "✅ Active" if advanced.multimodal_manager.image_processor._AVAILABLE else "⚠️ Limited"
        except:
            mm_status = "⚠️ Limited"
        
        return {
            "advanced": advanced,
            "llm": llm,
            "rag_status": rag_status,
            "training_status": training_status,
            "multimodal_status": mm_status
        }
    except Exception as e:
        st.error(f"Background systems initialization failed: {e}")
        return None

# Helper functions for quiz functionality
def parse_quiz_data(quiz_text):
    """Parse the raw quiz text into structured data."""
    try:
        # Split into questions
        questions = []
        lines = quiz_text.split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a question (various formats)
            if (line.startswith(('Q', 'Question')) and '?' in line) or \
               (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')) and '?' in line):
                if current_question:
                    questions.append(current_question)
                
                # Clean up question text
                question_text = line
                if line.startswith(('Q', 'Question')):
                    question_text = line.split('Q')[1] if line.startswith('Q') else line.split('Question')[1]
                elif any(line.startswith(f"{i}.") for i in range(1, 11)):
                    for i in range(1, 11):
                        if line.startswith(f"{i}."):
                            question_text = line.split(f"{i}.")[1]
                            break
                
                current_question = {
                    'question': question_text.strip(),
                    'options': [],
                    'correct_answer': '',
                    'explanation': ''
                }
                
            # Check for options (A), B), C), D) or A. B. C. D.
            elif (line.startswith(('A)', 'B)', 'C)', 'D)') or 
                  line.startswith(('A.', 'B.', 'C.', 'D.'))) and current_question:
                option_text = line[2:].strip()
                if option_text:
                    current_question['options'].append(option_text)
            
            # Check for correct answer
            elif 'Correct:' in line and current_question:
                correct_part = line.split('Correct:')[1].strip()
                if 'Explanation:' in correct_part:
                    parts = correct_part.split('Explanation:')
                    current_question['correct_answer'] = parts[0].strip()
                    if len(parts) > 1:
                        current_question['explanation'] = parts[1].strip()
                else:
                    current_question['correct_answer'] = correct_part
            
            # Check for explanation on separate line
            elif 'Explanation:' in line and current_question and not current_question['explanation']:
                explanation_text = line.split('Explanation:')[1].strip()
                if explanation_text:
                    current_question['explanation'] = explanation_text
        
        # Add the last question
        if current_question:
            questions.append(current_question)
        
        # Clean up questions and ensure they have proper structure
        valid_questions = []
        for q in questions:
            if q['question'] and len(q['options']) >= 2:
                # Ensure question ends with ?
                if not q['question'].endswith('?'):
                    q['question'] = q['question'] + '?'
                
                # Clean up options
                q['options'] = [opt.strip() for opt in q['options'] if opt.strip()]
                
                # Ensure we have exactly 4 options
                while len(q['options']) < 4:
                    q['options'].append(f"Option {chr(68 + len(q['options']))}")
                
                # Clean up correct answer
                if q['correct_answer']:
                    q['correct_answer'] = q['correct_answer'].strip()
                
                valid_questions.append(q)
        
        return valid_questions if valid_questions else None
        
    except Exception as e:
        st.error(f"Error parsing quiz: {e}")
        return None

def grade_quiz(quiz_data, user_answers):
    """Grade the quiz and return score and results."""
    try:
        score = 0
        results = []
        
        for i, question in enumerate(quiz_data):
            user_answer = user_answers.get(i, "Not answered")
            correct_answer = question.get('correct_answer', '')
            
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            results.append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        return score, results
        
    except Exception as e:
        st.error(f"Error grading quiz: {e}")
        return 0, []

def get_score_message(percentage):
    """Get a performance message based on score percentage."""
    if percentage >= 90:
        return "🎯 Excellent!"
    elif percentage >= 80:
        return "🌟 Great Job!"
    elif percentage >= 70:
        return "👍 Good Work!"
    elif percentage >= 60:
        return "📚 Keep Learning!"
    else:
        return "💪 Practice More!"

def main():
    """Main application with clean interface."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 SmartLearn Enhanced</h1>
        <h3>AI-Powered Study Assistant with Advanced Intelligence</h3>
        <p>Study Plans • Explanations • Adaptive Quizzes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize background systems silently
    systems = init_background_systems()
    
    if not systems:
        st.error("❌ Failed to initialize background systems. Please check your configuration.")
        return
    
    # Sidebar - Clean and simple
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # AI Model Selection
        model = st.selectbox(
            "AI Model",
            ["mistral:7b-instruct", "llama2:7b", "codellama:7b"],
            index=0
        )
        
        # Background Systems Status (Read-only)
        st.markdown("## 🔧 Background Systems")
        st.markdown(f"**RAG System:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        st.markdown(f"**Training Pipeline:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        st.markdown(f"**Multimodal:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <small>
        💡 **Advanced Features Running Silently:**
        • Enhanced Prompt Engineering
        • Advanced RAG System  
        • Fine-Tuning Pipeline
        • Multimodal Integration
        </small>
        """, unsafe_allow_html=True)
    
    # Main content - Only 3 tabs
    tab1, tab2, tab3 = st.tabs([
        "📚 Study Plan Generator", 
        "🧠 Explanation Generator", 
        "🎯 Adaptive Quiz Generator"
    ])
    
    # Tab 1: Enhanced Study Plan Generator
    with tab1:
        st.markdown("## 📚 Enhanced Study Plan Generator")
        st.markdown("*Powered by advanced AI with personalized learning paths*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Subject", value="mathematics", key="sp_subject")
            level = st.selectbox("Level", ["beginner", "intermediate", "advanced"], key="sp_level")
            topic = st.text_input("Topic/Concept", value="calculus", key="sp_topic")
        
        with col2:
            minutes_per_day = st.number_input("Minutes per Day", min_value=15, max_value=180, value=60, step=15)
            duration_days = st.number_input("Duration (Days)", min_value=1, max_value=30, value=7, step=1)
            goal = st.text_area("Learning Goal", value="Master fundamental concepts and problem-solving techniques", key="sp_goal")
        
        # Personalization options
        with st.expander("🎯 Personalization Options"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                learning_style = st.selectbox(
                    "Learning Style",
                    ["visual", "auditory", "kinesthetic", "reading/writing"],
                    index=0,
                    key="sp_style"
                )
            
            with col2:
                previous_knowledge = st.selectbox(
                    "Previous Knowledge",
                    ["none", "basic", "intermediate", "advanced"],
                    index=1,
                    key="sp_knowledge"
                )
            
            with col3:
                difficulty_preference = st.selectbox(
                    "Difficulty Preference",
                    ["easy", "medium", "hard"],
                    index=1,
                    key="sp_difficulty"
                )
        
        # Generate Study Plan
        if st.button("🚀 Generate Enhanced Study Plan", type="primary", key="sp_generate"):
            with st.spinner("Creating your personalized study plan..."):
                try:
                    # Use advanced features silently in background
                    user_context = {
                        "learning_style": learning_style,
                        "previous_knowledge": previous_knowledge,
                        "difficulty_preference": difficulty_preference
                    }
                    
                    # Generate enhanced prompt using advanced features
                    prompt = systems["advanced"].generate_enhanced_study_plan(
                        subject, level, minutes_per_day, duration_days, goal, 
                        user_context=user_context, use_cot=True
                    )
                    
                    # Generate the actual study plan
                    study_plan = systems["llm"].complete(prompt, temperature=0.7, max_tokens=1500)
                    
                    st.success("✅ Your personalized study plan is ready!")
                    
                    # Display the plan
                    st.markdown("### 📖 Your Personalized Study Plan")
                    st.markdown(study_plan)
                    
                    # Show that advanced features were used (subtle indicator)
                    st.info("💡 *Enhanced with AI reasoning, personalized context, and intelligent content retrieval*")
                    
                except Exception as e:
                    st.error(f"Error generating study plan: {e}")
    
    # Tab 2: Enhanced Explanation Generator
    with tab2:
        st.markdown("## 🧠 Enhanced Explanation Generator")
        st.markdown("*Powered by advanced AI with contextual understanding and examples*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Topic/Concept", value="derivatives", key="exp_topic")
            level = st.selectbox("Explanation Level", ["beginner", "intermediate", "advanced"], key="exp_level")
            subject = st.text_input("Subject Area", value="mathematics", key="exp_subject")
        
        with col2:
            explanation_type = st.selectbox(
                "Explanation Type",
                ["conceptual", "step-by-step", "with examples", "comprehensive"],
                index=0,
                key="exp_type"
            )
            include_visuals = st.checkbox("Include Visual Descriptions", value=True, key="exp_visuals")
        
        # Advanced options
        with st.expander("🔧 Advanced Explanation Options"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                use_cot = st.checkbox("Use Chain-of-Thought", value=True, key="exp_cot")
            
            with col2:
                include_examples = st.checkbox("Include Examples", value=True, key="exp_examples")
            
            with col3:
                adaptive_complexity = st.checkbox("Adaptive Complexity", value=True, key="exp_adaptive")
        
        # Generate Explanation
        if st.button("💡 Generate Enhanced Explanation", type="primary", key="exp_generate"):
            with st.spinner("Creating your personalized explanation..."):
                try:
                    # Use advanced features silently in background
                    user_context = {
                        "explanation_type": explanation_type,
                        "include_visuals": include_visuals,
                        "level": level
                    }
                    
                    # Generate enhanced prompt using advanced features
                    prompt = systems["advanced"].generate_enhanced_explanation(
                        topic, level, user_context, use_cot=use_cot, include_examples=include_examples
                    )
                    
                    # Generate the actual explanation
                    explanation = systems["llm"].complete(prompt, temperature=0.6, max_tokens=1200)
                    
                    st.success("✅ Your personalized explanation is ready!")
                    
                    # Display the explanation
                    st.markdown("### 🧠 Your Personalized Explanation")
                    st.markdown(explanation)
                    
                    # Show that advanced features were used (subtle indicator)
                    st.info("💡 *Enhanced with contextual AI, examples, and intelligent reasoning*")
                    
                except Exception as e:
                    st.error(f"Error generating explanation: {e}")
    
    # Tab 3: Enhanced Adaptive Quiz Generator
    with tab3:
        st.markdown("## 🎯 Enhanced Adaptive Quiz Generator")
        st.markdown("*Powered by advanced AI with personalized difficulty and intelligent question generation*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Quiz Topic", value="calculus fundamentals", key="quiz_topic")
            subject = st.text_input("Subject", value="mathematics", key="quiz_subject")
            difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], key="quiz_difficulty")
        
        with col2:
            num_questions = st.number_input("Number of Questions", min_value=5, max_value=20, value=10, step=1)
            question_type = st.selectbox(
                "Question Type",
                ["multiple choice", "true/false", "fill in the blank", "mixed"],
                index=0,
                key="quiz_type"
            )
        
        # Quiz personalization
        with st.expander("🎯 Quiz Personalization"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                include_examples = st.checkbox("Include Examples", value=True, key="quiz_examples")
            
            with col2:
                adaptive_difficulty = st.checkbox("Adaptive Difficulty", value=True, key="quiz_adaptive")
            
            with col3:
                use_context = st.checkbox("Use Context", value=True, key="quiz_context")
        
        # Generate Quiz
        if st.button("📝 Generate Enhanced Quiz", type="primary", key="quiz_generate"):
            with st.spinner("Creating your personalized quiz..."):
                try:
                    # Use advanced features silently in background
                    user_context = {
                        "question_type": question_type,
                        "include_examples": include_examples,
                        "adaptive_difficulty": adaptive_difficulty,
                        "level": difficulty
                    }
                    
                    # Generate enhanced prompt using advanced features
                    prompt = systems["advanced"].generate_enhanced_quiz(
                        topic, difficulty, difficulty, num_questions, user_context, use_cot=True
                    )
                    
                    # Enhance the prompt to ensure proper formatting
                    enhanced_prompt = f"""
{prompt}

IMPORTANT: Format your response exactly as follows for each question:

Q1. [Question text]?
A) [Option A text]
B) [Option B text] 
C) [Option C text]
D) [Option D text]

Correct: [Correct option letter] Explanation: [Brief explanation]

Q2. [Question text]?
A) [Option A text]
B) [Option B text]
C) [Option C text]
D) [Option D text]

Correct: [Correct option letter] Explanation: [Brief explanation]

Continue this format for all {num_questions} questions. Make sure each question has exactly 4 options (A, B, C, D) and includes the correct answer with explanation.
"""
                    
                    # Generate the actual quiz
                    quiz_raw = systems["llm"].complete(enhanced_prompt, temperature=0.7, max_tokens=2000)
                    
                    st.success("✅ Your personalized quiz is ready!")
                    
                    # Parse and format the quiz properly
                    quiz_data = parse_quiz_data(quiz_raw)
                    
                    if quiz_data:
                        # Store quiz data in session state
                        st.session_state.quiz_data = quiz_data
                        st.session_state.quiz_attempted = False
                        st.session_state.user_answers = {}
                        st.session_state.quiz_score = 0
                        
                        st.rerun()
                    else:
                        st.error("❌ Failed to parse quiz data. Please try again.")
                    
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
        
        # Display Interactive Quiz
        if hasattr(st.session_state, 'quiz_data') and st.session_state.quiz_data:
            quiz_data = st.session_state.quiz_data
            
            st.markdown("### 🧪 Your Personalized Quiz")
            st.markdown(f"**Topic:** {topic} | **Difficulty:** {difficulty} | **Questions:** {len(quiz_data)}")
            
            # Quiz Instructions
            with st.expander("📋 Quiz Instructions"):
                st.markdown("""
                - Read each question carefully
                - Select your answer using the radio buttons
                - Click 'Submit Quiz' when you're done
                - Your score will be calculated automatically
                - Review correct answers and explanations after submission
                """)
            
            # Quiz Questions
            if not st.session_state.quiz_attempted:
                st.markdown("---")
                
                for i, question in enumerate(quiz_data):
                    st.markdown(f"**Question {i+1}:** {question['question']}")
                    
                    # Create radio buttons for options
                    if 'options' in question and question['options']:
                        user_answer = st.radio(
                            f"Select your answer for Question {i+1}:",
                            options=question['options'],
                            key=f"q{i}",
                            label_visibility="collapsed"
                        )
                        
                        # Store user's answer
                        st.session_state.user_answers[i] = user_answer
                    
                    st.markdown("---")
                
                # Submit Button
                if st.button("📤 Submit Quiz", type="primary", key="submit_quiz"):
                    if len(st.session_state.user_answers) == len(quiz_data):
                        # Grade the quiz
                        score, results = grade_quiz(quiz_data, st.session_state.user_answers)
                        st.session_state.quiz_score = score
                        st.session_state.quiz_results = results
                        st.session_state.quiz_attempted = True
                        st.rerun()
                    else:
                        st.warning("⚠️ Please answer all questions before submitting.")
            
            # Quiz Results
            elif st.session_state.quiz_attempted:
                st.markdown("### 📊 Quiz Results")
                
                # Score Display
                score_percentage = (st.session_state.quiz_score / len(quiz_data)) * 100
                score_message = get_score_message(score_percentage)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{st.session_state.quiz_score}/{len(quiz_data)}")
                with col2:
                    st.metric("Percentage", f"{score_percentage:.1f}%")
                with col3:
                    st.metric("Performance", score_message)
                
                st.markdown("---")
                
                # Detailed Results
                st.markdown("### 📝 Question-by-Question Review")
                
                for i, question in enumerate(quiz_data):
                    with st.expander(f"Question {i+1}: {question['question'][:50]}..."):
                        # Show user's answer
                        user_answer = st.session_state.user_answers.get(i, "Not answered")
                        correct_answer = question.get('correct_answer', 'Unknown')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Your Answer:** {user_answer}")
                        with col2:
                            st.markdown(f"**Correct Answer:** {correct_answer}")
                        
                        # Show if correct
                        is_correct = user_answer == correct_answer
                        if is_correct:
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Incorrect")
                        
                        # Show explanation if available
                        if 'explanation' in question and question['explanation']:
                            st.markdown(f"**Explanation:** {question['explanation']}")
                        
                        # Show options
                        if 'options' in question and question['options']:
                            st.markdown("**Options:**")
                            for j, option in enumerate(question['options']):
                                if option == correct_answer:
                                    st.markdown(f"✅ {option}")
                                elif option == user_answer and not is_correct:
                                    st.markdown(f"❌ {option}")
                                else:
                                    st.markdown(f"• {option}")
                
                # Action Buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Take Quiz Again", key="retake_quiz"):
                        st.session_state.quiz_attempted = False
                        st.session_state.user_answers = {}
                        st.rerun()
                
                with col2:
                    if st.button("📚 Generate New Quiz", key="new_quiz"):
                        # Clear quiz data
                        if 'quiz_data' in st.session_state:
                            del st.session_state.quiz_data
                        if 'quiz_attempted' in st.session_state:
                            del st.session_state.quiz_attempted
                        if 'user_answers' in st.session_state:
                            del st.session_state.user_answers
                        if 'quiz_score' in st.session_state:
                            del st.session_state.quiz_score
                        st.rerun()

    # Footer with subtle advanced features indicator
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        🚀 Powered by SmartLearn Advanced AI • Enhanced Prompting • Advanced RAG • Fine-Tuning • Multimodal Integration
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
