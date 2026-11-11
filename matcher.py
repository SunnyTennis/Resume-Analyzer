from difflib import SequenceMatcher

def semantic_similarity(resume_text: str, job_text: str) -> tuple[float, str]:
    """
    Uses Sentence Transformers when installed; otherwise a transparent lexical
    similarity fallback. Returns score 0..100 and method label.
    """
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode([resume_text[:12000], job_text[:12000]])
        score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
        return max(0.0, min(100.0, score * 100)), "Sentence Transformers (all-MiniLM-L6-v2)"
    except Exception:
        # Fallback is intentionally simple and clearly labelled, not an embedding model.
        a = set(resume_text.lower().split())
        b = set(job_text.lower().split())
        overlap = len(a & b) / max(1, len(a | b))
        sequence = SequenceMatcher(None, resume_text.lower()[:5000], job_text.lower()[:5000]).ratio()
        return min(100.0, (0.75 * overlap + 0.25 * sequence) * 100), "Lexical fallback (install sentence-transformers for semantic matching)"
