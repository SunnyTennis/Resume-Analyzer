import os

def generate_recommendations(analysis: dict, resume_text: str, job_text: str) -> str:
    """Optional OpenAI explanation. Falls back to deterministic recommendations."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "\n".join(f"- {x}" for x in analysis["recommendations"])
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a careful resume-writing assistant.
Use only facts explicitly present in the resume. Never invent skills, employers,
degrees, dates, achievements, or metrics. Distinguish missing evidence from
missing qualifications. Give 3-5 concise, actionable suggestions.

Resume excerpt:
{resume_text[:7000]}

Job description:
{job_text[:5000]}

Matched skills: {analysis['matched_skills']}
Skills not found in resume: {analysis['missing_skills']}
"""
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content or "No recommendations returned."
    except Exception as exc:
        return "LLM unavailable; using rule-based suggestions instead.\n" + "\n".join(
            f"- {x}" for x in analysis["recommendations"]
        ) + f"\n\nTechnical detail: {type(exc).__name__}"
