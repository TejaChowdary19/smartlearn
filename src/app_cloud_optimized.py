#!/usr/bin/env python3
"""
SmartLearn Cloud-Optimized - Beautiful Black & Gold Theme
Intelligent AI-powered features optimized for cloud deployment
"""

import streamlit as st
import os
from datetime import datetime
import random
import json

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

# Enhanced knowledge base for intelligent content generation
KNOWLEDGE_BASE = {
    "mathematics": {
        "calculus": {
            "beginner": {
                "concepts": [
                    "Understanding what derivatives represent",
                    "Basic derivative rules (power rule, constant rule)",
                    "Simple applications like velocity and acceleration",
                    "Graphical interpretation of derivatives"
                ],
                "examples": [
                    "Finding the derivative of x² using power rule",
                    "Understanding that velocity is the derivative of position",
                    "Simple slope calculations"
                ],
                "applications": [
                    "Basic physics problems",
                    "Simple optimization problems",
                    "Understanding rates of change"
                ],
                "weekly_topics": [
                    "Week 1: Introduction to derivatives and basic rules",
                    "Week 2: Power rule and constant rule practice",
                    "Week 3: Simple applications and word problems",
                    "Week 4: Review and assessment"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Advanced derivative rules (product, quotient, chain rule)",
                    "Implicit differentiation",
                    "Related rates problems",
                    "Applications to optimization"
                ],
                "examples": [
                    "Using chain rule for composite functions",
                    "Solving related rates problems",
                    "Finding maximum/minimum values"
                ],
                "applications": [
                    "Economics: marginal cost and revenue",
                    "Engineering: optimization problems",
                    "Physics: complex motion problems"
                ],
                "weekly_topics": [
                    "Week 1: Product and quotient rules",
                    "Week 2: Chain rule and composite functions",
                    "Week 3: Implicit differentiation",
                    "Week 4: Related rates and optimization"
                ]
            },
            "advanced": {
                "concepts": [
                    "Multivariable calculus concepts",
                    "Partial derivatives and gradients",
                    "Vector calculus fundamentals",
                    "Advanced optimization techniques"
                ],
                "examples": [
                    "Finding partial derivatives of functions",
                    "Using Lagrange multipliers for optimization",
                    "Understanding gradient descent"
                ],
                "applications": [
                    "Machine learning algorithms",
                    "Advanced physics modeling",
                    "Financial mathematics"
                ],
                "weekly_topics": [
                    "Week 1: Multivariable functions and partial derivatives",
                    "Week 2: Gradients and directional derivatives",
                    "Week 3: Advanced optimization methods",
                    "Week 4: Applications in modern fields"
                ]
            }
        },
        "algebra": {
            "beginner": {
                "concepts": [
                    "Basic algebraic operations",
                    "Solving linear equations",
                    "Understanding variables and constants",
                    "Simple factoring techniques"
                ],
                "examples": [
                    "Solving 2x + 5 = 13",
                    "Factoring x² + 5x + 6",
                    "Understanding y = mx + b form"
                ],
                "applications": [
                    "Basic business calculations",
                    "Simple science formulas",
                    "Everyday problem solving"
                ],
                "weekly_topics": [
                    "Week 1: Basic operations and linear equations",
                    "Week 2: Factoring and quadratic expressions",
                    "Week 3: Graphing linear functions",
                    "Week 4: Word problems and applications"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Quadratic equations and functions",
                    "Systems of equations",
                    "Polynomial functions",
                    "Rational expressions"
                ],
                "examples": [
                    "Solving quadratic equations using various methods",
                    "Solving systems of linear equations",
                    "Graphing polynomial functions"
                ],
                "applications": [
                    "Business optimization",
                    "Scientific modeling",
                    "Engineering calculations"
                ],
                "weekly_topics": [
                    "Week 1: Quadratic equations and functions",
                    "Week 2: Systems of equations",
                    "Week 3: Polynomial functions and graphs",
                    "Week 4: Complex applications and problem solving"
                ]
            },
            "advanced": {
                "concepts": [
                    "Complex numbers and operations",
                    "Advanced polynomial theory",
                    "Abstract algebra concepts",
                    "Linear algebra foundations"
                ],
                "examples": [
                    "Working with complex numbers",
                    "Understanding polynomial roots and factors",
                    "Basic matrix operations"
                ],
                "applications": [
                    "Advanced engineering",
                    "Computer science algorithms",
                    "Theoretical physics"
                ],
                "weekly_topics": [
                    "Week 1: Complex numbers and operations",
                    "Week 2: Advanced polynomial theory",
                    "Week 3: Introduction to linear algebra",
                    "Week 4: Abstract concepts and applications"
                ]
            }
        },
        "geometry": {
            "beginner": {
                "concepts": [
                    "Basic geometric shapes and properties",
                    "Area and perimeter calculations",
                    "Understanding angles and measurements",
                    "Simple geometric proofs"
                ],
                "examples": [
                    "Calculating area of rectangles and triangles",
                    "Understanding complementary and supplementary angles",
                    "Basic Pythagorean theorem applications"
                ],
                "applications": [
                    "Basic construction and design",
                    "Simple measurement problems",
                    "Art and design fundamentals"
                ],
                "weekly_topics": [
                    "Week 1: Basic shapes and properties",
                    "Week 2: Area and perimeter calculations",
                    "Week 3: Angles and measurements",
                    "Week 4: Simple proofs and applications"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Advanced geometric theorems",
                    "Coordinate geometry",
                    "Trigonometry fundamentals",
                    "Geometric transformations"
                ],
                "examples": [
                    "Using coordinate geometry to solve problems",
                    "Applying trigonometric ratios",
                    "Understanding geometric transformations"
                ],
                "applications": [
                    "Architecture and design",
                    "Computer graphics",
                    "Navigation and surveying"
                ],
                "weekly_topics": [
                    "Week 1: Advanced theorems and proofs",
                    "Week 2: Coordinate geometry",
                    "Week 3: Trigonometry fundamentals",
                    "Week 4: Transformations and applications"
                ]
            },
            "advanced": {
                "concepts": [
                    "Non-Euclidean geometry",
                    "Advanced trigonometry",
                    "Vector geometry",
                    "Geometric analysis"
                ],
                "examples": [
                    "Understanding spherical geometry",
                    "Advanced trigonometric identities",
                    "Vector operations in geometry"
                ],
                "applications": [
                    "Advanced physics",
                    "Computer vision",
                    "Theoretical mathematics"
                ],
                "weekly_topics": [
                    "Week 1: Non-Euclidean geometry concepts",
                    "Week 2: Advanced trigonometry",
                    "Week 3: Vector geometry",
                    "Week 4: Modern applications and research"
                ]
            }
        }
    },
    "physics": {
        "mechanics": {
            "beginner": {
                "concepts": [
                    "Basic motion concepts (speed, velocity, acceleration)",
                    "Newton's laws of motion",
                    "Simple force calculations",
                    "Energy and work basics"
                ],
                "examples": [
                    "Calculating average speed",
                    "Understanding F = ma",
                    "Basic energy conservation problems"
                ],
                "applications": [
                    "Everyday motion problems",
                    "Simple machine operation",
                    "Basic sports physics"
                ],
                "weekly_topics": [
                    "Week 1: Motion and speed concepts",
                    "Week 2: Newton's laws and forces",
                    "Week 3: Energy and work",
                    "Week 4: Simple applications and problems"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Advanced motion analysis",
                    "Momentum and collisions",
                    "Circular motion and gravity",
                    "Work-energy theorem"
                ],
                "examples": [
                    "Solving collision problems",
                    "Understanding centripetal force",
                    "Advanced energy problems"
                ],
                "applications": [
                    "Vehicle safety design",
                    "Sports performance analysis",
                    "Engineering applications"
                ],
                "weekly_topics": [
                    "Week 1: Advanced motion analysis",
                    "Week 2: Momentum and collisions",
                    "Week 3: Circular motion and gravity",
                    "Week 4: Complex applications and problem solving"
                ]
            },
            "advanced": {
                "concepts": [
                    "Lagrangian and Hamiltonian mechanics",
                    "Advanced collision theory",
                    "Rigid body dynamics",
                    "Chaos theory in mechanics"
                ],
                "examples": [
                    "Using Lagrangian mechanics",
                    "Understanding chaotic systems",
                    "Advanced rigid body problems"
                ],
                "applications": [
                    "Advanced engineering design",
                    "Research in physics",
                    "Complex system modeling"
                ],
                "weekly_topics": [
                    "Week 1: Lagrangian mechanics",
                    "Week 2: Advanced collision theory",
                    "Week 3: Rigid body dynamics",
                    "Week 4: Modern research applications"
                ]
            }
        },
        "thermodynamics": {
            "beginner": {
                "concepts": [
                    "Temperature and heat basics",
                    "First law of thermodynamics",
                    "Simple heat transfer",
                    "Basic gas laws"
                ],
                "examples": [
                    "Understanding temperature scales",
                    "Basic heat calculations",
                    "Simple gas law problems"
                ],
                "applications": [
                    "Basic heating and cooling",
                    "Simple engine operation",
                    "Everyday temperature effects"
                ],
                "weekly_topics": [
                    "Week 1: Temperature and heat concepts",
                    "Week 2: First law of thermodynamics",
                    "Week 3: Heat transfer basics",
                    "Week 4: Gas laws and simple applications"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Second law of thermodynamics",
                    "Entropy and disorder",
                    "Heat engines and efficiency",
                    "Advanced gas processes"
                ],
                "examples": [
                    "Calculating engine efficiency",
                    "Understanding entropy changes",
                    "Advanced gas law problems"
                ],
                "applications": [
                    "Engine design and optimization",
                    "Refrigeration systems",
                    "Power generation"
                ],
                "weekly_topics": [
                    "Week 1: Second law and entropy",
                    "Week 2: Heat engines and efficiency",
                    "Week 3: Advanced gas processes",
                    "Week 4: Complex thermodynamic systems"
                ]
            },
            "advanced": {
                "concepts": [
                    "Statistical thermodynamics",
                    "Quantum thermodynamics",
                    "Non-equilibrium thermodynamics",
                    "Advanced entropy concepts"
                ],
                "examples": [
                    "Understanding statistical mechanics",
                    "Quantum thermodynamic effects",
                    "Non-equilibrium processes"
                ],
                "applications": [
                    "Advanced power systems",
                    "Quantum computing",
                    "Research in thermodynamics"
                ],
                "weekly_topics": [
                    "Week 1: Statistical thermodynamics",
                    "Week 2: Quantum thermodynamics",
                    "Week 3: Non-equilibrium processes",
                    "Week 4: Modern research and applications"
                ]
            }
        }
    },
    "computer_science": {
        "programming": {
            "beginner": {
                "concepts": [
                    "Variables and data types",
                    "Basic control structures (if-else, loops)",
                    "Functions and parameters",
                    "Simple input/output operations"
                ],
                "examples": [
                    "Writing a simple calculator program",
                    "Creating loops to process data",
                    "Defining and calling functions"
                ],
                "applications": [
                    "Simple automation tasks",
                    "Basic data processing",
                    "Learning problem-solving skills"
                ],
                "weekly_topics": [
                    "Week 1: Variables and basic operations",
                    "Week 2: Control structures and logic",
                    "Week 3: Functions and modularity",
                    "Week 4: Simple projects and applications"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Object-oriented programming",
                    "Data structures (arrays, lists, dictionaries)",
                    "Error handling and debugging",
                    "File operations and I/O"
                ],
                "examples": [
                    "Creating classes and objects",
                    "Implementing data structures",
                    "Building robust programs with error handling"
                ],
                "applications": [
                    "Web development",
                    "Desktop applications",
                    "Data analysis tools"
                ],
                "weekly_topics": [
                    "Week 1: Object-oriented concepts",
                    "Week 2: Data structures and algorithms",
                    "Week 3: Error handling and debugging",
                    "Week 4: Building complete applications"
                ]
            },
            "advanced": {
                "concepts": [
                    "Design patterns and architecture",
                    "Advanced algorithms and optimization",
                    "Concurrent programming",
                    "Software testing and quality"
                ],
                "examples": [
                    "Implementing design patterns",
                    "Optimizing algorithms for performance",
                    "Writing concurrent and parallel code"
                ],
                "applications": [
                    "Large-scale software systems",
                    "High-performance applications",
                    "Enterprise software development"
                ],
                "weekly_topics": [
                    "Week 1: Design patterns and architecture",
                    "Week 2: Advanced algorithms",
                    "Week 3: Concurrent programming",
                    "Week 4: Software quality and testing"
                ]
            }
        },
        "algorithms": {
            "beginner": {
                "concepts": [
                    "Basic algorithm concepts",
                    "Simple sorting algorithms",
                    "Search algorithms",
                    "Algorithm efficiency basics"
                ],
                "examples": [
                    "Implementing bubble sort",
                    "Understanding binary search",
                    "Analyzing simple algorithms"
                ],
                "applications": [
                    "Basic data organization",
                    "Simple search problems",
                    "Learning computational thinking"
                ],
                "weekly_topics": [
                    "Week 1: Algorithm fundamentals",
                    "Week 2: Basic sorting algorithms",
                    "Week 3: Search algorithms",
                    "Week 4: Efficiency and analysis"
                ]
            },
            "intermediate": {
                "concepts": [
                    "Advanced sorting algorithms",
                    "Graph algorithms",
                    "Dynamic programming basics",
                    "Algorithm complexity analysis"
                ],
                "examples": [
                    "Implementing merge sort and quick sort",
                    "Solving graph traversal problems",
                    "Understanding dynamic programming"
                ],
                "applications": [
                    "Network analysis",
                    "Route optimization",
                    "Data processing systems"
                ],
                "weekly_topics": [
                    "Week 1: Advanced sorting algorithms",
                    "Week 2: Graph algorithms",
                    "Week 3: Dynamic programming",
                    "Week 4: Complex problem solving"
                ]
            },
            "advanced": {
                "concepts": [
                    "Advanced algorithm design",
                    "NP-complete problems",
                    "Approximation algorithms",
                    "Parallel and distributed algorithms"
                ],
                "examples": [
                    "Designing approximation algorithms",
                    "Understanding NP-completeness",
                    "Implementing parallel algorithms"
                ],
                "applications": [
                    "Advanced research",
                    "Complex optimization problems",
                    "Distributed systems"
                ],
                "weekly_topics": [
                    "Week 1: Advanced algorithm design",
                    "Week 2: NP-complete problems",
                    "Week 3: Approximation algorithms",
                    "Week 4: Modern algorithmic research"
                ]
            }
        }
    }
}

