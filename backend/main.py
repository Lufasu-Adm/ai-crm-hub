from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, database
from ai_service import classify_lead_with_ai

# Inisialisasi Tabel
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI CRM Hub Backend", version="1.0.0")

@app.get("/", tags=["Health"])
def root():
    return {"status": "online", "message": "AI CRM API is active"}

@app.get("/db-test", tags=["Health"])
def test_db(db: Session = Depends(database.get_db)):
    return {"status": "success", "database": "connected"}

@app.post("/leads", response_model=schemas.LeadResponse, status_code=201, tags=["Leads"])
def create_lead(lead_in: schemas.LeadCreate, db: Session = Depends(database.get_db)):
    # 1. Cek Duplikasi
    if db.query(models.Lead).filter(models.Lead.email == lead_in.email).first():
        raise HTTPException(status_code=400, detail="Email address already registered.")

    # 2. AI Classification
    ai_result = classify_lead_with_ai(lead_in.full_name, lead_in.message)

    # 3. Simpan ke DB
    new_lead = models.Lead(
        **lead_in.model_dump(),
        ai_category=ai_result.get("category"),
        lead_score=ai_result.get("score")
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@app.get("/leads", response_model=List[schemas.LeadResponse], tags=["Leads"])
def list_leads(db: Session = Depends(database.get_db)):
    return db.query(models.Lead).all()