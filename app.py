import streamlit as st
from pathlib import Path

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
# SAMPLE DATA CONFIG
# ----------------------------

SAMPLE_DIR = Path(__file__).parent / "sample_data"

SAMPLE_TRANSCRIPT = SAMPLE_DIR / "Sample_Earnings_Call_Transcript.pdf"
SAMPLE_NOTES = SAMPLE_DIR / "Sample_Analyst_Notes.pdf"
SAMPLE_MODEL = SAMPLE_DIR / "Illustrative_RetailCo_Integrated_Financial_Model.xlsx"


# ----------------------------
# HELPER FUNCTIONS
# ----------------------------

def run_analysis(transcript_file, excel_file, notes_file=None):
    """Run the existing parsing + Gemini analysis pipeline."""

    progress = st.progress(0)

    progress.progress(15, text="Reading Earnings Call...")

    transcript_text = extract_pdf_text(transcript_file)

    progress.progress(35, text="Reading Financial Model...")

    excel_text = extract_excel_data(excel_file)

    progress.progress(50, text="Reading Analyst Notes...")

    notes_text = ""

    if notes_file is not None:
        notes_text = extract_pdf_text(notes_file)

    progress.progress(70, text="Analyzing with Gemini...")

    result = analyze_documents(
        transcript_text,
        notes_text,
        excel_text
    )

    progress.progress(100, text="Analysis Complete!")

    return result


def load_sample_files():
    """Open the bundled sample files for one-click demo analysis."""

    required_files = [
        SAMPLE_TRANSCRIPT,
        SAMPLE_MODEL,
        SAMPLE_NOTES
    ]

    missing = [str(path) for path in required_files if not path.exists()]

    if missing:
        return None, None, None, missing

    transcript_file = open(SAMPLE_TRANSCRIPT, "rb")
    model_file = open(SAMPLE_MODEL, "rb")
    notes_file = open(SAMPLE_NOTES, "rb")

    return transcript_file, model_file, notes_file, []


# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:

    st.title("📈 Financial Model Impact Analyzer")

    st.markdown("---")

    st.markdown("""
### What it does

Analyzes:

- Earnings call transcripts
- Financial models
- Analyst / hedge fund notes

and identifies **forecast assumptions and model cells likely to be impacted**.

### Built With

- Gemini 2.5 Flash
- Python
- Streamlit
- PyMuPDF
- OpenPyXL
""")

    st.markdown("---")

    st.caption("Created by **Arnav Okhade**")


# ----------------------------
# HEADER
# ----------------------------

st.title("📈 Financial Model Impact Analyzer")

st.markdown("""
AI-powered analysis of **earnings calls**, **financial models**, and **analyst notes**.

The agent identifies:

- Forecast assumptions likely to change
- Financial model cells impacted
- Supporting transcript evidence
- Confidence level
- Derived downstream impacts
""")


# ----------------------------
# SAMPLE DEMO
# ----------------------------

st.markdown("---")

st.subheader("🧪 Try the Agent with Sample Data")

st.markdown("""
Don't have an earnings call, financial model, and analyst notes handy?

Use the **illustrative sample dataset** below to test the complete workflow in one click.
The sample model contains quarterly historical and forecast periods, operating drivers,
an integrated P&L, balance sheet, cash flow, working capital, valuation and linked formulas.
""")

sample_col1, sample_col2 = st.columns([2, 1])

with sample_col1:

    if st.button(
        "🚀 Run Complete Sample Analysis",
        use_container_width=True,
        type="primary"
    ):

        transcript_file, model_file, notes_file, missing = load_sample_files()

        if missing:

            st.error(
                "Sample files are missing from the deployment. "
                "Make sure the `sample_data` folder is present in the GitHub repository."
            )

            for file in missing:
                st.code(file)

        else:

            st.info(
                "Running the agent on the bundled illustrative RetailCo dataset..."
            )

            try:

                result = run_analysis(
                    transcript_file,
                    model_file,
                    notes_file
                )

                st.session_state["analysis_result"] = result
                st.session_state["analysis_source"] = "Sample Dataset"

                st.success("✅ Sample analysis complete!")

            except Exception as e:

                st.error("The sample analysis failed.")

                st.exception(e)

            finally:

                transcript_file.close()
                model_file.close()
                notes_file.close()


with sample_col2:

    st.markdown("**Sample dataset includes:**")

    st.markdown("""
    📄 Earnings Call — 3 pages  
    📊 Financial Model — 12 sheets  
    📝 Analyst Notes — 2 pages
    """)


# ----------------------------
# SAMPLE FILE DOWNLOADS
# ----------------------------

with st.expander("📥 Download the sample files"):

    st.caption(
        "These files are illustrative demo data created for testing the agent. "
        "They are not actual company financial data."
    )

    if SAMPLE_TRANSCRIPT.exists():

        with open(SAMPLE_TRANSCRIPT, "rb") as f:
            st.download_button(
                "📄 Earnings Call Transcript",
                data=f.read(),
                file_name=SAMPLE_TRANSCRIPT.name,
                mime="application/pdf",
                use_container_width=True
            )

    if SAMPLE_MODEL.exists():

        with open(SAMPLE_MODEL, "rb") as f:
            st.download_button(
                "📊 Financial Model",
                data=f.read(),
                file_name=SAMPLE_MODEL.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    if SAMPLE_NOTES.exists():

        with open(SAMPLE_NOTES, "rb") as f:
            st.download_button(
                "📝 Analyst Notes",
                data=f.read(),
                file_name=SAMPLE_NOTES.name,
                mime="application/pdf",
                use_container_width=True
            )


# ----------------------------
# FILE UPLOADS
# ----------------------------

st.markdown("---")

st.subheader("📂 Analyze Your Own Files")

col1, col2, col3 = st.columns(3)

with col1:

    transcript = st.file_uploader(
        "📄 Earnings Call Transcript",
        type=["pdf"],
        key="transcript_upload"
    )

with col2:

    excel = st.file_uploader(
        "📊 Financial Model",
        type=["xlsx", "xlsm"],
        key="excel_upload"
    )

with col3:

    notes = st.file_uploader(
        "📝 Analyst Notes (Optional)",
        type=["pdf"],
        key="notes_upload"
    )

st.markdown("")


# ----------------------------
# ANALYZE UPLOADED FILES
# ----------------------------

if st.button(
    "🚀 Analyze Uploaded Files",
    use_container_width=True
):

    if transcript and excel:

        try:

            result = run_analysis(
                transcript,
                excel,
                notes
            )

            st.session_state["analysis_result"] = result
            st.session_state["analysis_source"] = "Uploaded Files"

            st.success("✅ Analysis Complete")

        except Exception as e:

            st.error("The analysis failed.")

            st.exception(e)

    else:

        st.error(
            "Please upload the Earnings Call Transcript and Financial Model."
        )


# ----------------------------
# RESULTS
# ----------------------------

if "analysis_result" in st.session_state:

    st.markdown("---")

    source = st.session_state.get(
        "analysis_source",
        "Analysis"
    )

    st.subheader(f"📊 AI Analysis — {source}")

    st.markdown(
        st.session_state["analysis_result"]
    )