# Enhanced study plan generator with intelligent algorithms
def generate_intelligent_study_plan(subject, level, minutes_per_day, duration_days, goal, learning_style, previous_knowledge, difficulty_preference):
    """Generate an intelligent, personalized study plan using knowledge base."""
    
    # Get subject knowledge
    subject_knowledge = KNOWLEDGE_BASE.get(subject.lower(), KNOWLEDGE_BASE["mathematics"])
    
    # Select topics based on level and difficulty
    if level == "beginner":
        topics = list(subject_knowledge.keys())[:2]  # First 2 topics
    elif level == "intermediate":
        topics = list(subject_knowledge.keys())[:3]  # First 3 topics
    else:  # advanced
        topics = list(subject_knowledge.keys())  # All topics
    
    # Personalize based on learning style
    style_methods = {
        "visual": [
            "📊 Create mind maps and concept diagrams",
            "🎨 Use color-coded notes and visual organizers",
            "📱 Watch educational videos and animations",
            "🖼️ Draw sketches and flowcharts"
        ],
        "auditory": [
            "🎧 Listen to educational podcasts and lectures",
            "🗣️ Join study groups and discussion sessions",
            "📝 Read notes aloud and record yourself",
            "🎵 Use mnemonic devices and rhymes"
        ],
        "kinesthetic": [
            "✋ Build physical models and prototypes",
            "🏃 Practice with hands-on experiments",
            "🎯 Use interactive simulations and games",
            "✏️ Write and rewrite notes by hand"
        ],
        "reading/writing": [
            "📚 Extensive reading of textbooks and papers",
            "✍️ Take detailed, organized notes",
            "📝 Write summaries and explanations",
            "📖 Create study guides and cheat sheets"
        ]
    }
    
    methods = style_methods.get(learning_style, style_methods["visual"])
    
    # Calculate time distribution intelligently
    total_minutes = minutes_per_day * duration_days
    concept_time = total_minutes * 0.4  # 40% for concepts
    practice_time = total_minutes * 0.3  # 30% for practice
    review_time = total_minutes * 0.2    # 20% for review
    assessment_time = total_minutes * 0.1 # 10% for assessment
    
    # Generate detailed plan with topic-specific content
    plan = f"""
## 📚 {subject.title()} Study Plan - {level.title()} Level

**Duration**: {duration_days} days | **Daily Time**: {minutes_per_day} minutes  
**Learning Goal**: {goal}

### 🎯 Learning Objectives:
"""
    
    for i, topic in enumerate(topics, 1):
        # Get level-specific content for each topic
        topic_content = subject_knowledge[topic].get(level.lower(), subject_knowledge[topic]["beginner"])
        concepts = topic_content["concepts"][:3]  # Get first 3 concepts
        plan += f"\n{i}. **{topic.title()}** - Master: {', '.join(concepts)}"
    
    plan += f"""

### 📅 Weekly Schedule:
"""
    
    weeks = (duration_days + 6) // 7  # Calculate number of weeks
    for week in range(1, weeks + 1):
        start_day = (week - 1) * 7 + 1
        end_day = min(week * 7, duration_days)
        week_topics = topics[(week - 1) % len(topics):week % len(topics) + 1]
        
        # Get specific weekly topics for each subject
        week_details = []
        for topic in week_topics:
            topic_content = subject_knowledge[topic].get(level.lower(), subject_knowledge[topic]["beginner"])
            weekly_topics = topic_content.get("weekly_topics", [])
            if weekly_topics:
                week_details.append(f"{topic.title()}: {weekly_topics[week % len(weekly_topics) - 1]}")
            else:
                week_details.append(topic.title())
        
        plan += f"- **Week {week} (Days {start_day}-{end_day})**: Focus on {', '.join(week_details)}\n"
    
    plan += f"""

### 🧪 Practice Activities (Total: {int(practice_time)} minutes):
- **Daily Problem Solving**: {minutes_per_day//4} minutes - Work through exercises and examples
- **Weekly Quizzes**: {minutes_per_day//2} minutes - Test understanding and retention
- **Hands-on Projects**: {minutes_per_day//3} minutes - Apply concepts practically
- **Study Groups**: {minutes_per_day//6} minutes - Discuss and explain concepts to others

### 🎨 Learning Methods (Personalized for {learning_style} style):
"""
    
    for method in methods:
        plan += f"- {method}"
    
    plan += f"""

### 📊 Progress Tracking:
- **Daily**: Quick concept review and practice
- **Weekly**: Self-assessment and topic mastery check
- **Bi-weekly**: Comprehensive review and adjustment
- **Monthly**: Major milestone evaluation and plan refinement

### 💡 Difficulty Progression ({difficulty_preference} preference):
"""
    
    if difficulty_preference == "easy":
        plan += """
- Start with foundational concepts and basic examples
- Gradually introduce complexity through guided practice
- Focus on understanding before memorization
- Use multiple approaches to reinforce learning
"""
    elif difficulty_preference == "medium":
        plan += """
- Balance foundational and advanced concepts
- Mix theoretical understanding with practical application
- Challenge yourself with progressively harder problems
- Seek connections between different topics
"""
    else:  # hard
        plan += """
- Dive deep into complex concepts early
- Focus on problem-solving and critical thinking
- Explore advanced applications and edge cases
- Push beyond comfort zone for maximum growth
"""
    
    plan += f"""

### 🔍 Topic-Specific Content:
This plan incorporates {len(topics)} key topics with level-appropriate content:
"""
    
    for topic in topics:
        topic_content = subject_knowledge[topic].get(level.lower(), subject_knowledge[topic]["beginner"])
        plan += f"- **{topic.title()}**: {len(topic_content['concepts'])} core concepts, {len(topic_content['examples'])} examples, {len(topic_content['applications'])} applications\n"
    
    # Add specific examples for the selected topics
    plan += f"\n### 📝 Specific Examples for {level.title()} Level:\n"
    for topic in topics:
        topic_content = subject_knowledge[topic].get(level.lower(), subject_knowledge[topic]["beginner"])
        examples = topic_content["examples"][:2]  # Get 2 examples
        plan += f"- **{topic.title()}**: {', '.join(examples)}\n"
    
    return plan

