from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    questions = Column(Text, nullable=False)
    rubric = Column(Text, nullable=False)
    study_plan = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
