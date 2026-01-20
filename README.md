
# 🏥 Medical Telegram Data Warehouse

**End-to-End ELT Pipeline for Ethiopian Medical Market Intelligence**

## 📌 Project Overview

This project implements a **modern data platform** that extracts, transforms, enriches, and serves analytical insights from **public Ethiopian medical Telegram channels**.

Built for **Kara Solutions**, a data science consultancy in Ethiopia, the platform enables stakeholders to analyze:

* Frequently mentioned medical products and drugs
* Channel-level activity and trends
* Visual content usage and engagement
* Image-based promotional strategies using computer vision

The system follows **modern ELT best practices**, using dbt for transformations, Dagster for orchestration, YOLOv8 for image enrichment, and FastAPI for data access.

---

## 🎯 Business Questions Answered

* What are the **top 10 most mentioned medical products** across Telegram?
* How do **prices and availability** vary by channel?
* Which channels publish the **most visual content**?
* Do **promotional images (people + product)** receive more views?
* What are the **daily and weekly posting trends** for health topics?

---

## 🏗️ Architecture Overview

```text
Telegram Channels
        │
        ▼
Raw Data Lake (JSON + Images)
        │
        ▼
PostgreSQL (Raw Schema)
        │
        ▼
dbt Transformations
(Staging → Star Schema)
        │
        ▼
YOLOv8 Image Enrichment
        │
        ▼
Analytics Data Marts
        │
        ▼
FastAPI Analytical API
```

---

## 🧰 Technology Stack

| Layer           | Tools                          |
| --------------- | ------------------------------ |
| Extraction      | Telethon (Telegram API)        |
| Storage         | Local Data Lake (JSON, Images) |
| Warehouse       | PostgreSQL                     |
| Transformations | dbt (ELT)                      |
| Orchestration   | Dagster                        |
| Enrichment      | YOLOv8 (Ultralytics)           |
| API             | FastAPI                        |
| Infrastructure  | Docker, Docker Compose         |
| Validation      | dbt Tests, Custom SQL Tests    |

---

## 📁 Project Structure

```text
medical-telegram-warehouse/
├── .github/workflows/        # CI pipelines
├── .vscode/                 # Editor settings
├── api/                     # FastAPI app
│   ├── main.py
│   ├── database.py
│   └── schemas.py
├── data/
│   └── raw/
│       ├── telegram_messages/
│       └── images/
├── medical_warehouse/       # dbt project
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── tests/
│   └── dbt_project.yml
├── src/
│   ├── scraper.py           # Telegram scraper
│   ├── yolo_detect.py       # Image detection
│   └── pipeline.py          # Dagster pipeline
├── logs/                    # Scraping & pipeline logs
├── scripts/                 # Utility scripts
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env                     
└── README.md
```

---

## 🔐 Environment Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Nebiyou-x/MedData_Warehouse.git
cd MedData_Warehouse
```

### 2️⃣ Create `.env` File

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

POSTGRES_DB=medical_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```



---

## 🐳 Run with Docker (Recommended)

```bash
docker-compose up --build
```

This starts:

* PostgreSQL
* API service
* dbt-ready environment

---

## 🧲 Task 1 – Telegram Data Scraping

**Script:** `src/scraper.py`

### Features

* Scrapes public medical Telegram channels
* Extracts text, metadata, views, forwards
* Downloads images
* Stores raw JSON in a partitioned data lake

```text
data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
data/raw/images/channel_name/message_id.jpg
```

### Run

```bash
python src/scraper.py
```

---

## 🧱 Task 2 – Data Modeling with dbt

### Star Schema Design

#### Dimension Tables

* `dim_channels`
* `dim_dates`

#### Fact Tables

* `fct_messages`
* `fct_image_detections`

### dbt Workflow

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```

### Data Quality

* Primary key uniqueness
* Foreign key relationships
* Custom tests:

  * No future messages
  * Non-negative view counts

---

## 🖼️ Task 3 – Image Enrichment (YOLOv8)

**Script:** `src/yolo_detect.py`

### Object Categories

* `promotional` → person + product
* `product_display` → product only
* `lifestyle` → person only
* `other`

### Output

* CSV with detections
* Loaded into `fct_image_detections`

```bash
python src/yolo_detect.py
```

---

## 🌐 Task 4 – Analytical API (FastAPI)

### Run API

```bash
uvicorn api.main:app --reload
```

### API Docs

```
http://localhost:8000/docs
```

### Endpoints

| Endpoint                        | Description             |
| ------------------------------- | ----------------------- |
| `/api/reports/top-products`     | Most mentioned products |
| `/api/channels/{name}/activity` | Channel trends          |
| `/api/search/messages`          | Keyword search          |
| `/api/reports/visual-content`   | Image usage stats       |

---

## ⏱️ Task 5 – Pipeline Orchestration (Dagster)

### Run Dagster

```bash
dagster dev -f src/pipeline.py
```

### UI

```
http://localhost:3000
```

### Pipeline Ops

* `scrape_telegram_data`
* `load_raw_to_postgres`
* `run_dbt_transformations`
* `run_yolo_enrichment`

Supports **daily scheduling and monitoring**.

---

## 📊 Key Insights (Example)

* Promotional images tend to receive **higher average views**
* Pharmaceutical channels post **less frequently but more consistently**
* Pre-trained YOLO models struggle with **domain-specific medical objects**

---

## ⚠️ Limitations

* YOLO is not trained on Ethiopian pharmaceutical products
* Telegram message text may contain informal language
* Pricing extraction requires advanced NLP

---

## 🚀 Future Improvements

* Custom-trained YOLO model for medical products
* NLP-based product and price extraction
* Cloud deployment (S3, BigQuery, GCP)
* Authentication for API access
* Airflow alternative orchestration