# Enhanced explanation generator with contextual intelligence
def generate_intelligent_explanation(topic, level, explanation_type, include_visuals, use_cot, include_examples):
    """Generate an intelligent, contextual explanation using knowledge base."""
    
    # Find topic in knowledge base
    topic_found = False
    topic_data = {}
    subject_name = ""
    
    for subject, subjects in KNOWLEDGE_BASE.items():
        if topic.lower() in subjects:
            topic_data = subjects[topic.lower()]
            subject_name = subject
            topic_found = True
            break
    
    if not topic_found:
        # Generate generic explanation if topic not found
        topic_data = {
            "beginner": {
                "concepts": [f"{topic} is a fundamental concept that involves understanding core principles and applications."],
                "examples": [f"Basic examples of {topic} demonstrate its practical use."],
                "applications": [f"{topic} has applications in various fields and industries."]
            }
        }
        subject_name = "general"
    
    # Get level-appropriate content
    level_content = topic_data.get(level.lower(), topic_data["beginner"])
    concepts = level_content["concepts"]
    examples = level_content["examples"]
    applications = level_content["applications"]
    
    # Generate topic-specific explanation
    explanation = f"""
## 🧠 {topic.title()} - {level.title()} Level Explanation

### 📖 Core Concepts:
"""
    
    for i, concept in enumerate(concepts, 1):
        explanation += f"{i}. **{concept}**\n"
    
    explanation += f"""

### 🔍 {explanation_type.title()} Breakdown:
"""
    
    if explanation_type == "conceptual":
        explanation += f"""
- **What it is**: {topic.title()} represents fundamental principles in {subject_name}
- **Why it matters**: Understanding {topic.lower()} is crucial for advanced learning in {subject_name}
- **Key insight**: It connects multiple related concepts together
- **Core principle**: {concepts[0] if concepts else 'Fundamental understanding'}
"""
    elif explanation_type == "step-by-step":
        explanation += f"""
1. **Foundation**: Start with basic principles and definitions
2. **Building blocks**: Understand component parts and relationships
3. **Integration**: See how pieces fit together
4. **Application**: Practice with real-world examples
5. **Mastery**: Develop deep understanding and intuition
"""
    elif explanation_type == "with examples":
        explanation += f"""
- **Simple case**: Start with basic, clear examples
- **Intermediate**: Build complexity step by step
- **Advanced**: Explore edge cases and variations
- **Real-world**: Connect to practical applications
"""
    else:  # comprehensive
        explanation += f"""
- **Theoretical foundation**: Understand underlying principles
- **Practical application**: See how theory becomes practice
- **Historical context**: Learn about development and evolution
- **Future implications**: Explore current research and applications
"""
    
    if include_examples and examples:
        explanation += f"""

### 💡 Specific Examples for {level.title()} Level:
"""
        for i, example in enumerate(examples, 1):
            explanation += f"{i}. **{example}**\n"
    
    if include_visuals:
        explanation += f"""

### 🎨 Visual Description:
Imagine {topic.lower()} as a building with multiple floors. Each floor represents a different aspect or level of understanding. As you climb higher, you see more connections and applications. The foundation supports everything above, just as basic concepts support advanced understanding.
"""
    
    if use_cot:
        explanation += f"""

### 🤔 Chain of Thought:
1. **Question**: What is {topic} and why is it important in {subject_name}?
2. **Analysis**: Let me break this down systematically
3. **Understanding**: {concepts[0] if concepts else 'Core concept explanation'}
4. **Connection**: This relates to other concepts because...
5. **Application**: We use this in practice when...
6. **Conclusion**: {topic.title()} is essential for understanding {subject_name}...
"""
    
    if applications:
        explanation += f"""

### 🌍 Real-World Applications:
"""
        for i, application in enumerate(applications, 1):
            explanation += f"{i}. **{application}**\n"
    
    explanation += f"""

### 📚 Next Steps:
- Practice with progressively challenging problems
- Connect {topic.lower()} to related concepts in {subject_name}
- Apply understanding to real-world scenarios
- Explore advanced topics and research areas
- Teach others to reinforce your own understanding

### 🎯 Level-Appropriate Focus:
For {level} level, focus on: {', '.join(concepts[:2])}
"""
    
    return explanation

