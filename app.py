import streamlit as st
from io import BytesIO
from xml.sax.saxutils import escape
from datetime import date

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from resume_parser import extract_text_from_pdf
from skills import extract_skills
from matcher import get_skill_analysis


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ---------------- PREMIUM DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080D1C;
    --panel: rgba(20, 27, 55, 0.82);
    --border: rgba(158, 153, 255, 0.24);
    --text: #F5F6FF;
    --muted: #AEB8D6;
    --purple: #8B70FF;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(72, 89, 220, .24), transparent 38%),
        radial-gradient(ellipse at 95% 45%, rgba(133, 63, 218, .20), transparent 38%),
        linear-gradient(140deg, #080D1C, #11152B 55%, #17112F);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1080px;
    padding: 2rem 1.5rem 4rem;
}

h1, h2, h3 {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

h1 {
    font-size: clamp(2.3rem, 5vw, 3.5rem) !important;
    line-height: 1.15 !important;
    font-weight: 800 !important;
    letter-spacing: -1.8px;
}

h2 {
    font-size: 1.65rem !important;
    font-weight: 750 !important;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    color: #D9DDF0;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* Hero card */
.hero-card {
    padding: 30px 30px 26px;
    border-radius: 24px;
    border: 1px solid var(--border);
    background: linear-gradient(
        130deg,
        rgba(63, 79, 167, .24),
        rgba(91, 55, 145, .15)
    );
    box-shadow: 0 18px 60px rgba(0, 0, 0, .15);
    margin-bottom: 24px;
}

.eyebrow {
    color: #B8A8FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: .75rem;
    font-weight: 800;
    margin-bottom: 12px;
}

.hero-subtitle {
    color: #CBD3ED;
    font-size: 1.05rem;
    line-height: 1.8;
    max-width: 680px;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 22px;
}

.pill {
    padding: 8px 12px;
    border: 1px solid rgba(172, 162, 255, .25);
    background: rgba(255, 255, 255, .045);
    border-radius: 30px;
    color: #E5E2FF;
    font-size: .82rem;
}

/* Form and result cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 15px 45px rgba(0, 0, 0, .12);
}

/* Uploader */
div[data-testid="stFileUploader"] {
    background: rgba(91, 85, 188, .10);
    border: 1px dashed rgba(170, 157, 255, .7);
    border-radius: 16px;
    padding: 14px;
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

div[data-testid="stFileUploader"] button {
    border-radius: 10px;
}

/* Job description */
.stTextArea textarea {
    background: #0D142A !important;
    color: #FFFFFF !important;
    border: 1px solid #394267 !important;
    border-radius: 15px !important;
    padding: 14px !important;
    font-size: .95rem !important;
}

.stTextArea textarea:focus {
    border-color: #9A85FF !important;
    box-shadow: 0 0 0 2px rgba(139, 112, 255, .14) !important;
}

.stTextArea textarea::placeholder {
    color: #8994B5 !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #6557F5, #8967F8 58%, #A579FF);
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, .14);
    border-radius: 13px;
    min-height: 47px;
    font-weight: 750;
    box-shadow: 0 7px 25px rgba(105, 83, 245, .22);
    transition: all .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #C6BBFF;
    box-shadow: 0 9px 30px rgba(125, 100, 255, .36);
    transform: translateY(-2px);
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(105, 95, 220, .16), rgba(143, 93, 235, .07));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 20px;
}

div[data-testid="stMetricLabel"] {
    color: #C6CBE4 !important;
}

div[data-testid="stMetricValue"] {
    color: #B9AAFF !important;
    font-weight: 800 !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6557F5, #B17CFF);
    border-radius: 10px;
}

/* Alerts and expander */
div[data-testid="stAlert"],
div[data-testid="stExpander"] {
    border-radius: 14px;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, .025);
}

/* Footer */
.app-footer {
    text-align: center;
    color: #8792B4;
    font-size: .82rem;
    padding-top: 32px;
    margin-top: 35px;
    border-top: 1px solid rgba(158, 153, 255, .15);
}

