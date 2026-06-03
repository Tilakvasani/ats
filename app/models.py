from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class AuthUser(Base):
    __tablename__ = "auth_user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # hashed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Resume(Base):
    __tablename__ = "resume"

    resume_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"), nullable=False)
    resume_text: Mapped[str] = mapped_column(Text, nullable=True)
    resume_pdf_path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class JobDescription(Base):
    __tablename__ = "job_description"

    jd_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"), nullable=False)
    jd_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.resume_id"), nullable=False)
    jd_id: Mapped[int] = mapped_column(ForeignKey("job_description.jd_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"), nullable=False)
    match_score: Mapped[float] = mapped_column(Float, nullable=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=True)
    matching_skills: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    missing_skills: Mapped[str] = mapped_column(Text, nullable=True)   # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)