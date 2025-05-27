from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel

class SourceBase(SQLModel):
    url: str
    name: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class SourceRead(SourceBase):
    id: int

    class Config:
        from_attributes = True

class ContentBase(SQLModel):
    source_url: str
    text: str
    publication_date: Optional[datetime] = None
    media_url: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentRead(ContentBase):
    id: int
    source: SourceRead

    class Config:
        from_attributes = True

class DetectionResultBase(SQLModel):
    is_fake: bool
    confidence_score: float
    reason: Optional[str] = None

class DetectionResultCreate(DetectionResultBase):
    content_id: int

class DetectionResultRead(DetectionResultBase):
    id: int
    content_id: int

    class Config:
        from_attributes = True

class AnalysisResultBase(SQLModel):
    sentiment: Optional[str] = None
    spread_metrics: Optional[Dict] = None
    related_articles: Optional[List[int]] = None

class AnalysisResultCreate(AnalysisResultBase):
    detection_result_id: int

class AnalysisResultRead(AnalysisResultBase):
    id: int
    detection_result_id: int

    class Config:
        from_attributes = True

class ContentWithDetectionAndAnalysis(ContentRead):
    detection_result: Optional[DetectionResultRead] = None
    analysis_result: Optional[AnalysisResultRead] = None





