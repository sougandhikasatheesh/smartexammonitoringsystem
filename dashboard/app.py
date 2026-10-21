
import json
import sys
from pathlib import Path

import streamlit as st

# Add the project root so Python can import ai_service.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ai_service import generate_report


SAMPLE_PATH = PROJECT_ROOT / "examples" / "sample_session.json"


st.set_page_config(
    page_title="ExamGuard | AI Reporting",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ ExamGuard")
st.subheader("Smart Exam Monitoring — Invigilator Dashboard")

st.caption(
    "Sprint 1 prototype | Sample data | Mock report generation"
)


def load_sample_session():
    with SAMPLE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


# Load the fictional exam session.
try:
    session_data = load_sample_session()
    report = generate_report(session_data)

except Exception as error:
    st.error(f"Unable to load or generate the report: {error}")
    st.stop()


# Candidate information
st.markdown("### Candidate Information")

info1, info2 = st.columns(2)

info1.text_input(
    "Candidate ID",
    value=report["candidate_id"],
    disabled=True,
)

info2.text_input(
    "Session ID",
    value=report["session_id"],
    disabled=True,
)


# Session metrics
st.markdown("### Session Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Integrity Score",
    f'{report["integrity_score"]}/100',
)

col2.metric(
    "Risk Category",
    report["risk_category"].title(),
)

col3.metric(
    "Events Recorded",
    len(session_data["events"]),
)


# Observed events
st.markdown("### Observed Events")

if session_data["events"]:
    for index, event in enumerate(session_data["events"], start=1):
        with st.expander(
            f'{index}. {event["event_type"].replace("_", " ").title()}'
        ):
            st.write(f'**Timestamp:** {event["timestamp"]}')
            st.write(f'**Severity:** {event["severity"].title()}')
            st.write(f'**Confidence:** {event["confidence"]:.2f}')
            st.json(event.get("metadata", {}))
else:
    st.info("No monitoring events were recorded.")


# Report summary
st.markdown("### Integrity Report")

st.write("**Event Summary**")
st.write(report["event_summary"])

st.write("**Important Evidence**")

if report["important_evidence"]:
    for evidence in report["important_evidence"]:
        st.write(f"- {evidence}")
else:
    st.write("No evidence items were recorded.")

st.write("**AI-Style Summary**")
st.info(report["ai_summary"])

st.caption(
    "This is a deterministic mock summary, not a live AI-generated response."
)


# Human review section
st.markdown("### Invigilator Review")

if "review_status" not in st.session_state:
    st.session_state.review_status = "Pending"

st.write(f"**Review Status:** {st.session_state.review_status}")

review_col1, review_col2 = st.columns(2)

with review_col1:
    if st.button("Mark as Reviewed", use_container_width=True):
        st.session_state.review_status = "Reviewed"

with review_col2:
    if st.button("Keep Pending", use_container_width=True):
        st.session_state.review_status = "Pending"

st.caption(
    "Review status is stored only for the current Streamlit session. "
    "It is not saved to a database."
)
