# ExamGuard – AI Reporting Architecture and Prompt Design

## 1. Overview

The AI Reporting module of ExamGuard converts examination monitoring data into a structured integrity report for invigilators. It validates session information, summarizes recorded events, identifies relevant evidence, and presents the report for human review.

**Current stage:** Sprint 1 prototype using mock report generation.

## 2. Architecture

The module follows a modular architecture consisting of input validation, prompt design, report generation, mock API integration, and dashboard presentation.

### Data Flow

1. **Monitoring Data Input:** Receives candidate information, session details, integrity score, risk category, and detected events.
2. **Input Validation:** Uses Pydantic models to validate required fields, data types, and permitted values.
3. **Prompt Design:** Defines instructions using LangChain Core's `ChatPromptTemplate`.
4. **Report Generation:** Generates a structured report using predefined Python logic in the current prototype.
5. **Mock API Client:** Simulates communication with the reporting service without requiring a live backend.
6. **Dashboard Presentation:** Displays the report and monitoring events through Streamlit for invigilator review.

### Architecture Diagram

```text
Monitoring Session Data (JSON)
             |
             v
     Pydantic Validation
             |
             v
      Report Service
             |
             v
   Structured Report (JSON)
             |
             v
       Streamlit Dashboard
             |
             v
       Human Invigilator
```

The LangChain prompt template is defined separately and is ready for future integration with a language model. It is not yet connected to the current report-generation flow.

## 3. Input JSON Contract

The reporting service accepts a JSON object containing:

- `candidate_id`: Candidate identifier.
- `session_id`: Examination session identifier.
- `integrity_score`: Integer between 0 and 100.
- `risk_category`: `low`, `moderate`, or `high`.
- `events`: List of recorded monitoring events.

Each event contains an event type, timestamp, severity, confidence value, and optional metadata.

The schema rejects unexpected fields and validates confidence values between 0 and 1.

Refer to `examples/sample_session.json` for the sample input.

## 4. Output JSON Contract

The reporting service returns a structured JSON object containing:

- `candidate_id`: Candidate identifier.
- `session_id`: Examination session identifier.
- `integrity_score`: Validated integrity score.
- `risk_category`: Risk classification.
- `event_summary`: Summary of the recorded events.
- `important_evidence`: List of evidence descriptions derived from event data.
- `ai_summary`: Summary text for the invigilator.
- `review_status`: Initially set to `pending`.

Refer to `examples/sample_output.json` for the sample output.

## 5. Prompt Design

The prompt is defined in `ai_service/prompt_template.py` using LangChain Core's `ChatPromptTemplate`.

### Prompt Objectives

1. Summarize only the information supplied in the session data.
2. Include relevant monitoring events and evidence.
3. Use the provided integrity score and risk category.
4. Avoid inventing candidate details or evidence.
5. Avoid declaring a candidate guilty of misconduct.
6. Recommend human review before making a decision.
7. Produce a structured report consistent with the defined output schema.

### Responsible AI Considerations

The report is intended to support invigilators, not replace their judgment. A risk score or suspicious event alone is not proof of misconduct. Human review is required before any disciplinary decision.

## 6. Testing Strategy

Automated tests are implemented using Pytest.

The tests cover:

- Required report fields.
- Preservation of candidate and session information.
- Evidence generation.
- Sessions with no monitoring events.
- Validation of invalid scores.
- Validation of missing candidate identifiers.
- Mock client functionality.
- Consistency between generated reports and the saved sample output.

The current test suite contains eight tests.

## 7. Current Limitations

- The report service uses deterministic Python logic rather than a live LLM.
- The LangChain prompt is defined but not invoked by the report service.
- The mock client does not connect to an actual backend API.
- Sample monitoring data is used instead of real-time events.
- Dashboard review status is not persisted to a database.

## 8. Future Work

- Integrate a language model through LangChain.
- Connect the service to the backend API.
- Receive monitoring events from the other project teams.
- Add persistent report storage and review history.
- Evaluate the quality, consistency, and reliability of generated reports.

## 9. Sprint 1 Outcome

The prototype establishes a validated input/output contract, a modular reporting service, a LangChain prompt template, a mock API client, automated tests, and a Streamlit invigilator dashboard.
