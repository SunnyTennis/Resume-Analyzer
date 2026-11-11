# AI Resume Analyzer

An end-to-end MVP that compares a resume with a job description, extracts recognized skills, calculates a transparent weighted match score, identifies skills not found in the resume, and suggests improvements.

## Features

- PDF, DOCX, and TXT resume upload
- Lightweight resume section parsing
- Skill extraction using an editable alias dictionary
- Skill overlap and evidence snippets
- Optional semantic similarity with Sentence Transformers
- Transparent weighted scoring
- Optional OpenAI-generated recommendations
- Streamlit user interface
- FastAPI JSON endpoint
- JSON export and unit tests

## Stack

Python, Streamlit, FastAPI, PyMuPDF, python-docx, Sentence Transformers, scikit-learn, OpenAI API (optional).

## Setup

Python 3.10+ is recommended.

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the Streamlit app

From the project root:

```bash
streamlit run app/frontend.py
```

Upload a resume and paste a job description. For a quick test, use `data/sample_resume.txt` and `data/sample_job_description.txt`.

## Run the API

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "resume=@data/sample_resume.txt" \
  -F "job_description=Seeking a Data Scientist with Python, SQL, statistics, and machine learning."
```

## Optional OpenAI recommendations

Copy `.env.example` to `.env`, add your API key, and load environment variables before starting Streamlit.

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your_key"
streamlit run app/frontend.py
```

macOS/Linux:
```bash
export OPENAI_API_KEY="your_key"
streamlit run app/frontend.py
```

Without an API key, the application uses deterministic rule-based recommendations. The scoring engine does not depend on the LLM.

## Scoring logic

The overall score is a weighted combination of four components:

| Component | Weight | MVP calculation |
|---|---:|---|
| Technical skills | 40% | Recognized job-description skills also found in the resume / recognized job-description skills |
| Experience | 25% | Coverage of selected experience-related keywords appearing in the job description |
| Education | 15% | Coverage of selected education-related keywords appearing in the job description |
| Text relevance | 20% | Sentence Transformer cosine similarity; lexical fallback if unavailable |

`overall = 0.40 * skills + 0.25 * experience + 0.15 * education + 0.20 * relevance`

All component values are on a 0–100 scale. The skill dictionary is in `app/skills.py` and can be expanded for specific industries.

### Important limitations

- This is a portfolio MVP, not a validated hiring or candidate-ranking system.
- A skill not found in the resume is not proof that the candidate lacks it.
- Experience and education are estimated from keyword indicators; the MVP does not verify years of experience, degree requirements, or credential authenticity.
- Semantic similarity measures textual similarity, not actual job performance.
- Scanned/image-only PDFs need OCR; OCR is not included.
- The built-in skill taxonomy is intentionally small and should be expanded and tested.
- Avoid uploading sensitive personal information to third-party LLM services without appropriate consent and safeguards.

## Sample input and output

Sample inputs are in `data/`.

Expected qualitative result for the sample pair:
- Matched skills include Python, SQL, statistics, machine learning, and data visualization (depending on exact aliases present).
- Cloud/AWS may be reported as not found in the resume.
- The numeric score can vary if the Sentence Transformers model is installed; otherwise the app uses a labelled lexical fallback.

## Tests

```bash
pytest -q
```

## Suggested next improvements

1. Add OCR for scanned resumes.
2. Add a curated job-skill taxonomy and skill importance levels.
3. Extract years of experience and dates with robust entity/temporal parsing.
4. Add a human-reviewed evaluation set and calibration report.
5. Add persistence, authentication, rate limiting, and file deletion controls before production use.
6. Add deployment configuration (Docker and a cloud host).

## License

Choose a license before making the repository public. Do not upload real candidate resumes or API keys.
