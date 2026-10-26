
import json
from pathlib import Path

import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = PROJECT_ROOT / "examples" / "sample_session.json"
API_URL = "http://127.0.0.1:5000/api/v1"

st.set_page_config(page_title="ExamGuard", page_icon="🛡️", layout="wide")
st.title("ExamGuard — Smart Exam Monitoring")
st.caption("Sprint 2 | Login, Exam Selection and Session Management")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "candidate" not in st.session_state:
    st.session_state.candidate = None
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "login_cookie" not in st.session_state:
    st.session_state.login_cookie = None

if not st.session_state.logged_in:
    st.subheader("Candidate Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": email, "password": password},
                timeout=10,
            )
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.candidate = response.json()["candidate"]
                st.session_state.login_cookie = response.cookies.get("session")
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(response.json().get("error", "Login failed"))
        except requests.RequestException as error:
            st.error(f"Cannot connect to backend: {error}")

    st.stop()

candidate = st.session_state.candidate
st.success(f"Logged in as {candidate['name']}")

if st.button("Logout"):
    try:
        requests.post(
            f"{API_URL}/auth/logout",
            cookies={"session": st.session_state.login_cookie}
            if st.session_state.login_cookie else {},
            timeout=10,
        )
    except requests.RequestException:
        pass
    st.session_state.logged_in = False
    st.session_state.candidate = None
    st.session_state.login_cookie = None
    st.session_state.session_id = None
    st.rerun()

st.subheader("Candidate Details")
st.write(f"**Name:** {candidate['name']}")
st.write(f"**Email:** {candidate['email']}")
st.write(f"**Candidate ID:** {candidate['id']}")

cookies = (
    {"session": st.session_state.login_cookie}
    if st.session_state.login_cookie else {}
)

st.subheader("Available Exams")

try:
    response = requests.get(f"{API_URL}/exams", timeout=10)
    response.raise_for_status()
    exams = response.json().get("exams", [])

    if not exams:
        st.info("No exams are available.")
    else:
        exam_options = {
            f"{exam['title']} — {exam['duration_minutes']} minutes (ID: {exam['id']})": exam
            for exam in exams
        }
        selected_label = st.selectbox(
            "Select an exam",
            list(exam_options.keys()),
        )
        selected_exam = exam_options[selected_label]

        st.write(f"**Description:** {selected_exam.get('description') or 'No description'}")

        if st.button("Start Exam", type="primary"):
            try:
                start_response = requests.post(
                    f"{API_URL}/sessions/start",
                    json={"exam_id": selected_exam["id"]},
                    cookies=cookies,
                    timeout=10,
                )
                if start_response.status_code == 201:
                    result = start_response.json()
                    st.session_state.session_id = result["session_id"]
                    st.success("Exam session started!")
                else:
                    st.error(
                        start_response.json().get(
                            "error", "Could not start the exam"
                        )
                    )
            except requests.RequestException as error:
                st.error(f"Session request failed: {error}")

except requests.RequestException as error:
    st.error(f"Could not load exams: {error}")

if st.session_state.session_id:
    st.subheader("Active Session")
    st.write(f"**Session ID:** {st.session_state.session_id}")
    st.write(f"**Exam:** {selected_exam['title']}")
    st.write("**Status:** In progress")

st.divider()
st.subheader("Mock Report Preview")

try:
    with SAMPLE_PATH.open("r", encoding="utf-8") as file:
        sample_data = json.load(file)
    st.json(sample_data)
except (OSError, json.JSONDecodeError) as error:
    st.error(f"Could not load sample report data: {error}")
