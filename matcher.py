def get_skill_analysis(resume_skills, job_skills):
    resume_skills = {s.lower().strip() for s in resume_skills}
    job_skills = {s.lower().strip() for s in job_skills}

    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills - resume_skills)

    if not job_skills:
        score = 0
    else:
        score = round(len(matched) / len(job_skills) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }