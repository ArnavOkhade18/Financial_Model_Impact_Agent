import streamlit as st
from parser import extract_pdf_text
from excel_parser import extract_excel_data
from llm import analyze_documents

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Financial Model Impact Analyzer",
    page_icon="📈",
    layout="wide"
)

# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:

    st.title("📈 Financial Model Impact Analyzer")

    st.markdown("---")

    st.markdown("""
### Built With

- Gemini 2.5 Flash
- Python
- Streamlit
- PyMuPDF
- OpenPyXL

---
Created by

**Arnav Okhade**
""")

# ----------------------------
# HEADER
# ----------------------------

st.title("📈 Financial Model Impact Analyzer")

st.markdown("""
AI-powered analysis of **earnings call transcripts**, **financial models**, and **analyst notes**.

The AI identifies:

- Forecast assumptions likely to change
- Financial model cells impacted
- Supporting evidence from transcripts
- Confidence level
- Derived downstream impacts

---
""")

# ----------------------------
# FILE UPLOADS
# ----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    transcript = st.file_uploader(
        "📄 Earnings Call Transcript",
        type=["pdf"]
    )

with col2:

    excel = st.file_uploader(
        "📊 Financial Model",
        type=["xlsx", "xlsm"]
    )

with col3:

    notes = st.file_uploader(
        "📝 Analyst Notes (Optional)",
        type=["pdf"]
    )

st.markdown("")

# ----------------------------
# ANALYZE BUTTON
# ----------------------------

analyze = st.button(
    "🚀 Analyze Financial Model",
    use_container_width=True
)

# ----------------------------
# ANALYSIS
# ----------------------------

if analyze:

    if transcript and excel:

        progress = st.progress(0)

        progress.progress(15, text="Reading Earnings Call...")

        transcript_text = extract_pdf_text(transcript)

        progress.progress(35, text="Reading Financial Model...")

        excel_text = extract_excel_data(excel)

        progress.progress(50, text="Reading Analyst Notes...")

        notes_text = ""

        if notes:
            notes_text = extract_pdf_text(notes)

        progress.progress(70, text="Analyzing with Gemini...")

        result = analyze_documents(
            transcript_text,
            notes_text,
            excel_text
        )

        progress.progress(100, text="Analysis Complete!")

        st.success("✅ Analysis Complete")

        st.markdown("---")

        st.subheader("📊 AI Analysis")

        st.markdown(result)

    else:

        st.error("Please upload the Earnings Call Transcript and Financial Model.")
