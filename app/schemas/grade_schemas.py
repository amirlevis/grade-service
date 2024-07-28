from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, func

from app.database import Base


class Grade(Base):
    __tablename__ = "grade"

    id: int = Column(Integer, primary_key=True, index=True)
    subject_id: int = Column(Integer, nullable=False)
    student_id: int = Column(Integer, nullable=False)
    grade: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