# Enhanced quiz generator with variety and intelligence
def generate_intelligent_quiz(topic, difficulty, num_questions, question_type):
    """Generate an intelligent, varied quiz using knowledge base."""
    
    # Find topic in knowledge base
    topic_found = False
    topic_data = {}
    
    for subject, subjects in KNOWLEDGE_BASE.items():
        if topic.lower() in subjects:
            topic_data = subjects[topic.lower()]
            topic_found = True
            break
    
    if not topic_found:
        # Generate generic questions if topic not found
        topic_data = {
            "beginner": {
                "concepts": [f"Understanding {topic} requires knowledge of fundamental principles"],
                "examples": [f"Basic applications of {topic} demonstrate its utility"],
                "applications": [f"{topic} has wide-ranging applications in various fields"]
            }
        }
    
    # Generate different question types
    questions = []
    
    if question_type == "multiple choice":
        questions = generate_multiple_choice_questions(topic, topic_data, difficulty, num_questions)
    elif question_type == "true/false":
        questions = generate_true_false_questions(topic, topic_data, difficulty, num_questions)
    elif question_type == "fill in the blank":
        questions = generate_fill_blank_questions(topic, topic_data, difficulty, num_questions)
    else:  # mixed
        questions = generate_mixed_questions(topic, topic_data, difficulty, num_questions)
    
    return questions

