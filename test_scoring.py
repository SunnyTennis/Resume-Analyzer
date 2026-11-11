from app.scoring import analyze_resume

def test_skill_matching_and_score():
    resume = "Skills\nPython, SQL, statistics, pandas\nExperience\nBuilt a data analysis project."
    job = "Required skills: Python, SQL, statistics, machine learning."
    result = analyze_resume(resume, job)
    assert "python" in result["matched_skills"]
    assert "sql" in result["matched_skills"]
    assert "machine learning" in result["missing_skills"]
    assert 0 <= result["overall_score"] <= 100

def test_empty_recognized_job_skills_does_not_crash():
    result = analyze_resume("A resume with some experience.", "Seeking a curious and motivated person.")
    assert 0 <= result["overall_score"] <= 100
