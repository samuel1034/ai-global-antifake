from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSON


class Source (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True, unique=True)
    name: Optional[str] = None
    contents: List["Content"] = Relationship(back_populates="source")


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="source.id")
    source: Optional[Source] = Relationship(back_populates="contents")
    text: str
    publication_date: Optional[datetime] = None
    media_url: Optional[str] = None
    detection_result: Optional["DetectionResult"] = Relationship(
        back_populates="contents")


class DetectionResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content_id: int = Field(foreign_key="content.id")
    content: Optional[Content] = Relationship(
        back_populates="detection_result")
    is_fake: bool
    confidence_score: float
    reason: Optional[str] = None
    analysis_result: Optional["AnalysisResult"] = Relationship(
        back_populates="detection_result")


class AnalysisResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    detection_result_id: int = Field(foreign_key="detectionresult.id")
    detection_result: Optional[DetectionResult] = Relationship(
        back_populates="analysis_result")
    sentiment: Optional[str] = None
    spread_metrics: Optional[dict] = Field(default=None, sqltype=JSON)
    related_articles: Optional[List[int]] = Field(default=None, sqltype=JSON)
