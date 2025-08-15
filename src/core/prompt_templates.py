from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json

@dataclass
class AdvancedPromptTemplate:
    """Base class for advanced prompt engineering features."""
    
    def add_chain_of_thought(self, prompt: str, reasoning_steps: List[str] = None) -> str:
        """Add chain-of-thought reasoning to prompts."""
        if not reasoning_steps:
            reasoning_steps = [
                "First, let me understand what is being asked",
                "Next, I'll break this down into logical steps", 
                "Then, I'll apply relevant knowledge and concepts",
                "Finally, I'll provide a comprehensive answer"
            ]
        
        cot_prompt = f"""
{prompt}

**Reasoning Process:**
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(reasoning_steps)])}

Please think through this step by step before providing your final answer.
"""
        return cot_prompt
    
    def add_few_shot_examples(self, prompt: str, examples: List[Dict[str, Any]]) -> str:
        """Add few-shot learning examples to prompts."""
        examples_text = "\n\n**Examples:**\n"
        for i, example in enumerate(examples):
            examples_text += f"""
**Example {i+1}:**
Input: {example.get('input', 'N/A')}
Output: {example.get('output', 'N/A')}
"""
        
        return f"{prompt}\n{examples_text}\nNow, please provide your response following the pattern above."
    
    def add_dynamic_context(self, prompt: str, user_context: Dict[str, Any]) -> str:
        """Dynamically adapt prompts based on user context."""
        context_text = ""
        if user_context.get('learning_style'):
            context_text += f"\n**Learning Style:** {user_context['learning_style']}"
        if user_context.get('previous_knowledge'):
            context_text += f"\n**Previous Knowledge:** {user_context['previous_knowledge']}"
        if user_context.get('difficulty_preference'):
            context_text += f"\n**Difficulty Preference:** {user_context['difficulty_preference']}"
        
        return f"{prompt}{context_text}" if context_text else prompt

@dataclass
class StudyPlanPrompt(AdvancedPromptTemplate):
    def render(self, subject: str, level: str, minutes_per_day: int, duration_days: int, goal: str, 
               rag_context: Optional[str] = None, rag_sources: Optional[List[dict]] = None,
               user_context: Optional[Dict[str, Any]] = None, use_cot: bool = True) -> str:
        
        # Subject-specific study strategies
        subject_strategies = self._get_subject_strategies(subject)
        
        # RAG context integration
        rag_instruction = ""
        if rag_context:
            rag_instruction = f"""
KNOWLEDGE BASE CONTEXT:
{rag_context}

Use this context to create a more accurate and relevant study plan. Reference specific concepts, formulas, or techniques from your knowledge base when appropriate.
"""
        
        # Base prompt
        base_prompt = f"""Create a comprehensive {duration_days}-day study plan for {level} {subject}.

**Study Parameters:**
- Daily time: {minutes_per_day} minutes
- Goal: {goal}
- Subject: {subject}
- Level: {level}

{subject_strategies}

{rag_instruction}

**Study Plan Requirements:**
- Each day should have 3-5 focused learning objectives
- Include active learning activities (practice problems, exercises, projects)
- Incorporate spaced repetition principles
- Add self-assessment checkpoints every 3-4 days
- Include resources and reference materials
- Conclude with comprehensive review and final assessment

**Output Format:**
## Day 1: [Topic Focus]
**Learning Objectives:**
- [Specific objective 1]
- [Specific objective 2]
**Activities:**
- [Practice/Exercise description]
**Resources:** [Reference materials]

Continue for all {duration_days} days, ending with:
## Day {duration_days}: Comprehensive Review & Assessment
**Review Topics:** [Key concepts to review]
**Final Assessment:** [Self-test or project description]"""

        # Add dynamic context if available
        if user_context:
            base_prompt = self.add_dynamic_context(base_prompt, user_context)
        
        # Add chain-of-thought reasoning if requested
        if use_cot:
            base_prompt = self.add_chain_of_thought(base_prompt)
        
        return base_prompt
    
    def _get_subject_strategies(self, subject: str) -> str:
        """Return subject-specific study strategies."""
        strategies = {
            "mathematics": "Focus on problem-solving practice, formula memorization, and concept connections. Include daily practice problems and weekly concept reviews.",
            "computer science": "Emphasize hands-on coding, algorithm understanding, and project-based learning. Include code reviews and debugging practice.",
            "physics": "Combine theoretical understanding with practical applications. Include problem-solving, lab work, and real-world examples.",
            "chemistry": "Focus on understanding molecular concepts, balancing equations, and laboratory safety. Include hands-on experiments and calculations.",
            "biology": "Emphasize understanding systems and processes, memorizing key terms, and connecting concepts. Include diagrams and real-world applications.",
            "history": "Focus on chronological understanding, cause-and-effect relationships, and primary source analysis. Include timeline creation and document analysis.",
            "literature": "Emphasize close reading, analysis, and creative writing. Include discussion, essay writing, and literary analysis.",
            "economics": "Focus on understanding principles, analyzing data, and applying concepts to real situations. Include case studies and data interpretation."
        }
        return strategies.get(subject.lower(), "Focus on understanding core concepts, regular practice, and application of knowledge.")

