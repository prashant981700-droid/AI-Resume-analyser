"""
Job Description Matcher
Uses TF-IDF cosine similarity to compute match between resume and JD.
Falls back to keyword overlap if sklearn is unavailable.
"""
import re
from collections import Counter
import math

STOPWORDS = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with",
    "is","are","was","were","be","been","being","have","has","had","do","does",
    "did","will","would","could","should","may","might","shall","can","not",
    "this","that","these","those","it","its","we","you","he","she","they","i",
    "my","your","our","their","his","her","from","by","about","as","into",
    "through","during","before","after","above","below","up","down","out",
    "off","over","under","again","then","once","here","there","when","where",
    "why","how","all","both","each","few","more","most","other","some","such",
    "no","nor","only","own","same","so","than","too","very","just","because",
}

def _tokenise(text: str):
    words = re.findall(r'\b[a-z][a-z0-9+#.]*\b', text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]

def _tfidf_cosine(doc1: str, doc2: str) -> float:
    """Pure-Python TF-IDF cosine similarity (no external deps)."""
    t1, t2 = _tokenise(doc1), _tokenise(doc2)
    vocab   = set(t1) | set(t2)
    tf1     = Counter(t1)
    tf2     = Counter(t2)

    # IDF over the tiny 2-doc corpus
    def idf(term):
        in_docs = (term in tf1) + (term in tf2)
        return math.log((2 + 1) / (in_docs + 1)) + 1

    def vec(tf_map):
        return {t: (tf_map[t] / max(len(t1), 1)) * idf(t) for t in vocab}

    v1, v2 = vec(tf1), vec(tf2)
    dot    = sum(v1.get(t, 0) * v2.get(t, 0) for t in vocab)
    mag1   = math.sqrt(sum(x**2 for x in v1.values())) or 1
    mag2   = math.sqrt(sum(x**2 for x in v2.values())) or 1
    return dot / (mag1 * mag2)

def match_jd(resume_text: str, job_desc: str) -> dict:
    if not job_desc.strip():
        return {}

    # Cosine similarity score
    score = _tfidf_cosine(resume_text, job_desc)
    match_pct = min(100, round(score * 180))  # scale to 0–100

    # Keyword analysis
    jd_tokens     = set(_tokenise(job_desc))
    resume_tokens = set(_tokenise(resume_text))

    matched   = sorted(jd_tokens & resume_tokens)
    unmatched = sorted(jd_tokens - resume_tokens)

    # Score each keyword by frequency in JD
    jd_freq = Counter(_tokenise(job_desc))
    top_matched   = sorted(matched,   key=lambda w: jd_freq[w], reverse=True)[:15]
    top_unmatched = sorted(unmatched, key=lambda w: jd_freq[w], reverse=True)[:15]

    # Keyword density
    density = round(len(matched) / max(len(jd_tokens), 1) * 100)

    return {
        "match_percent":   match_pct,
        "keyword_density": density,
        "matched_keywords":   top_matched,
        "missing_keywords":   top_unmatched,
        "total_jd_keywords":  len(jd_tokens),
        "matched_count":      len(matched),
    }
