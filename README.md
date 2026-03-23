# AI CRM Hub: Intelligent Lead Scoring & Event-Driven Automation

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)


## 🎬 Demo

<p align="center">
  <img src="https://github.com/Lufasu-Adm/AI-QUIZ-EVENT/blob/main/docs/demo/0316.gif" width="900"/>
</p>

AI CRM Hub adalah sistem **AI-powered lead management** yang dirancang untuk membantu tim sales mengidentifikasi, memprioritaskan, dan merespons prospek secara otomatis dan real-time.

Sistem ini menggunakan **LLM (Gemini 3 Flash)** untuk menganalisis intensitas pesan pelanggan dan mengotomatisasi alur kerja berbasis event melalui **n8n**, termasuk notifikasi instan ke Telegram untuk lead bernilai tinggi.

---

## 💼 Business Value

* 🚀 **Increase Conversion Rate** dengan memprioritaskan lead berkualitas tinggi
* ⚡ **Reduce Response Time** melalui automation real-time
* 🎯 **Better Lead Qualification** menggunakan AI berbasis BANT
* 🤖 **Minimize Manual Work** untuk tim sales

---

## ✨ Fitur Utama

### 🤖 Real-time AI Scoring

Menggunakan **Gemini 3 Flash** untuk mengklasifikasikan lead ke dalam kategori **Hot, Warm, Cold** berdasarkan framework **BANT (Budget, Authority, Need, Timeline)**.

### ⚡ Asynchronous Webhook

Dengan **FastAPI BackgroundTasks**, API tetap responsif (<100ms) sementara proses AI dan automation berjalan di background.

### 🔄 Event-Driven Automation

Integrasi dengan **n8n** untuk memicu workflow otomatis seperti:

* Notifikasi Telegram
* Lead routing
* Integrasi ke sistem eksternal

### 🎨 Modern Landing Page

Frontend responsif menggunakan **Tailwind CSS**.

### 🏗️ Production-Ready Architecture

* Environment Variables (.env)
* Type Hinting
* Robust Error Handling
* Scalable Architecture

---

## 🧠 Arsitektur Sistem

```mermaid
graph LR
A[Frontend] --> B[FastAPI Backend]
B --> C[Gemini AI]
B --> D[PostgreSQL]
B --> E[n8n Webhook]
E --> F[Telegram Notification]
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python 3.10+)
* **Database:** PostgreSQL (SQLAlchemy ORM)
* **AI Engine:** Google Generative AI (Gemini 3 Flash)
* **Automation:** n8n
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```
ai-crm-hub/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── frontend/
├── docker/
├── n8n/
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10+
* Docker & Docker Compose
* Gemini API Key

### 2. Environment Setup

Buat file `.env` di folder `backend/`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/crm_db
GEMINI_API_KEY=your_google_api_key_here
N8N_WEBHOOK_URL=http://localhost:5678/webhook/your-webhook-id
```

### 3. Installation

```bash
# Clone repository
git clone https://github.com/Lufasu-Adm/ai-crm-hub.git
cd ai-crm-hub

# Run infrastructure
docker-compose up -d

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload
```

---

## 📡 API Endpoints

| Method | Endpoint | Description                      |
| ------ | -------- | -------------------------------- |
| GET    | `/`      | Health check                     |
| POST   | `/leads` | Submit lead & trigger AI scoring |
| GET    | `/leads` | Get all leads                    |

---

## 🔌 Example API Usage

### Request

```json
POST /leads
{
  "message": "Saya mau beli 100 unit, bisa kirim invoice hari ini?"
}
```

### Response

```json
{
  "score": 92,
  "category": "HOT"
}
```

---

## 📊 AI Classification Logic

* 🔥 **HOT (80–100)** → Urgent, high intent, ready to buy
* 🌤️ **WARM (40–79)** → Interested but exploratory
* ❄️ **COLD (0–39)** → Low intent or unclear

📌 Hanya kategori **HOT** yang akan memicu notifikasi ke Telegram.

---

## 🔮 Future Improvements

* Multi-channel integration (WhatsApp, Email)
* Dashboard analytics (conversion tracking)
* Fine-tuned AI model
* Role-based access control (RBAC)

---

## 👤 Author

**Jordan Wijayanto (Lufasu-Adm)**
Informatics Student – Telkom University Surabaya
GitHub: [https://github.com/Lufasu-Adm](https://github.com/Lufasu-Adm)

---

## 📜 License

This project is licensed under the MIT License.
