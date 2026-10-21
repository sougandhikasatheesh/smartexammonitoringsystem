# ExamGuard – Smart Exam Monitoring System

## Project Overview

ExamGuard is a Smart Exam Monitoring System designed to support online examination integrity through automated monitoring, risk analysis, and AI-assisted reporting.

The system aims to help invigilators review suspicious events detected during an examination. The AI reporting module summarizes monitoring events and presents relevant evidence in a structured format to support human review.

**Current Development Stage:** Sprint 1 – AI Reporting Prototype

## Team 5 – LangChain and AI Reporting

Our responsibility is to design and develop the AI reporting module for ExamGuard.

### Sprint 1 Objectives

- Design the AI reporting service architecture.
- Define the input and output JSON contract for report generation.
- Develop a structured prompt for generating examination integrity reports.
- Implement mock report generation without connecting to a live LLM.
- Create mock API clients and automated integration tests.
- Develop a basic Streamlit dashboard for invigilators to view examination reports.

## Technologies Used

- **Python 3.11** – Core programming language.
- **Streamlit** – Interactive invigilator dashboard.
- **LangChain Core** – Prompt template design.
- **Pydantic** – Input validation and report schema definition.
- **Pytest** – Automated testing.

## Project Structure

```text
smartexammonitoringsystem/
│
├── ai_service/
│   ├── __init__.py
│   ├── report_schema.py
│   ├── prompt_template.py
│   ├── report_service.py
│   └── mock_client.py
│
├── dashboard/
│   └── app.py
│
├── examples/
│   └── sample_session.json
│
├── tests/
│   └── test_report_service.py
│
├── requirements.txt
├── README.md
└── run_demo.py
```

## Module Description

### 1. Report Schema (`report_schema.py`)

Defines the input and output data structures using Pydantic.

The input contains candidate information, session information, integrity score, risk category, and monitoring events. The output contains an event summary, important evidence, an AI-style summary, and review status.

### 2. Prompt Template (`prompt_template.py`)

Defines the LangChain prompt instructions for producing structured examination integrity reports.

The prompt instructs the reporting system to use only the provided information, avoid inventing evidence, and leave final decisions to human invigilators.

### 3. Report Service (`report_service.py`)

Validates examination session data and generates a structured report using predefined Python logic.

The current implementation uses a mock summary rather than a live language model.

### 4. Mock Client (`mock_client.py`)

Simulates an API client that submits session data to the reporting service without requiring a real backend connection.

### 5. Streamlit Dashboard (`dashboard/app.py`)

Provides a basic invigilator dashboard displaying candidate information, integrity score, risk category, monitoring events, important evidence, and the generated report.

The prototype also provides controls to mark a report as reviewed or keep it pending.

### 6. Automated Tests (`tests/test_report_service.py`)

Tests report generation, required fields, session information, evidence handling, input validation, empty event handling, and mock client functionality.

## Setup Instructions

### Prerequisites

- Python 3.11 or a compatible Python version.
- pip package manager.

### Step 1: Clone or download the repository

Open a terminal in the project directory.

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the dashboard

```bash
streamlit run dashboard/app.py
```

Streamlit will provide a local URL where the dashboard can be accessed.

### Step 5: Run the automated tests

```bash
python -m pytest -v
```

## Sample Input

The sample session file contains fictional examination monitoring data, including candidate and session identifiers, an integrity score, a risk category, and events such as face absence or multiple faces detected.

## Sample Output

The reporting service generates a structured report containing:

- Candidate ID and session ID.
- Integrity score and risk category.
- Monitoring event summary.
- Important evidence.
- AI-style session summary.
- Review status.

## Current Limitations

- The dashboard currently uses sample session data.
- Report summaries are generated using predefined Python logic.
- A live LLM has not yet been integrated.
- The mock client does not communicate with a real backend API.
- Review status is stored only in the current Streamlit session and is not persisted to a database.
- The reporting module depends on the monitoring data provided to it; it does not independently detect examination violations.

## Future Enhancements

- Integrate a live LLM through LangChain.
- Connect the reporting module to the backend API.
- Integrate real-time monitoring events from the other system modules.
- Add persistent report storage and review history.
- Improve report explanations and evidence presentation.

## Responsible Use

ExamGuard is intended to assist invigilators, not replace human judgment. A suspicious event or risk score alone does not establish misconduct. Reports should be reviewed alongside the available evidence before any decision is made.

## Sprint 1 Deliverable

A prototype AI reporting module with a defined JSON contract, structured prompt template, mock report generation, automated tests, and a basic Streamlit invigilator dashboard.
