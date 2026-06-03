from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import String, Text, Float, Boolean, DateTime, ForeignKey
from datetime import datetime, UTC
from app.database import Base

class AuthUser(Base):
    __tablename__ = "auth_user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    mobile_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

class Resume(Base):
    __tablename__ = "resume"

    resume_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"), nullable=False)
    resume_text: Mapped[str] = mapped_column(Text, nullable=True)
    resume_pdf_path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class JobDescription(Base):
    __tablename__ = "job_description"

    jd_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"), nullable=False)
    jd_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    
class Suggestion(Base):
    __tablename__ = "suggestion"

    suggestion_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.user_id"),nullable=False)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.resume_id"),nullable=False)
    jd_id: Mapped[int] = mapped_column(ForeignKey("job_description.jd_id"),nullable=False)
    suggestion_text: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    suggestion_data: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(UTC))
    is_viewed: Mapped[bool] = mapped_column(Boolean,default=False)