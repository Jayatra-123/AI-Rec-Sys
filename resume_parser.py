# ============================================================
# AI RECRUITMENT SYSTEM
# RESUME PARSER
# ============================================================

import os
import pdfplumber
from docx import Document


# ============================================================
# READ PDF RESUME
# ============================================================

def read_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    except Exception as e:

        print("PDF reading error:", e)

        return ""


# ============================================================
# READ DOCX RESUME
# ============================================================

def read_docx(file_path):
    """
    Extract text from a DOCX resume.
    """

    text = ""

    try:

        document = Document(file_path)

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                text += paragraph.text + "\n"

        return text.strip()

    except Exception as e:

        print("DOCX reading error:", e)

        return ""


# ============================================================
# READ RESUME
# ============================================================

def read_resume(file_path):
    """
    Automatically detects PDF or DOCX
    and extracts the text.
    """

    if not file_path:
        return ""

    if not os.path.exists(file_path):
        return ""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        return read_pdf(file_path)

    elif extension == ".docx":

        return read_docx(file_path)

    else:

        return ""


# ============================================================
# EXTRACT BASIC INFORMATION
# ============================================================

def extract_email(text):

    import re

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    result = re.search(pattern, text)

    if result:
        return result.group(0)

    return ""


def extract_phone(text):

    import re

    patterns = [
        r"\+?\d[\d\s\-]{8,14}\d",
        r"\d{10}"
    ]

    for pattern in patterns:

        result = re.search(pattern, text)

        if result:
            return result.group(0)

    return ""


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):

    common_skills = [

        "python",
        "java",
        "c++",
        "c",
        "sql",
        "mysql",
        "oracle",
        "excel",
        "power bi",
        "tableau",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "data analysis",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "flask",
        "django",
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "communication",
        "leadership",
        "teamwork",
        "project management",
        "financial analysis",
        "accounting",
        "accounts payable",
        "accounts receivable",
        "treasury",
        "cash management",
        "sap",
        "quickbooks"
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in common_skills:

        if skill in text_lower:

            found_skills.append(skill.title())

    return ", ".join(found_skills)


# ============================================================
# EXTRACT EXPERIENCE
# ============================================================

def extract_experience(text):

    import re

    text_lower = text.lower()

    patterns = [

        r"(\d+)\+?\s*years?\s*(?:of)?\s*experience",

        r"experience\s*[:\-]?\s*(\d+)\+?\s*years?",

        r"(\d+)\s*years?\s*working"
    ]

    for pattern in patterns:

        result = re.search(pattern, text_lower)

        if result:

            try:
                return int(result.group(1))

            except:
                pass

    return 0