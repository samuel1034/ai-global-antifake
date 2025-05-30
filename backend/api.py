# backend/app/api.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

import crud
import models
import schemas
from database import get_db

router = APIRouter()

@router.post("/contents/", response_model=schemas.ContentRead)
def create_content_api(content: schemas.ContentCreate, db: Session = Depends(get_db)):
    db_content = crud.create_content(db=db, content=content)
    return db_content

@router.get("/contents/{content_id}", response_model=schemas.ContentWithDetectionAndAnalysis)
def read_content_api(content_id: int, db: Session = Depends(get_db)):
    db_content = crud.get_content(db=db, content_id=content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.get("/contents/", response_model=List[schemas.ContentRead])
def read_contents_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contents(db=db, skip=skip, limit=limit)

@router.post("/detect/", response_model=schemas.DetectionResultRead)
def detect_misinformation_api(content_id: int, db: Session = Depends(get_db)):
    db_content = crud.get_content(db=db, content_id=content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")

    # --- AI Misinformation Detection Logic Here ---
    # For simplicity, let's directly create the schema instance
    detection_result_schema = schemas.DetectionResultCreate(
        content_id=content_id,
        is_fake=False,
        confidence_score=0.85,
        reason="Contains strong claims without credible sources."
    )
    return crud.create_detection_result(db=db, result=detection_result_schema)

@router.get("/detections/{detection_id}", response_model=schemas.DetectionResultRead)
def read_detection_api(detection_id: int, db: Session = Depends(get_db)):
    db_detection = crud.get_detection_result(db=db, result_id=detection_id)
    if not db_detection:
        raise HTTPException(status_code=404, detail="Detection result not found")
    return db_detection

@router.post("/analyze/{detection_id}", response_model=schemas.AnalysisResultRead)
def analyze_misinformation_api(detection_id: int, db: Session = Depends(get_db)):
    db_detection = crud.get_detection_result(db=db, result_id=detection_id)
    if not db_detection:
        raise HTTPException(status_code=404, detail="Detection result not found")

    # --- AI Misinformation Analysis Logic Here ---
    analysis_result_schema = schemas.AnalysisResultCreate(
        detection_result_id=detection_id,
        sentiment="negative",
        spread_metrics={"retweets": 120, "shares": 300},
        related_articles=[45, 67]
    )
    return crud.create_analysis_result(db=db, result=analysis_result_schema)

@router.get("/analysis/{analysis_id}", response_model=schemas.AnalysisResultRead)
def read_analysis_api(analysis_id: int, db: Session = Depends(get_db)):
    db_analysis = crud.get_analysis_result(db=db, result_id=analysis_id)
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return db_analysis