@dataclass
class ExplanationPrompt(AdvancedPromptTemplate):
    def render(self, topic: str, level: str, rag_context: Optional[str] = None, 
               rag_sources: Optional[List[dict]] = None, user_context: Optional[Dict[str, Any]] = None,
               use_cot: bool = True, include_examples: bool = True) -> str:
        
        # Level-specific explanation guidelines
        level_guidelines = self._get_level_guidelines(level)
        
        # RAG context integration
        rag_instruction = ""
        if rag_context:
            rag_instruction = f"""
KNOWLEDGE BASE CONTEXT:
{rag_context}

Use this context to provide accurate, detailed explanations. Reference specific concepts, examples, or techniques from your knowledge base when relevant.
"""
        
        # Base prompt
        base_prompt = f"""Provide a comprehensive explanation of "{topic}" for a {level} student.

{level_guidelines}

{rag_instruction}

**Explanation Structure:**
1. **Overview**: 2-3 sentence introduction explaining what the topic is
2. **Core Concepts**: Break down the main ideas into digestible parts
3. **Examples**: Provide 2-3 concrete examples (simple to complex)
4. **Real-World Applications**: Show how this topic applies in everyday life or other subjects
5. **Common Misconceptions**: Address typical misunderstandings
6. **Practice Questions**: 3 questions of increasing difficulty (no answers)
7. **Further Study**: Suggest related topics or resources for deeper learning

Make the explanation engaging, clear, and appropriate for the specified level."""

        # Add dynamic context if available
        if user_context:
            base_prompt = self.add_dynamic_context(base_prompt, user_context)
        
        # Add few-shot examples if requested
        if include_examples:
            examples = self._get_explanation_examples(topic, level)
            base_prompt = self.add_few_shot_examples(base_prompt, examples)
        
        # Add chain-of-thought reasoning if requested
        if use_cot:
            base_prompt = self.add_chain_of_thought(base_prompt)
        
        return base_prompt
    
    def _get_level_guidelines(self, level: str) -> str:
        """Return level-specific explanation guidelines."""
        guidelines = {
            "beginner": "Use simple language, avoid jargon, focus on basic concepts, provide many examples, use analogies from everyday life.",
            "intermediate": "Build on basic knowledge, introduce some technical terms, include moderate complexity examples, connect to related concepts.",
            "advanced": "Assume solid foundation, use technical terminology, include complex examples, explore advanced applications and edge cases."
        }
        return guidelines.get(level.lower(), "Provide clear, comprehensive explanations with appropriate complexity for the level.")
    
    def _get_explanation_examples(self, topic: str, level: str) -> List[Dict[str, str]]:
        """Get few-shot examples for explanations."""
        # This could be expanded with more sophisticated examples
        return [
            {
                "input": f"Explain {topic} to a {level} student",
                "output": f"Here's a comprehensive explanation of {topic}..."
            }
        ]

