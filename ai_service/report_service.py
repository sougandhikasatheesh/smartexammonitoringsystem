
from .report_schema import SessionInput, IntegrityReport


def generate_report(session_data: dict) -> dict:
    # Step 1: Validate incoming session data
    session = SessionInput.model_validate(session_data)

    # Step 2: Summarize the recorded events
    event_count = len(session.events)

    if event_count == 0:
        event_summary = "No monitoring events were recorded."
        evidence = []
        ai_summary = (
            "No monitoring events were recorded during this session. "
            "Continue to follow the normal review procedure."
        )
    else:
        event_summary = (
            f"{event_count} monitoring event(s) were recorded."
        )

        evidence = []

        for event in session.events:
            description = (
                f"{event.event_type.replace('_', ' ').title()} "
                f"(severity: {event.severity}, "
                f"confidence: {event.confidence:.2f})"
            )

            duration = event.metadata.get("duration_seconds")
            if isinstance(duration, (int, float)) and not isinstance(duration, bool):
                description += f", duration: {duration} seconds"

            evidence.append(description)

        ai_summary = (
            f"The session has an integrity score of "
            f"{session.integrity_score}/100 and is classified as "
            f"{session.risk_category} risk. "
            f"{event_count} monitoring event(s) were recorded. "
            "The invigilator should review the available evidence "
            "before making a decision. These events alone do not "
            "establish misconduct."
        )

    # Step 3: Create a report matching the output schema
    report = IntegrityReport(
        candidate_id=session.candidate_id,
        session_id=session.session_id,
        integrity_score=session.integrity_score,
        risk_category=session.risk_category,
        event_summary=event_summary,
        important_evidence=evidence,
        ai_summary=ai_summary,
        review_status="pending",
    )

    # Step 4: Return JSON-compatible data
    return report.model_dump()
