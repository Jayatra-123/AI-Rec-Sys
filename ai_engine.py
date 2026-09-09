# ============================================================
# AI RECRUITMENT SYSTEM
# AI RESUME SCREENING ENGINE
# ============================================================

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# TF-IDF SCORE
# ============================================================

def calculate_tfidf_score(job_description, resume_text):

    if not job_description or not resume_text:

        return 0.0

    job_description = clean_text(job_description)

    resume_text = clean_text(resume_text)

    documents = [
        job_description,
        resume_text
    ]

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )

        score = similarity[0][0] * 100

        return round(float(score), 2)

    except Exception as e:

        print("AI scoring error:", e)

        return 0.0


# ============================================================
# KEYWORD MATCH SCORE
# ============================================================

def calculate_keyword_score(required_skills, resume_text):

    if not required_skills or not resume_text:

        return 0.0

    resume_lower = resume_text.lower()

    skills = re.split(
        r"[,;/|]+",
        required_skills
    )

    skills = [
        skill.strip().lower()
        for skill in skills
        if skill.strip()
    ]

    if not skills:

        return 0.0

    matched = 0

    for skill in skills:

        if skill in resume_lower:

            matched += 1

    score = (matched / len(skills)) * 100

    return round(score, 2)


# ============================================================
# FINAL AI SCORE
# ============================================================

def calculate_score(
    job_description,
    required_skills,
    resume_text
):
    """
    Final score combines:

    70% TF-IDF similarity
    30% required-skill matching
    """

    tfidf_score = calculate_tfidf_score(
        job_description,
        resume_text
    )

    keyword_score = calculate_keyword_score(
        required_skills,
        resume_text
    )

    final_score = (
        tfidf_score * 0.70
        +
        keyword_score * 0.30
    )

    final_score = max(
        0,
        min(100, final_score)
    )

    return round(final_score, 2)


# ============================================================
# AUTOMATIC STATUS
# ============================================================

def get_status(score):

    if score >= 80:

        return "Shortlisted"

    elif score >= 60:

        return "Under Review"

    else:

        return "Rejected"


# ============================================================
# RECOMMENDATION
# ============================================================

def get_recommendation(score):

    if score >= 80:

        return "Highly Recommended"

    elif score >= 70:

        return "Recommended"

    elif score >= 60:

        return "Needs Review"

    else:

        return "Not Recommended"


# ============================================================
# MATCHED SKILLS
# ============================================================

def get_matched_skills(
    required_skills,
    resume_text
):

    if not required_skills or not resume_text:

        return []

    resume_lower = resume_text.lower()

    skills = re.split(
        r"[,;/|]+",
        required_skills
    )

    matched = []

    for skill in skills:

        skill = skill.strip()

        if skill and skill.lower() in resume_lower:

            matched.append(skill)

    return matched


# ============================================================
# MISSING SKILLS
# ============================================================

def get_missing_skills(
    required_skills,
    resume_text
):

    if not required_skills:

        return []

    resume_lower = resume_text.lower()

    skills = re.split(
        r"[,;/|]+",
        required_skills
    )

    missing = []

    for skill in skills:

        skill = skill.strip()

        if skill and skill.lower() not in resume_lower:

            missing.append(skill)

    return missing