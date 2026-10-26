# ExamGuard – Smart Exam Monitoring System

## Project Overview
ExamGuard is a Smart Exam Monitoring System designed to support online examination integrity through monitoring, risk analysis, and AI-assisted reporting. It helps invigilators review suspicious events using structured reports.

## Sprint 1 – AI Reporting Prototype

**Team 5: LangChain and AI Reporting**

### Objectives
- Design the AI reporting service architecture.
- Define input and output JSON contracts.
- Create a LangChain prompt template for integrity reports.
- Implement mock report generation without a live LLM.
- Develop a mock API client and automated tests.
- Build a basic Streamlit invigilator dashboard.

### Technologies
- Python
- Streamlit
- LangChain Core
- Pydantic
- Pytest

### Project Structure
```text
ai_service/       # Validation and report generation
dashboard/        # Streamlit dashboard
examples/         # Sample input and output JSON
tests/            # Automated tests
README.md         # Project documentation
AI_ARCHITECTURE.md # Architecture and prompt design
```

### Setup and Execution
Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

Run tests:

```bash
python -m pytest -v
```

### Sprint 1 Outcome
Developed a reporting prototype with validated input/output schemas, a LangChain prompt template, mock report generation, a mock API client, a Streamlit dashboard, and automated tests.

### Current Limitations
The prototype uses sample data and predefined Python logic. Live LLM integration, backend connectivity, and persistent report storage are future enhancements.

### Responsible Use
The system assists invigilators; suspicious events alone do not establish misconduct. Final decisions require human review.
