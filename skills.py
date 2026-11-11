import re

# Canonical names and common variants. Extend this dictionary for your target roles.
SKILL_ALIASES = {
    "python": ["python", "pandas", "numpy"],
    "r": [r"\br\b", "r programming", "tidyverse", "ggplot2"],
    "sql": ["sql", "postgresql", "mysql", "sqlite", "sql server"],
    "machine learning": ["machine learning", "scikit-learn", "sklearn", "xgboost"],
    "deep learning": ["deep learning", "pytorch", "tensorflow", "keras"],
    "nlp": ["natural language processing", r"\bnlp\b", "spacy", "nltk", "transformers"],
    "generative ai": ["generative ai", "llm", "large language model", "prompt engineering", "rag"],
    "statistics": ["statistics", "statistical analysis", "hypothesis testing", "regression"],
    "data visualization": ["tableau", "power bi", "matplotlib", "seaborn", "plotly", "visualization"],
    "excel": ["excel", "vlookup", "pivot table"],
    "cloud": ["aws", "azure", "google cloud", "gcp"],
    "fastapi": ["fastapi"],
    "streamlit": ["streamlit"],
    "git": ["git", "github", "version control"],
    "docker": ["docker", "containerization"],
    "airflow": ["airflow", "workflow orchestration"],
    "spark": ["apache spark", "pyspark"],
    "communication": ["communication", "stakeholder", "cross-functional"],
    "project management": ["project management", "agile", "scrum"],
}

def _contains(text: str, term: str) -> bool:
    if term.startswith("\\b"):
        return re.search(term, text, re.I) is not None
    # Use word boundaries for simple terms to avoid matching substrings.
    return re.search(r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])", text, re.I) is not None

def extract_skills(text: str) -> list[str]:
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains(text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(found)

def find_skill_evidence(text: str, skill: str) -> str:
    aliases = SKILL_ALIASES.get(skill, [skill])
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if any(_contains(line, alias) for alias in aliases):
            return line[:260]
    return ""