@dataclass
class QuizPrompt(AdvancedPromptTemplate):
    def render(self, topic: str, level: str, difficulty: str, num_questions: int = 10,
               rag_context: Optional[str] = None, rag_sources: Optional[List[dict]] = None,
               user_context: Optional[Dict[str, Any]] = None, use_cot: bool = True) -> str:
        
        # Difficulty-specific guidelines
        difficulty_guidelines = self._get_difficulty_guidelines(difficulty)
        
        # RAG context integration
        rag_instruction = ""
        if rag_context:
            rag_instruction = f"""
KNOWLEDGE BASE CONTEXT:
{rag_context}

Use this context to create questions that are accurate and relevant to the topic. Reference specific concepts, formulas, or examples from your knowledge base when appropriate.
"""
        
        # Base prompt
        base_prompt = f"""Create a {difficulty.lower()} level assessment on "{topic}" for a {level} student with exactly {num_questions} questions.

**Difficulty Level: {difficulty.upper()}**
{difficulty_guidelines}

{rag_instruction}

**Question Requirements:**
- Exactly {num_questions} multiple choice questions
- Each question should have 4 distinct, plausible options
- Questions should progress from basic to more challenging
- Include a mix of concept understanding and application
- Make incorrect options plausible but clearly wrong
- Provide clear, concise explanations for correct answers

**Output Format:**
Q1. [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [A/B/C/D]
Explanation: [Brief explanation of why this is correct]

Continue this format for all {num_questions} questions."""

        # Add dynamic context if available
        if user_context:
            base_prompt = self.add_dynamic_context(base_prompt, user_context)
        
        # Add chain-of-thought reasoning if requested
        if use_cot:
            base_prompt = self.add_chain_of_thought(base_prompt)
        
        return base_prompt
    
    def _get_difficulty_guidelines(self, difficulty: str) -> str:
        """Return difficulty-specific question guidelines."""
        guidelines = {
            "easy": "Focus on basic facts, definitions, and simple applications. Use straightforward language and make incorrect options obviously wrong.",
            "medium": "Test understanding and application of concepts. Use moderate complexity language and make incorrect options plausible but wrong.",
            "hard": "Challenge with analysis, synthesis, and evaluation. Use advanced concepts and make incorrect options very plausible. Include complex scenarios."
        }
        return guidelines.get(difficulty.lower(), "Create questions appropriate for the specified difficulty level.")

@dataclass
class RAGEnhancedPrompt(AdvancedPromptTemplate):
    """Enhanced RAG prompt with advanced features."""
    
    def _format_rag_context(self, rag_context: str, rag_sources: List[dict]) -> str:
        """Format RAG context and sources for inclusion in prompts."""
        if not rag_context:
            return ""
        
        source_info = "\n".join([
            f"- {source['source']} (Relevance: {source['relevance_score']:.2f})"
            for source in rag_sources[:3]  # Top 3 most relevant sources
        ])
        
        return f"""
KNOWLEDGE BASE CONTEXT:
{rag_context}

SOURCES:
{source_info}

Use this context to provide accurate, relevant, and comprehensive responses. Reference specific information from your knowledge base when appropriate.
"""

@dataclass
class AdaptivePromptManager:
    """Manages dynamic prompt adaptation based on user performance and preferences."""
    
    def __init__(self):
        self.user_performance = {}
        self.prompt_variations = {}
    
    def adapt_prompt_complexity(self, base_prompt: str, user_level: str, performance_history: List[float]) -> str:
        """Adapt prompt complexity based on user performance."""
        if not performance_history:
            return base_prompt
        
        avg_performance = sum(performance_history) / len(performance_history)
        
        if avg_performance > 0.8:  # High performer
            complexity_instruction = "\n\n**Advanced Instructions:** Include complex scenarios, edge cases, and advanced applications."
        elif avg_performance > 0.6:  # Medium performer
            complexity_instruction = "\n\n**Intermediate Instructions:** Balance basic and advanced concepts with clear explanations."
        else:  # Low performer
            complexity_instruction = "\n\n**Basic Instructions:** Focus on fundamental concepts with many examples and step-by-step explanations."
        
        return base_prompt + complexity_instruction
    
    def get_personalized_prompt(self, prompt_type: str, user_id: str, **kwargs) -> str:
        """Get a personalized prompt based on user history and preferences."""
        # This could be expanded with more sophisticated personalization
        base_prompt = self._get_base_prompt(prompt_type, **kwargs)
        
        if user_id in self.user_performance:
            return self.adapt_prompt_complexity(base_prompt, "intermediate", self.user_performance[user_id])
        
        return base_prompt
    
    def _get_base_prompt(self, prompt_type: str, **kwargs) -> str:
        """Get base prompt for a given type."""
        if prompt_type == "study_plan":
            return StudyPlanPrompt().render(**kwargs)
        elif prompt_type == "explanation":
            return ExplanationPrompt().render(**kwargs)
        elif prompt_type == "quiz":
            return QuizPrompt().render(**kwargs)
        else:
            return "Please provide a detailed response."