# CureTrace — Backend (FastAPI)

## Tech Stack
- **Python 3.11+**
- **FastAPI** — High-performance async web framework
- **Uvicorn** — ASGI server
- **Pydantic v2** — Data validation & settings management

## Project Structure

```
Backend/
├── main.py               # App entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── app/
    ├── config.py         # Settings (loaded from .env)
    ├── routers/
    │   ├── health.py     # GET /api/v1/health
    │   └── users.py      # CRUD /api/v1/users
    ├── models/           # ORM models (add when using a DB)
    └── schemas/
        └── user.py       # Pydantic request/response schemas
```

## Getting Started

### 1. Create & activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Run the development server
```bash
uvicorn main:app --reload --port 8000
```

## API Docs
Once running, open:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc
