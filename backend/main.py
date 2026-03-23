import os
import logging
import httpx
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from dotenv import load_dotenv

import models, schemas, database
from ai_service import classify_lead_with_ai

load_dotenv()

# Konfigurasi Logging standar industri
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Inisialisasi Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="AI CRM Hub API",
    description="Intelligent CRM system powered by Gemini and n8n",
    version="1.1.0"
)

# Konfigurasi CORS agar frontend dapat mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def send_webhook_to_n8n(payload: Dict[str, Any]) -> None:
    """Mengirim data lead ke n8n webhook secara asinkron."""
    if not N8N_WEBHOOK_URL:
        logger.error("Konfigurasi N8N_WEBHOOK_URL tidak ditemukan di .env")
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(N8N_WEBHOOK_URL, json=payload, timeout=5.0)
            response.raise_for_status()
            logger.info(f"Webhook berhasil dikirim ke n8n. Status: {response.status_code}")
    except httpx.HTTPStatusError as e:
        logger.error(f"n8n Webhook error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error(f"Gagal mengirim webhook ke n8n: {e}", exc_info=True)

@app.get("/", tags=["Health"])
def health_check():
    """Endpoint untuk mengecek status API."""
    return {"status": "online", "message": "AI CRM API is operational"}

@app.get("/db-test", tags=["Health"])
def database_check(db: Session = Depends(database.get_db)):
    """Endpoint untuk mengecek koneksi database."""
    return {"status": "success", "database": "connected"}

@app.post("/leads", response_model=schemas.LeadResponse, status_code=status.HTTP_201_CREATED, tags=["Leads"])
async def create_lead(
    lead_in: schemas.LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    """
    Menerima lead baru, klasifikasi via AI, simpan ke database,
    dan memicu webhook n8n di background.
    """
    if db.query(models.Lead).filter(models.Lead.email == lead_in.email).first():
        logger.warning(f"Percobaan input duplikat untuk email: {lead_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered."
        )

    ai_result = classify_lead_with_ai(lead_in.full_name, lead_in.message)
    category = ai_result.get("category", "Warm")
    score = ai_result.get("score", 50)

    new_lead = models.Lead(
        **lead_in.model_dump(),
        ai_category=category,
        lead_score=score
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    # Eksekusi webhook di background agar response API tetap instan (< 100ms)
    payload = {
        "event": "lead_received",
        "id": new_lead.id,
        "full_name": new_lead.full_name,
        "email": new_lead.email,
        "company": new_lead.company,
        "message": new_lead.message,
        "category": category,
        "score": score
    }
    
    if category == "Hot":
        background_tasks.add_task(send_webhook_to_n8n, payload)

    logger.info(f"Lead berhasil disimpan: {new_lead.email} (Kategori: {category})")
    return new_lead

@app.get("/leads", response_model=List[schemas.LeadResponse], tags=["Leads"])
def list_leads(db: Session = Depends(database.get_db)):
    """Mengambil seluruh data lead dari database."""
    return db.query(models.Lead).all()