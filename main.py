from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.parser import extract_text
from app.scoring import analyze_resume

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

@app.get("/")
def health():
    return {"status": "ok", "message": "AI Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        data = await resume.read()
        resume_text = extract_text(data, resume.filename or "resume.txt")
        if not job_description.strip():
            raise ValueError("Job description cannot be empty.")
        return analyze_resume(resume_text, job_description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {type(exc).__name__}")
