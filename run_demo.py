
import json
from pathlib import Path

from ai_service import generate_report


input_path = Path("examples/sample_session.json")

with input_path.open(encoding="utf-8") as file:
    session_data = json.load(file)

report = generate_report(session_data)

print(json.dumps(report, indent=2))