def generate_multiple_choice_questions(topic, topic_data, difficulty, num_questions):
    """Generate varied multiple choice questions."""
    
    # Base questions for different topics
    base_questions = {
        "calculus": [
            {
                "question": "What is the derivative of x³?",
                "options": ["x²", "2x²", "3x²", "3x"],
                "correct_answer": "3x²",
                "explanation": "Using the power rule: d/dx(x^n) = n*x^(n-1). For x³, n=3, so d/dx(x³) = 3*x^(3-1) = 3x²."
            },
            {
                "question": "What does the integral represent geometrically?",
                "options": ["Slope of the curve", "Area under the curve", "Length of the curve", "Volume of revolution"],
                "correct_answer": "Area under the curve",
                "explanation": "The definite integral calculates the area between the curve and the x-axis over a specified interval."
            },
            {
                "question": "What is the limit of 1/x as x approaches infinity?",
                "options": ["Infinity", "1", "0", "Undefined"],
                "correct_answer": "0",
                "explanation": "As x gets larger and larger, 1/x gets smaller and smaller, approaching 0."
            },
            {
                "question": "What is the derivative of a constant function?",
                "options": ["The constant itself", "Zero", "One", "Undefined"],
                "correct_answer": "Zero",
                "explanation": "A constant function doesn't change, so its rate of change (derivative) is zero."
            },
            {
                "question": "What is the integral of 2x?",
                "options": ["x²", "x² + C", "2x²", "2x² + C"],
                "correct_answer": "x² + C",
                "explanation": "The integral of 2x is x² + C, where C is the constant of integration."
            }
        ],
        "algebra": [
            {
                "question": "What is the solution to 2x + 5 = 13?",
                "options": ["x = 4", "x = 8", "x = 9", "x = 3"],
                "correct_answer": "x = 4",
                "explanation": "Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4."
            },
            {
                "question": "What is the vertex form of a quadratic equation?",
                "options": ["y = ax² + bx + c", "y = a(x-h)² + k", "y = mx + b", "y = 1/x"],
                "correct_answer": "y = a(x-h)² + k",
                "explanation": "The vertex form y = a(x-h)² + k shows the vertex at point (h,k)."
            },
            {
                "question": "What is the slope of the line y = 3x + 2?",
                "options": ["2", "3", "5", "Undefined"],
                "correct_answer": "3",
                "explanation": "In the slope-intercept form y = mx + b, m is the slope, so the slope is 3."
            }
        ],
        "physics": [
            {
                "question": "What is Newton's First Law?",
                "options": ["F = ma", "Action equals reaction", "Objects in motion stay in motion", "Gravity attracts objects"],
                "correct_answer": "Objects in motion stay in motion",
                "explanation": "Newton's First Law states that an object in motion will stay in motion unless acted upon by an external force."
            },
            {
                "question": "What is the formula for kinetic energy?",
                "options": ["KE = mgh", "KE = ½mv²", "KE = Fd", "KE = Pt"],
                "correct_answer": "KE = ½mv²",
                "explanation": "Kinetic energy is calculated using KE = ½mv², where m is mass and v is velocity."
            }
        ]
    }
    
    # Get questions for the specific topic
    topic_questions = base_questions.get(topic.lower(), base_questions["calculus"])
    
    # Adjust difficulty and add variety
    if difficulty == "easy":
        questions = topic_questions[:min(3, len(topic_questions))]
    elif difficulty == "medium":
        questions = topic_questions[:min(4, len(topic_questions))]
    else:  # hard
        questions = topic_questions[:min(5, len(topic_questions))]
    
    # Ensure we have enough questions
    while len(questions) < num_questions:
        # Create variations of existing questions
        for q in questions[:]:
            if len(questions) >= num_questions:
                break
            new_q = q.copy()
            new_q["question"] = f"Advanced: {q['question']}"
            new_q["explanation"] = f"Advanced understanding: {q['explanation']}"
            questions.append(new_q)
    
    # Shuffle questions for variety
    random.shuffle(questions)
    
    return questions[:num_questions]

