from pydantic import BaseModel


class AnalysisCreate(BaseModel):
    filename: str
    summary: str
    questions: str
    rubric: str
    study_plan: str


class AnalysisOut(AnalysisCreate):
    id: int
    created_at: str | None = None

    class Config:
        from_attributes = True
