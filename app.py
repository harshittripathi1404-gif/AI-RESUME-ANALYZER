import streamlit as st
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from resume_parser import extract_text_from_pdf
from skills import extract_skills
from matcher import get_skill_analysis


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
# PREMIUM UI THEME
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #080D1C 0%, #11152B 55%, #1A1235 100%);
    color: #F4F6FF;
}

/* Main content width and spacing */
.block-container {
    max-width: 1050px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Headings */
h1 {
    color: #FFFFFF !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}
h2, h3 {
    color: #E6E9FF !important;
    font-weight: 700 !important;
}

/* Normal text */
.stApp p, .stApp label {
    color: #D0D6EA;
}

/* Cards and sections */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(151,140,255,0.22);
    border-radius: 18px;
    padding: 18px;
}

/* File uploader */
div[data-testid="stFileUploader"] {
    background: rgba(105, 95, 220, 0.09);
    border: 1px dashed #8176FF;
    border-radius: 16px;
    padding: 15px;
}

/* Job description input */
.stTextArea textarea {
    background-color: #141A30 !important;
    color: #FFFFFF !important;
    border: 1px solid #424A70 !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #6557F5, #9270FF);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.3rem;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #796DFF, #A184FF);
    transform: translateY(-2px);
    box-shadow: 0 7px 24px rgba(112, 91, 255, 0.3);
}

/* Metrics */
div[data-testid="stMetric"] {
    background: rgba(105, 95, 220, 0.12);
    border: 1px solid rgba(151,140,255,0.25);
    padding: 18px;
    border-radius: 16px;
}
div[data-testid="stMetricLabel"] {
    color: #C6CBE4 !important;
}
div[data-testid="stMetricValue"] {
    color: #B7A6FF !important;
    font-weight: 800;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6557F5, #A184FF);
}

/* Success message */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0B1022;
    border-right: 1px solid #252B48;
}

/* Smooth appearance */
.stApp, .stButton, textarea {
    transition: all 0.2s ease;
}
</style>
""", unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer")
st.caption("Compare your resume with a job description.")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"]
)

job_description = st.text_area(
    "Job Description",
    placeholder="Paste the complete job description here...",
    height=180
)


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
        f"<b>Report Date:</b> {__import__('datetime').date.today().strftime('%d %B %Y')}",
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

    content.append(Paragraph("Improvement Suggestions", styles["Heading2"]))

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
     


if st.button("Analyze Resume", type="primary"):
    if resume is None:
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter the job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):
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

                    st.success("Analysis completed!")

                    st.subheader("Resume Analysis Results")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Skill Match Score",
                        f"{result['score']}%"
                    )
                    col2.metric(
                        "Matched Skills",
                        len(result["matched"])
                    )
                    col3.metric(
                        "Missing Skills",
                        len(result["missing"])
                    )

                    st.progress(result["score"] / 100)

                    left, right = st.columns(2)

                    with left:
                        st.subheader("✅ Matched Skills")
                        if result["matched"]:
                            for skill in result["matched"]:
                                st.write(f"• {skill}")
                        else:
                            st.write("No matching skills identified.")

                    with right:
                        st.subheader("📌 Missing Skills")
                        if result["missing"]:
                            for skill in result["missing"]:
                                st.write(f"• {skill}")
                        else:
                            st.write("No identified skills are missing.")

                    st.subheader("💡 Improvement Suggestions")

                    if result["missing"]:
                        st.write(
                            "Review these skills and learn or highlight "
                            "them where relevant to your actual experience:"
                        )
                        for skill in result["missing"]:
                            st.write(f"• {skill}")
                    else:
                        st.write(
                            "Your resume contains all skills identified "
                            "in this job description."
                        )

                    pdf_bytes = create_pdf_report(result)

                    st.download_button(
                        "📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name="resume_analysis_report.pdf",
                        mime="application/pdf"
                    )

                    with st.expander("View extracted resume text"):
                        st.text(resume_text)

        except Exception as error:
            st.error(
                "Analysis failed. Check whether the uploaded file is "
                "valid and readable."
            )
            st.caption(f"Technical details: {error}")