section[data-testid="stSidebar"] {
    background: #0B1022;
    border-right: 1px solid #252B48;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1.1rem .9rem 2rem;
    }

    .hero-card {
        padding: 22px 18px;
    }

    h1 {
        letter-spacing: -1px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-card">
    <div class="eyebrow">✦ Smart Career Toolkit</div>
    <h1>AI Resume Analyzer</h1>
    <div class="hero-subtitle">
        Discover how well your resume matches your dream job.
        Identify skill gaps, understand your strengths, and take
        the next step in your career with confidence.
    </div>
    <div class="pill-row">
        <span class="pill">📄 Resume Analysis</span>
        <span class="pill">🎯 Skill Matching</span>
        <span class="pill">💡 Improvement Tips</span>
        <span class="pill">📥 PDF Report</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- INPUT SECTION ----------------
with st.container(border=True):
    st.subheader("🚀 Start Your Analysis")
    st.caption("Upload your resume and paste the job description below.")

    resume = st.file_uploader(
        "📄 Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Choose the resume you want to compare with a job description."
    )

    job_description = st.text_area(
        "💼 Job Description",
        placeholder="Paste the complete job description here...",
        height=190
    )

    analyze_clicked = st.button(
        "✨ Analyze My Resume",
        type="primary",
        use_container_width=True
    )


# ---------------- PDF REPORT ----------------
def create_pdf_report(result):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    content = []

    styles["Title"].textColor = "#245A81"
    styles["Title"].fontSize = 22

    content.append(Paragraph("AI Resume Analyzer", styles["Title"]))
    content.append(Paragraph(
        "Resume and Job Description Match Report",
        styles["Normal"]
    ))
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        f"<b>Report Date:</b> {date.today().strftime('%d %B %Y')}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 15))

    content.append(Paragraph(
        f"Skill Match Score: {result['score']}%",
        styles["Heading1"]
    ))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Matched Skills", styles["Heading2"]))
    matched = ", ".join(result["matched"]) or "None identified"
    content.append(Paragraph(escape(matched), styles["BodyText"]))
    content.append(Spacer(1, 14))

    content.append(Paragraph("Missing Skills", styles["Heading2"]))
    missing = ", ".join(result["missing"]) or "None identified"
    content.append(Paragraph(escape(missing), styles["BodyText"]))
    content.append(Spacer(1, 14))

    content.append(Paragraph(
        "Improvement Suggestions", styles["Heading2"]
    ))

    if result["missing"]:
        for skill in result["missing"]:
            content.append(Paragraph(
                f"Review {escape(skill)} and add it to your resume "
                "only if you genuinely have this skill.",
                styles["BodyText"]
            ))
            content.append(Spacer(1, 6))
    else:
        content.append(Paragraph(
            "All identified job-description skills were matched.",
            styles["BodyText"]
        ))

    content.append(Spacer(1, 18))
    content.append(Paragraph(
        "Note: This score reflects keyword-based skill matching, "
        "not a guarantee of interview selection.",
        styles["Italic"]
    ))

    doc.build(content)
    return buffer.getvalue()


# ---------------- ANALYSIS ----------------
if analyze_clicked:
    if resume is None:
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter the job description.")

    else:
        try:
            with st.spinner("✨ Analyzing your resume..."):
                resume_text = extract_text_from_pdf(resume)
                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

                if not resume_text.strip():
                    st.error(
                        "No readable text found. If this is a scanned PDF, "
                        "OCR may be required."
                    )

                elif not job_skills:
                    st.warning(
                        "No supported skills found in the job description. "
                        "Try adding more technical skill keywords."
                    )

                else:
                    result = get_skill_analysis(
                        resume_skills, job_skills
                    )

                    st.success("Analysis completed successfully!")

                    st.markdown("## 📊 Your Analysis Results")
                    st.caption(
                        "Here is how your resume compares with the job description."
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "🎯 Skill Match Score",
                        f"{result['score']}%"
                    )
                    col2.metric(
                        "✅ Matched Skills",
                        len(result["matched"])
                    )
                    col3.metric(
                        "📌 Missing Skills",
                        len(result["missing"])
                    )

                    st.progress(
                        max(0.0, min(1.0, float(result["score"]) / 100))
                    )

                    left, right = st.columns(2)

                    with left:
                        with st.container(border=True):
                            st.subheader("✅ Matched Skills")

                            if result["matched"]:
                                for skill in result["matched"]:
                                    st.markdown(f"- 🟢 {skill}")
                            else:
                                st.write("No matching skills identified.")

                    with right:
                        with st.container(border=True):
                            st.subheader("📌 Missing Skills")

                            if result["missing"]:
                                for skill in result["missing"]:
                                    st.markdown(f"- 🟠 {skill}")
                            else:
                                st.write(
                                    "No identified skills are missing."
                                )

                    with st.container(border=True):
                        st.subheader("💡 Improvement Suggestions")

                        if result["missing"]:
                            st.write(
                                "Review these skills and learn or highlight "
                                "them where relevant to your actual experience:"
                            )

                            for skill in result["missing"]:
                                st.markdown(f"- **{skill}**")

                        else:
                            st.write(
                                "Your resume contains all skills identified "
                                "in this job description."
                            )

                    pdf_bytes = create_pdf_report(result)

                    st.download_button(
                        "📥 Download Your PDF Report",
                        data=pdf_bytes,
                        file_name="resume_analysis_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                    with st.expander("🔍 View extracted resume text"):
                        st.text(resume_text)

        except Exception as error:
            st.error(
                "Analysis failed. Check whether the uploaded file is "
                "valid and readable."
            )
            st.caption(f"Technical details: {error}")


# ---------------- FOOTER ----------------
st.markdown("""
<div class="app-footer">
    Built with Python & Streamlit · AI Resume Analyzer
    <br>
    Your career journey, one skill at a time.
</div>
""", unsafe_allow_html=True)