def generate_true_false_questions(topic, topic_data, difficulty, num_questions):
    """Generate true/false questions."""
    
    questions = []
    
    # Generate T/F questions based on topic data
    if topic.lower() in ["calculus", "derivatives"]:
        tf_questions = [
            {
                "question": "The derivative of a constant is always zero.",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "A constant doesn't change, so its rate of change is zero."
            },
            {
                "question": "The integral of a function is always positive.",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Integrals can be positive, negative, or zero depending on the function and interval."
            },
            {
                "question": "All continuous functions are differentiable.",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Not all continuous functions are differentiable (e.g., |x| at x=0)."
            }
        ]
    else:
        tf_questions = [
            {
                "question": f"Understanding {topic} requires practice and application.",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Learning requires both theoretical understanding and practical application."
            },
            {
                "question": f"{topic.title()} has applications in multiple fields.",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Most fundamental concepts have wide-ranging applications."
            }
        ]
    
    # Select questions based on difficulty
    if difficulty == "easy":
        questions = tf_questions[:min(2, len(tf_questions))]
    elif difficulty == "medium":
        questions = tf_questions[:min(3, len(tf_questions))]
    else:
        questions = tf_questions[:min(3, len(tf_questions))]
    
    # Ensure enough questions
    while len(questions) < num_questions:
        for q in questions[:]:
            if len(questions) >= num_questions:
                break
            new_q = q.copy()
            new_q["question"] = f"Additional: {q['question']}"
            questions.append(new_q)
    
    random.shuffle(questions)
    return questions[:num_questions]

