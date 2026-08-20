from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run
app=FastAPI(title='Agentic Commerce AI Assistant')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://agentic-commerce-ai-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Query(BaseModel): query:str
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/api/recommend')
def recommend(q:Query): return run(q.query)
