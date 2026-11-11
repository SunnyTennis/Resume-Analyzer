from app.skills import extract_skills, find_skill_evidence
from app.matcher import semantic_similarity

WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "education": 0.15,
    "relevance": 0.20,
}

def _keyword_coverage(resume_text: str, job_text: str, terms: list[str]) -> tuple[float, list[str], list[str]]:
    resume = resume_text.lower()
    job = job_text.lower()
    required = [t for t in terms if t.lower() in job]
    if not required:
        return 0.0, [], []
    matched = [t for t in required if t.lower() in resume]
    missing = [t for t in required if t.lower() not in resume]
    return 100 * len(matched) / len(required), matched, missing

def analyze_resume(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    skills_score = 100 * len(matched) / max(1, len(job_skills))

    # Experience and education indicators are intentionally heuristic. They are
    # explainable signals, not verification of years, seniority, or credentials.
    exp_terms = ["experience", "intern", "analyst", "engineer", "scientist", "manager", "developed", "built"]
    edu_terms = ["bachelor", "master", "phd", "degree", "university", "college", "statistics", "mathematics"]
    exp_score, exp_hits, exp_missing = _keyword_coverage(resume_text, job_text, exp_terms)
    edu_score, edu_hits, edu_missing = _keyword_coverage(resume_text, job_text, edu_terms)
    relevance_score, relevance_method = semantic_similarity(resume_text, job_text)

    # If job description contains no recognized skills, avoid silently awarding
    # a perfect skill score; report the limitation.
    total = (
        WEIGHTS["skills"] * skills_score
        + WEIGHTS["experience"] * exp_score
        + WEIGHTS["education"] * edu_score
        + WEIGHTS["relevance"] * relevance_score
    )
    evidence = {s: find_skill_evidence(resume_text, s) for s in matched}
    recommendations = []
    if missing:
        recommendations.append("If you genuinely have these skills, add concrete evidence of where and how you used: " + ", ".join(missing) + ".")
    if not any(x in resume_text.lower() for x in ["result", "%", "increased", "reduced", "improved"]):
        recommendations.append("Add measurable outcomes to relevant experience or project bullets where you can substantiate them.")
    if not any(x in resume_text.lower() for x in ["project", "built", "developed", "implemented"]):
        recommendations.append("Include a projects section describing the problem, methods, tools, and outcome.")
    if not recommendations:
        recommendations.append("Prioritize the strongest relevant experience and quantify outcomes where possible.")

    return {
        "overall_score": round(total),
        "component_scores": {
            "skills": round(skills_score, 1),
            "experience": round(exp_score, 1),
            "education": round(edu_score, 1),
            "relevance": round(relevance_score, 1),
        },
        "weights": WEIGHTS,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_evidence": evidence,
        "experience_keyword_hits": exp_hits,
        "education_keyword_hits": edu_hits,
        "experience_keyword_gaps": exp_missing,
        "education_keyword_gaps": edu_missing,
        "similarity_method": relevance_method,
        "recommendations": recommendations,
        "limitations": [
            "Scores are heuristic decision-support signals, not hiring probabilities or objective measures of candidate quality.",
            "A skill not found in the resume may still be held by the candidate; it may simply be omitted or phrased differently.",
            "Experience and education components use keyword indicators and do not verify years of experience, degree equivalency, or qualification validity.",
            "The semantic similarity component may vary by model version; the fallback is lexical rather than semantic."
        ]
    }