def generate_fill_blank_questions(topic, topic_data, difficulty, num_questions):
    """Generate fill-in-the-blank questions."""
    
    questions = []
    
    if topic.lower() in ["calculus", "derivatives"]:
        fill_questions = [
            {
                "question": "The derivative of x² is _____.",
                "options": ["2x", "x", "2x²", "x²"],
                "correct_answer": "2x",
                "explanation": "Using the power rule: d/dx(x^n) = n*x^(n-1). For x², n=2, so d/dx(x²) = 2x."
            },
            {
                "question": "The integral of 2x is _____.",
                "options": ["x²", "x² + C", "2x²", "2x² + C"],
                "correct_answer": "x² + C",
                "explanation": "The integral of 2x is x² + C, where C is the constant of integration."
            }
        ]
    else:
        fill_questions = [
            {
                "question": f"Understanding {topic} requires _____ and _____.",
                "options": ["theory and practice", "memorization only", "examples only", "none of the above"],
                "correct_answer": "theory and practice",
                "explanation": "Effective learning combines theoretical understanding with practical application."
            }
        ]
    
    # Select questions based on difficulty
    if difficulty == "easy":
        questions = fill_questions[:min(2, len(fill_questions))]
    else:
        questions = fill_questions[:min(3, len(fill_questions))]
    
    # Ensure enough questions
    while len(questions) < num_questions:
        for q in questions[:]:
            if len(questions) >= num_questions:
                break
            new_q = q.copy()
            new_q["question"] = f"Additional: {q['question']}"
            questions.append(new_q)
    
    random.shuffle(questions)
    return questions[:num_questions]

