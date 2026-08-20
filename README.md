# Agentic Commerce AI Assistant

AI-powered shopping assistant: natural-language intent extraction, budget filtering, product ranking, comparison and explainable recommendations.

## Stack
- React + Vite
- FastAPI + Python
- Rule-based agent pipeline (LLM integration can be added later)

## Run
Backend:
```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```
