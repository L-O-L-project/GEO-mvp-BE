# geo-mvp-BE

FastAPI backend for GEO audit testing.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Endpoints
- `GET /` service info
- `GET /health` health check
- `GET /geo-test` GEO web test page
- `POST /api/geo-audit` run GEO audit

## GEO enhancement reserve
The following modules are intentionally kept for future GEO enhancement:
- `app/services/analyze.py`
- `app/services/llm.py`
