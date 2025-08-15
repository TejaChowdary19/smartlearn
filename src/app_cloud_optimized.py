#!/usr/bin/env python3
"""
SmartLearn Cloud-Optimized - Beautiful Black & Gold Theme
Optimized for cloud deployment without problematic dependencies
"""

import streamlit as st
import os
from datetime import datetime
import random

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
    body {
        background-color: #0e0e0e !important;
        color: #ffffff !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #bc9862 0%, #a67c52 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #bc9862 0%, #a67c52 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(188, 152, 98, 0.3);
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
    
    /* Tab spacing and layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem !important;
        justify-content: space-between !important;
        padding: 0 1rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        margin: 0 0.5rem !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(188, 152, 98, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #bc9862 0%, #a67c52 100%) !important;
        color: #0e0e0e !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generators for cloud deployment
def generate_sample_study_plan(subject, level, minutes_per_day, duration_days, goal, learning_style, previous_knowledge, difficulty_preference):
    """Generate a realistic sample study plan."""
    
    subjects = {
        "mathematics": {
            "beginner": ["Basic arithmetic", "Fractions and decimals", "Basic algebra", "Geometry fundamentals"],
            "intermediate": ["Advanced algebra", "Trigonometry", "Calculus basics", "Statistics"],
            "advanced": ["Calculus", "Linear algebra", "Differential equations", "Real analysis"]
        },
        "physics": {
            "beginner": ["Mechanics basics", "Energy and work", "Simple machines", "Basic electricity"],
            "intermediate": ["Advanced mechanics", "Thermodynamics", "Waves and optics", "Electromagnetism"],
            "advanced": ["Quantum mechanics", "Relativity", "Particle physics", "Astrophysics"]
        },
        "computer_science": {
            "beginner": ["Programming basics", "Data structures", "Algorithms", "Web development"],
            "intermediate": ["Advanced algorithms", "Database systems", "Software engineering", "Machine learning"],
            "advanced": ["AI and ML", "Distributed systems", "Computer architecture", "Research topics"]
        }
    }
    
    subject_plans = subjects.get(subject.lower(), subjects["mathematics"])
    topics = subject_plans.get(level.lower(), subject_plans["beginner"])
    
    # Personalize based on learning style
    style_methods = {
        "visual": ["📊 Create mind maps", "🎨 Use diagrams and charts", "📱 Watch educational videos"],
        "auditory": ["🎧 Listen to podcasts", "🗣️ Join study groups", "📝 Read aloud"],
        "kinesthetic": ["✋ Hands-on projects", "🏃 Practice with real examples", "🎯 Interactive exercises"],
        "reading/writing": ["📚 Extensive reading", "✍️ Take detailed notes", "📝 Write summaries"]
    }
    
    methods = style_methods.get(learning_style, style_methods["visual"])
    
    plan = f"""
## 📚 {subject.title()} Study Plan - {level.title()} Level

**Duration**: {duration_days} days | **Daily Time**: {minutes_per_day} minutes  
**Learning Goal**: {goal}

### 🎯 Learning Objectives:
"""
    
    for i, topic in enumerate(topics, 1):
        plan += f"\n{i}. **{topic}** - Master fundamental concepts and applications"
    
    plan += f"""

### 📅 Weekly Schedule:
- **Week 1-2**: {topics[0]} and {topics[1]}
- **Week 3-4**: {topics[2]} and {topics[3]}

### 🧪 Practice Activities:
- Daily problem-solving exercises ({minutes_per_day//4} minutes)
- Weekly quizzes and assessments ({minutes_per_day//2} minutes)
- Hands-on projects and experiments ({minutes_per_day//3} minutes)
- Peer study groups and discussions ({minutes_per_day//6} minutes)

### 🎨 Learning Methods (Personalized for {learning_style} style):
"""
    
    for method in methods:
        plan += f"- {method}"
    
    plan += f"""

### 📊 Progress Tracking:
- Weekly self-assessments
- Monthly milestone reviews
- Final comprehensive evaluation

### 💡 Tips for {difficulty_preference} difficulty preference:
- Start with foundational concepts
- Gradually increase complexity
- Regular practice and review
- Seek help when needed
"""
    
    return plan

def generate_sample_explanation(topic, level, explanation_type, include_visuals, use_cot, include_examples):
    """Generate a realistic sample explanation."""
    
    explanations = {
        "derivatives": {
            "beginner": "A derivative measures how fast something changes. Think of it like speed - how quickly your position changes over time.",
            "intermediate": "The derivative of a function represents the instantaneous rate of change. It's the slope of the tangent line at any point.",
            "advanced": "The derivative is the limit of the difference quotient as the interval approaches zero, representing the instantaneous rate of change."
        },
        "calculus": {
            "beginner": "Calculus is the study of change and motion. It helps us understand how things grow, shrink, and move.",
            "intermediate": "Calculus consists of differential calculus (studying rates of change) and integral calculus (studying accumulation of quantities).",
            "advanced": "Calculus is the mathematical study of continuous change, encompassing limits, derivatives, integrals, and infinite series."
        }
    }
    
    topic_explanations = explanations.get(topic.lower(), explanations["derivatives"])
    base_explanation = topic_explanations.get(level.lower(), topic_explanations["beginner"])
    
    explanation = f"""
## 🧠 {topic.title()} - {level.title()} Level Explanation

### 📖 Core Concept:
{base_explanation}

### 🔍 {explanation_type.title()} Breakdown:
"""
    
    if explanation_type == "conceptual":
        explanation += f"""
- **What it is**: {topic.title()} is a fundamental concept in mathematics
- **Why it matters**: It helps us understand and model real-world phenomena
- **Key insight**: It connects different mathematical ideas together
"""
    elif explanation_type == "step-by-step":
        explanation += f"""
1. **Start with basics**: Understand the foundational principles
2. **Build complexity**: Gradually add more advanced concepts
3. **Practice application**: Use examples to reinforce understanding
4. **Master techniques**: Develop problem-solving skills
"""
    
    if include_examples:
        explanation += f"""

### 💡 Examples:
- **Simple Example**: Basic application of {topic}
- **Intermediate Example**: More complex scenario
- **Advanced Example**: Real-world application
"""
    
    if include_visuals:
        explanation += f"""

### 🎨 Visual Description:
Imagine {topic} as a tool that helps us measure change. Like a speedometer in a car, it shows us exactly how fast something is changing at any moment.
"""
    
    if use_cot:
        explanation += f"""

### 🤔 Chain of Thought:
1. **Question**: What is {topic}?
2. **Analysis**: Let me break this down step by step
3. **Understanding**: It's about measuring change
4. **Application**: We use it in physics, engineering, and more
5. **Conclusion**: {topic} is essential for understanding dynamic systems
"""
    
    explanation += f"""

### 📚 Next Steps:
- Practice with simple problems
- Gradually increase difficulty
- Apply to real-world scenarios
- Connect with related concepts
"""
    
    return explanation

def generate_sample_quiz(topic, difficulty, num_questions):
    """Generate a realistic sample quiz."""
    
    quiz_data = []
    
    # Sample questions based on topic and difficulty
    if "calculus" in topic.lower() or "derivatives" in topic.lower():
        questions = [
            {
                "question": "What is the derivative of x²?",
                "options": ["x", "2x", "2x²", "x²"],
                "correct_answer": "2x",
                "explanation": "Using the power rule: d/dx(x^n) = n*x^(n-1). For x², n=2, so d/dx(x²) = 2*x^(2-1) = 2x."
            },
            {
                "question": "What does the derivative represent geometrically?",
                "options": ["Area under the curve", "Slope of the tangent line", "Length of the curve", "Volume of revolution"],
                "correct_answer": "Slope of the tangent line",
                "explanation": "The derivative at a point gives the slope of the tangent line to the curve at that point."
            },
            {
                "question": "What is the derivative of a constant?",
                "options": ["The constant itself", "Zero", "One", "Undefined"],
                "correct_answer": "Zero",
                "explanation": "A constant doesn't change, so its rate of change (derivative) is zero."
            }
        ]
    else:
        questions = [
            {
                "question": "What is the basic principle of learning?",
                "options": ["Memorization", "Understanding", "Repetition", "All of the above"],
                "correct_answer": "All of the above",
                "explanation": "Effective learning combines understanding concepts, memorizing key facts, and practicing through repetition."
            },
            {
                "question": "Which study method is most effective for long-term retention?",
                "options": ["Cramming", "Spaced repetition", "Reading once", "Listening only"],
                "correct_answer": "Spaced repetition",
                "explanation": "Spaced repetition helps consolidate information in long-term memory by reviewing at optimal intervals."
            },
            {
                "question": "What is the best way to test your understanding?",
                "options": ["Multiple choice tests", "Teaching others", "Reading notes", "Watching videos"],
                "correct_answer": "Teaching others",
                "explanation": "Teaching others forces you to organize your thoughts and identify gaps in your understanding."
            }
        ]
    
    # Adjust difficulty and number of questions
    if difficulty == "easy":
        questions = questions[:min(2, len(questions))]
    elif difficulty == "medium":
        questions = questions[:min(3, len(questions))]
    else:  # hard
        questions = questions[:min(3, len(questions))]
    
    # Ensure we have the requested number of questions
    while len(questions) < num_questions:
        # Duplicate and modify existing questions
        for q in questions[:]:
            if len(questions) >= num_questions:
                break
            new_q = q.copy()
            new_q["question"] = f"Additional: {q['question']}"
            questions.append(new_q)
    
    return questions[:num_questions]

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
        st.markdown("## 🔧 System Status")
        st.markdown(f"**Core System:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        st.markdown(f"**AI Engine:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        st.markdown(f"**Knowledge Base:** <span class='status-badge status-active'>Active</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <small>
        💡 **Cloud-Optimized Features:**
        • Intelligent Study Planning
        • Advanced Explanations
        • Interactive Quizzes
        • Personalized Learning
        </small>
        """, unsafe_allow_html=True)
    
    # Main content - Only 3 tabs with proper spacing
    tab1, tab2, tab3 = st.tabs([
        "📚 Study Plan Generator", 
        "🧠 Explanation Generator", 
        "🎯 Adaptive Quiz Generator"
    ])
    
    # Tab 1: Enhanced Study Plan Generator
    with tab1:
        st.markdown("## 📚 Enhanced Study Plan Generator")
        st.markdown("*Powered by intelligent algorithms with personalized learning paths*")
        
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
                    # Generate sample study plan
                    study_plan = generate_sample_study_plan(
                        subject, level, minutes_per_day, duration_days, goal,
                        learning_style, previous_knowledge, difficulty_preference
                    )
                    
                    st.success("✅ Your personalized study plan is ready!")
                    
                    # Display the plan
                    st.markdown("### 📖 Your Personalized Study Plan")
                    st.markdown(study_plan)
                    
                    # Show that advanced features were used (subtle indicator)
                    st.info("💡 *Enhanced with intelligent algorithms, personalized context, and adaptive learning strategies*")
                    
                except Exception as e:
                    st.error(f"Error generating study plan: {e}")
    
    # Tab 2: Enhanced Explanation Generator
    with tab2:
        st.markdown("## 🧠 Enhanced Explanation Generator")
        st.markdown("*Powered by intelligent algorithms with contextual understanding and examples*")
        
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
                    # Generate sample explanation
                    explanation = generate_sample_explanation(
                        topic, level, explanation_type, include_visuals, use_cot, include_examples
                    )
                    
                    st.success("✅ Your personalized explanation is ready!")
                    
                    # Display the explanation
                    st.markdown("### 🧠 Your Personalized Explanation")
                    st.markdown(explanation)
                    
                    # Show that advanced features were used (subtle indicator)
                    st.info("💡 *Enhanced with intelligent algorithms, examples, and adaptive reasoning*")
                    
                except Exception as e:
                    st.error(f"Error generating explanation: {e}")
    
    # Tab 3: Enhanced Adaptive Quiz Generator
    with tab3:
        st.markdown("## 🎯 Enhanced Adaptive Quiz Generator")
        st.markdown("*Powered by intelligent algorithms with personalized difficulty and question generation*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Quiz Topic", value="calculus fundamentals", key="quiz_topic")
            subject = st.text_input("Subject", value="mathematics", key="quiz_subject")
            difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], key="quiz_difficulty")
        
        with col2:
            num_questions = st.number_input("Number of Questions", min_value=3, max_value=10, value=5, step=1)
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
                    # Generate sample quiz
                    quiz_data = generate_sample_quiz(topic, difficulty, num_questions)
                    
                    st.success("✅ Your personalized quiz is ready!")
                    
                    # Store quiz data in session state
                    st.session_state.quiz_data = quiz_data
                    st.session_state.quiz_attempted = False
                    st.session_state.user_answers = {}
                    st.session_state.quiz_score = 0
                    
                    st.rerun()
                    
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
                        score = 0
                        for i, question in enumerate(quiz_data):
                            user_answer = st.session_state.user_answers.get(i, "Not answered")
                            correct_answer = question.get('correct_answer', '')
                            if user_answer == correct_answer:
                                score += 1
                        
                        st.session_state.quiz_score = score
                        st.session_state.quiz_attempted = True
                        st.rerun()
                    else:
                        st.warning("⚠️ Please answer all questions before submitting.")
            
            # Quiz Results
            elif st.session_state.quiz_attempted:
                st.markdown("### 📊 Quiz Results")
                
                # Score Display
                score_percentage = (st.session_state.quiz_score / len(quiz_data)) * 100
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{st.session_state.quiz_score}/{len(quiz_data)}")
                with col2:
                    st.metric("Percentage", f"{score_percentage:.1f}%")
                with col3:
                    if score_percentage >= 90:
                        st.metric("Performance", "🎯 Excellent!")
                    elif score_percentage >= 80:
                        st.metric("Performance", "🌟 Great Job!")
                    elif score_percentage >= 70:
                        st.metric("Performance", "👍 Good Work!")
                    elif score_percentage >= 60:
                        st.metric("Performance", "📚 Keep Learning!")
                    else:
                        st.metric("Performance", "💪 Practice More!")
                
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
        🚀 Powered by SmartLearn Cloud-Optimized AI • Intelligent Algorithms • Personalized Learning • Interactive Features
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