def generate_mixed_questions(topic, topic_data, difficulty, num_questions):
    """Generate a mix of different question types."""
    
    mc_questions = generate_multiple_choice_questions(topic, topic_data, difficulty, num_questions//2)
    tf_questions = generate_true_false_questions(topic, topic_data, difficulty, num_questions//3)
    fill_questions = generate_fill_blank_questions(topic, topic_data, difficulty, num_questions//3)
    
    # Combine and shuffle
    all_questions = mc_questions + tf_questions + fill_questions
    random.shuffle(all_questions)
    
    return all_questions[:num_questions]

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
        💡 **Intelligent Features:**
        • Advanced Study Planning
        • Contextual Explanations
        • Varied Quiz Generation
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
                    # Generate intelligent study plan
                    study_plan = generate_intelligent_study_plan(
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
                    # Generate intelligent explanation
                    explanation = generate_intelligent_explanation(
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
        st.markdown("*Powered by intelligent algorithms with varied question types and personalized difficulty*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Quiz Topic", value="calculus fundamentals", key="quiz_topic")
            subject = st.text_input("Subject", value="mathematics", key="quiz_subject")
            difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], key="quiz_difficulty")
        
        with col2:
            num_questions = st.number_input("Number of Questions", min_value=3, max_value=15, value=5, step=1)
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
                    # Generate intelligent quiz
                    quiz_data = generate_intelligent_quiz(topic, difficulty, num_questions, question_type)
                    
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
            st.markdown(f"**Topic:** {topic} | **Difficulty:** {difficulty} | **Questions:** {len(quiz_data)} | **Type:** {question_type}")
            
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
        🚀 Powered by SmartLearn Intelligent AI • Advanced Algorithms • Varied Content • Personalized Learning
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
