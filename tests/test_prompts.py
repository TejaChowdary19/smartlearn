import re
from src.core.prompt_templates import StudyPlanPrompt, ExplanationPrompt, QuizPrompt

def test_templates_have_placeholders():
    s = StudyPlanPrompt()
    e = ExplanationPrompt()
    q = QuizPrompt()
    sp = s.render(subject="Algebra", level="10th grade", minutes_per_day=30, duration_days=7, goal="master linear equations")
    assert "Algebra" in sp and "10th grade" in sp
    ep = e.render(topic="Linear Equations", level="10th grade")
    assert "Linear Equations" in ep
    qp = q.render(topic="Linear Equations", level="10th grade", difficulty=1)
    assert "difficulty 1" in qp.lower()
