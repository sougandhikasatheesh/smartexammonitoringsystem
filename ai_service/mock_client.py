
from .report_service import generate_report


def post_report(session_data: dict) -> dict:
    """
    Simulate sending exam session data to the AI reporting service.
    No real network request is made.
    """
    return generate_report(session_data)
