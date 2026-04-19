from openai import OpenAI
from app.core.config import settings


def _mock_response(text: str) -> dict:
    excerpt = text[:700].replace('\n', ' ').strip()
    return {
        'summary': f"This is a demo summary based on the uploaded content. Main focus: {excerpt[:300]}...",
        'questions': (
            "1. What is the central idea of the uploaded content?\n"
            "2. Identify two important concepts and explain them.\n"
            "3. How can the ideas be applied in practice?\n"
            "4. What strengths or limitations appear in the text?\n"
            "5. Suggest one improvement or recommendation."
        ),
        'rubric': (
            "Excellent (5): Clear understanding, accurate explanation, and strong examples.\n"
            "Very Good (4): Good understanding with minor gaps.\n"
            "Good (3): Basic understanding but limited depth.\n"
            "Acceptable (2): Partial answer with weak support.\n"
            "Weak (0-1): Incomplete or unclear response."
        ),
        'study_plan': (
            "Day 1: Read the content and identify key terms.\n"
            "Day 2: Review the summary and rewrite it in your own words.\n"
            "Day 3: Answer the generated questions.\n"
            "Day 4: Revise weak areas and create flashcards.\n"
            "Day 5: Self-test using short-answer questions."
        )
    }


def generate_academic_outputs(text: str) -> dict:
    if not settings.openai_api_key:
        return _mock_response(text)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
You are an academic assistant.
Based on the content below, produce four sections:
1) Summary
2) Five study questions
3) A simple rubric with five levels
4) A 5-day study plan

Content:
{text[:12000]}
"""

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )
    output_text = response.output_text

    parts = output_text.split('2) Five study questions')
    if len(parts) < 2:
        return _mock_response(text)

    summary = parts[0].replace('1) Summary', '').strip()
    rest = '2) Five study questions' + parts[1]

    q_parts = rest.split('3) A simple rubric with five levels')
    questions = q_parts[0].replace('2) Five study questions', '').strip()

    if len(q_parts) < 2:
        return _mock_response(text)

    r_parts = q_parts[1].split('4) A 5-day study plan')
    rubric = r_parts[0].strip()
    study_plan = r_parts[1].strip() if len(r_parts) > 1 else ''

    return {
        'summary': summary,
        'questions': questions,
        'rubric': rubric,
        'study_plan': study_plan or _mock_response(text)['study_plan']
    }
