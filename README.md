# 🤖 Agentic Commerce AI Assistant

An AI-powered shopping assistant that understands natural-language product requests, extracts user intent, filters products based on constraints, ranks the best options, and generates an AI-powered recommendation.

## 🚀 Features

- 🧠 Natural-language shopping query understanding
- 🎯 Intent extraction
- 🔎 Product catalog search
- 💰 Budget constraint filtering
- ⭐ Product ranking based on rating and use case
- 🤖 Gemini-powered recommendation explanation
- 🔄 Alternative product suggestions
- 📊 Agent pipeline visualization
- ⚡ React frontend with FastAPI backend

## 🏗️ Agent Pipeline

The application follows a multi-step agentic workflow:

1. **Intent Extraction**  
   Identifies product category, budget, and intended use.

2. **Catalog Search**  
   Searches the local product catalog for relevant products.

3. **Constraint Filtering**  
   Filters products according to category and budget.

4. **Product Ranking**  
   Ranks products using ratings and use-case relevance.

5. **AI Recommendation Generation**  
   Uses Google Gemini to explain why the selected product is suitable.

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn

### AI
- Google Gemini API
- Google GenAI SDK

### Data
- JSON product catalog

### Development Tools
- VS Code
- Git
- GitHub

## 📁 Project Structure

```text
agentic-commerce-ai-assistant/
│
├── backend/
│   ├── agent.py
│   ├── main.py
│   ├── products.json
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
## 🚀 Live Demo

Frontend: https://agentic-commerce-ai-frontend.onrender.com

Backend API: https://agentic-commerce-ai-assistant-1.onrender.com

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### AI & Agent
- LLM-based query understanding
- Intent extraction
- Product filtering
- Product ranking
- AI recommendation generation

## ▶️ How to Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload