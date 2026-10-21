
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_service.report_service import generate_report
from ai_service.mock_client import post_report


SAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "sample_session.json"
)


@pytest.fixture
def sample_session():
    with SAMPLE_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def test_report_has_required_fields(sample_session):
    report = generate_report(sample_session)

    required_fields = {
        "candidate_id",
        "session_id",
        "integrity_score",
        "risk_category",
        "event_summary",
        "important_evidence",
        "ai_summary",
        "review_status",
    }

    assert required_fields == set(report.keys())


def test_report_preserves_session_information(sample_session):
    report = generate_report(sample_session)

    assert report["candidate_id"] == "CAND-001"
    assert report["session_id"] == "SES-001"
    assert report["integrity_score"] == 65
    assert report["risk_category"] == "moderate"


def test_report_contains_evidence(sample_session):
    report = generate_report(sample_session)

    assert len(report["important_evidence"]) == 2
    assert "Face Absent" in report["important_evidence"][0]
    assert report["review_status"] == "pending"


def test_empty_events_are_handled(sample_session):
    sample_session["events"] = []

    report = generate_report(sample_session)

    assert report["important_evidence"] == []
    assert "No monitoring events" in report["event_summary"]


def test_invalid_score_is_rejected(sample_session):
    sample_session["integrity_score"] = 150

    with pytest.raises(ValidationError):
        generate_report(sample_session)


def test_missing_candidate_id_is_rejected(sample_session):
    del sample_session["candidate_id"]

    with pytest.raises(ValidationError):
        generate_report(sample_session)


def test_mock_client_returns_report(sample_session):
    report = post_report(sample_session)

    assert report["session_id"] == sample_session["session_id"]
    assert report["review_status"] == "pending"


def test_report_matches_output_contract():
    from pathlib import Path
    import json

    project_root = Path(__file__).resolve().parents[1]

    with (project_root / "examples" / "sample_session.json").open(
        "r", encoding="utf-8"
    ) as file:
        input_data = json.load(file)

    with (project_root / "examples" / "sample_output.json").open(
        "r", encoding="utf-8"
    ) as file:
        expected_output = json.load(file)

    actual_output = generate_report(input_data)

    assert actual_output == expected_output
