
from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


RiskCategory = Literal["low", "moderate", "high"]
Severity = Literal["low", "medium", "high"]


class MonitoringEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str = Field(min_length=1)
    timestamp: str = Field(min_length=1)
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    integrity_score: int = Field(ge=0, le=100)
    risk_category: RiskCategory
    events: list[MonitoringEvent] = Field(default_factory=list)


class IntegrityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str
    session_id: str
    integrity_score: int = Field(ge=0, le=100)
    risk_category: RiskCategory
    event_summary: str
    important_evidence: list[str]
    ai_summary: str
    review_status: Literal["pending"] = "pending"
