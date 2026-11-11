import streamlit as st
from app.parser import extract_text
from app.scoring import analyze_resume
from app.recommendations import generate_recommendations

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer")
st.caption("Compare a resume with a job description using transparent, explainable signals.")

with st.sidebar:
    st.header("How scoring works")
    st.write("Skills 40% · Experience indicators 25% · Education indicators 15% · Text relevance 20%")
    st.info("This is a decision-support tool, not a hiring prediction. Missing resume evidence does not prove a candidate lacks a qualification.")

resume_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"])
job_description = st.text_area("Paste job description", height=260, placeholder="Paste the full job description here...")
analyze = st.button("Analyze resume", type="primary", disabled=not (resume_file and job_description.strip()))

if analyze:
    try:
        resume_text = extract_text(resume_file.getvalue(), resume_file.name)
        with st.spinner("Analyzing resume and job description..."):
            result = analyze_resume(resume_text, job_description)
            recommendations = generate_recommendations(result, resume_text, job_description)

        st.divider()
        left, right = st.columns([1, 2])
        with left:
            st.metric("Overall match score", f"{result['overall_score']}/100")
            st.progress(result["overall_score"] / 100)
        with right:
            st.subheader("Score breakdown")
            cols = st.columns(4)
            for col, (name, score) in zip(cols, result["component_scores"].items()):
                col.metric(name.title(), f"{score:.0f}%")

        st.subheader("Skills comparison")
        a, b = st.columns(2)
        with a:
            st.markdown("**Matched skills**")
            st.success(", ".join(result["matched_skills"]) if result["matched_skills"] else "No recognized matching skills found.")
        with b:
            st.markdown("**Skills not found in resume**")
            st.warning(", ".join(result["missing_skills"]) if result["missing_skills"] else "No recognized skill gaps.")
        with st.expander("Evidence found in resume"):
            if result["skill_evidence"]:
                for skill, evidence in result["skill_evidence"].items():
                    st.write(f"**{skill}:** {evidence}")
            else:
                st.write("No matched-skill evidence lines found.")

        st.subheader("Recommendations")
        st.markdown(recommendations)

        with st.expander("Scoring methodology and limitations"):
            st.write("Weighted score = skills × 0.40 + experience indicators × 0.25 + education indicators × 0.15 + relevance × 0.20.")
            st.write(f"Relevance method: {result['similarity_method']}")
            for item in result["limitations"]:
                st.write(f"- {item}")

        st.download_button(
            "Download analysis as JSON",
            data=__import__("json").dumps(result, indent=2),
            file_name="resume_analysis.json",
            mime="application/json",
        )
    except Exception as exc:
        st.error(str(exc))
