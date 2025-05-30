
from typing import List, Optional
from sqlmodel import Session, select

import models
import schemas


def _add_and_commit(db: Session, obj):
    """Helper to add, commit, and refresh a SQLModel object."""
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_source_by_url(db: Session, url: str) -> Optional[models.Source]:
    """Retrieve a Source by its URL."""
    return db.exec(select(models.Source).where(models.Source.url == url)).first()

def create_source(db: Session, source: schemas.SourceCreate) -> models.Source:
    """Create a new Source."""
    db_source = models.Source(**source.model_dump())
    return _add_and_commit(db, db_source)

def create_content(db: Session, content: schemas.ContentCreate) -> models.Content:
    """Create a new Content, creating its Source if necessary."""
    db_source = get_source_by_url(db, content.source_url)
    if not db_source:
        db_source = create_source(db, schemas.SourceCreate(url=content.source_url))
    db_content = models.Content(
        source_id=db_source.id,
        **content.model_dump(exclude={"source_url"})
    )
    return _add_and_commit(db, db_content)

def get_content(db: Session, content_id: int) -> Optional[models.Content]:
    """Retrieve a Content by its ID."""
    return db.get(models.Content, content_id)

def get_contents(db: Session, skip: int = 0, limit: int = 100) -> List[models.Content]:
    """Retrieve a list of Content objects with pagination."""
    return list(db.exec(select(models.Content).offset(skip).limit(limit)).all())

def create_detection_result(db: Session, result: schemas.DetectionResultCreate) -> models.DetectionResult:
    """Create a new DetectionResult."""
    db_result = models.DetectionResult(**result.model_dump())
    return _add_and_commit(db, db_result)

def get_detection_result(db: Session, result_id: int) -> Optional[models.DetectionResult]:
    """Retrieve a DetectionResult by its ID."""
    return db.get(models.DetectionResult, result_id)

def create_analysis_result(db: Session, result: schemas.AnalysisResultCreate) -> models.AnalysisResult:
    """Create a new AnalysisResult."""
    db_result = models.AnalysisResult(**result.model_dump())
    return _add_and_commit(db, db_result)

def get_analysis_result(db: Session, result_id: int) -> Optional[models.AnalysisResult]:
    """Retrieve an AnalysisResult by its ID."""
    return db.get(models.AnalysisResult, result_id)