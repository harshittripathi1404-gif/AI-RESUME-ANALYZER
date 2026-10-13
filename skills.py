import re

SKILLS = {
    "python": ["python", "python programming"],
    "java": ["java", "java programming"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "data structures": ["data structures", "dsa"],
    "algorithms": ["algorithms", "algorithm design"],
    "git": ["git", "github", "git version control"],
    "rest apis": ["rest api", "rest apis", "restful api"],
    "backend development": ["backend development", "back-end development"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "react": ["react", "reactjs"],
    "mongodb": ["mongodb", "mongo db"],
    "problem solving": ["problem-solving", "problem solving"],
    "software development": ["software development"],
    "operating systems": ["operating systems", "os"],
    "computer networks": ["computer networks"],
}


def extract_skills(text):
    text = text.lower()
    found = set()

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            if re.search(pattern, text):
                found.add(skill)
                break

    return sorted(found)