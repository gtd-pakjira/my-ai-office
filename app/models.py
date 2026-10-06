from pydantic import BaseModel, Field


class Risk(BaseModel):
    title: str
    description: str


class BlackHatResult(BaseModel):
    hat: str = Field(default="BLACK")
    risks: list[Risk]


class Assignment(BaseModel):
    agent: str
    task: str


class RoundPlan(BaseModel):
    objective: str
    assignments: list[Assignment]


class AgentResult(BaseModel):
    agent: str
    response: str


class MeetingRound(BaseModel):
    hat: str
    objective: str
    assignments: list[Assignment]
    results: list[AgentResult] = Field(default_factory=list)


class HatDecision(BaseModel):
    direction: str
    reason: str


class FinalProposal(BaseModel):
    summary: str
    proposal: str


class MeetingSession(BaseModel):
    goal: str
    rounds: list[MeetingRound] = Field(default_factory=list)
    current_hat: str = "WHITE"
    status: str = "ACTIVE"
    final_proposal: FinalProposal | None = None