# 🚀 ET MarketLens: Portfolio-Aware News Intelligence Engine

[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)](https://fastapi.tiangolo.com/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.27-008CC1)](https://neo4j.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB)](https://www.python.org/)

**AI-powered intelligence overlay that bridges the gap between ET news and individual investor portfolios.**

![ET MarketLens Dashboard](docs/screenshot.png)

---

## 🎯 Problem Statement

Indian retail investors (14cr+ demat accounts) consume ET news but **can't connect macro events to their holdings**:
- "RBI rate hike announced" → **Should I sell SBI?**
- "Crude oil +20%" → **How does this hit my retirement goal?**

**Result:** 90%+ retail F&O traders lose money due to information overload and poor decisions.

---

## 💡 Solution: ET MarketLens

**What We Built:**
- **Knowledge Graph** (Neo4j): Maps 15 stocks → 8 sectors → 6 Indian macro factors (Monsoon, PLI, FII flows, etc.)
- **LangChain Agent**: Queries graph + generates plain-language impact cards
- **Portfolio-Aware Analysis**: Shows "what matters for YOUR money"
- **Behavioral Nudges**: Prevents FOMO/panic selling with goal-aligned advice

**Key Innovation:**
> Only ET can do this—no broker has ET's content+data+portfolio stack. We model India-first factors (monsoon, GST collections) that Bloomberg ignores.

---

## 🏗️ Architecture
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Next.js 15 │ ───> │ FastAPI Backend │ ───> │ Neo4j Graph DB │
│ Frontend │ │ + LangChain │ │ (Aura Cloud) │
│ (Port 3000) │ │ (Port 8000) │ │ │
└─────────────────┘ └──────────────────┘ └─────────────────┘
│
▼
┌──────────────────┐
│ OpenAI GPT-4o │
│ (Impact Cards) │
└──────────────────┘

text


**Tech Stack:**
| Component | Technology | Why? |
|-----------|-----------|------|
| **Frontend** | Next.js 15 + Tailwind | Fast SSR, modern React, responsive UI |
| **Backend** | FastAPI + Python 3.13 | Async, auto docs, native ML integration |
| **Graph DB** | Neo4j Aura (Cloud) | Financial relationship modeling, fast traversal |
| **AI/ML** | LangChain + OpenAI | RAG workflows, structured outputs |
| **Deployment** | Vercel + Render | Free tiers, auto-deploy from Git |

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- Neo4j Aura account (free tier)
- OpenAI API key

### **1. Clone & Setup**

```bash
git clone <your-repo>
cd et-marketlens

# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
2. Configure Environment
Backend .env:

Bash

OPENAI_API_KEY=sk-proj-your-key
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j
API_PORT=8000
FRONTEND_URL=https://etmarketlens.vercel.app/
Frontend .env.local:

Bash

NEXT_PUBLIC_API_URL=https://et-marketlens.onrender.com
3. Initialize Database
Bash

cd backend
python setup_graph.py
# ✅ Loads 15 stocks, 8 sectors, 6 factors, 3 news articles
4. Run
Bash

# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
Open: http://localhost:3000

📊 Features Implemented (MVP)
✅ Core Features
 Portfolio upload (JSON/CSV)
 Neo4j knowledge graph (32 nodes, 23 relationships)
 Impact card generation (3 cards per analysis)
 Factor sensitivity scoring (0-100%)
 Daily brief dashboard
 Mock LangChain agent (OpenAI optional)
🎨 UI/UX
 Responsive Tailwind design
 Color-coded impact levels (High/Moderate/Mild/Low)
 Sample portfolio loader
 Real-time API integration
🧪 Testing
 Graph query tests
 Impact analyzer tests
 API endpoint tests
📂 Project Structure
text

et-marketlens/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangChain impact analyzer
│   │   ├── api/              # FastAPI endpoints
│   │   ├── graph/            # Neo4j connection & queries
│   │   └── models/           # Pydantic schemas
│   ├── setup_graph.py        # DB initialization
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js 15 app router
│   ├── components/           # React components
│   ├── lib/                  # API client
│   └── package.json
├── data/                     # Sample portfolios & news
└── docs/                     # Architecture diagrams
🎯 Key Endpoints
Backend API (http://localhost:8000/docs)
Endpoint	Method	Description
/	GET	Health check (Neo4j + OpenAI status)
/api/portfolio/upload	POST	Upload portfolio holdings + goals
/api/impact/analyze	POST	Generate impact cards for portfolio
/api/impact/daily-brief	POST	Daily 3-minute brief
Example Request:

Bash

curl -X POST http://localhost:8000/api/impact/daily-brief \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo",
    "holdings": [
      {"symbol": "RELIANCE", "quantity": 10, "avg_buy_price": 2450.50}
    ],
    "persona": "sip_investor"
  }'
🧠 How It Works
1. Knowledge Graph Schema
cypher

(:Stock {symbol, name, beta, market_cap})
  -[:BELONGS_TO]->
(:Sector {name, type})
  -[:SENSITIVE_TO {sensitivity}]->
(:Factor {name, current_value, impact})

(:News {id, title, sentiment, published_date})
  -[:MENTIONS]->
(:Stock)
Example Relationships:

HDFCBANK → Banking → RepoRate (90% sensitivity)
RELIANCE → Energy → CrudeOilPrice (95% sensitivity)
TCS → IT → USDINRRate (80% sensitivity)
2. Impact Analysis Flow
Python

1. User uploads portfolio → Extract symbols
2. Query Neo4j: "What factors affect these stocks?"
3. Score impact: (beta × factor_move × sensitivity)
4. LLM generates cards: "Explain in simple Hindi-English"
5. Return top 3 impacts with action options
3. Sample Output
JSON

{
  "headline": "HIGH: Crude Oil Spike Affects Energy Stocks",
  "impact_cards": [
    {
      "factor": "CrudeOilPrice",
      "title": "Crude Oil Spike Affects Energy Stocks",
      "impact_level": "high",
      "sensitivity_score": 95.0,
      "affected_holdings": ["RELIANCE"],
      "summary": "Crude oil at $85/barrel impacts Reliance...",
      "action_options": [
        {"action": "Hold & Monitor", "reason": "Continue SIP as planned"},
        {"action": "Review Allocation", "reason": "Check rebalancing"}
      ]
    }
  ]
}
🔮 Future Scope
Post-Hackathon Roadmap
Phase 1 (Week 1-2):

 Live ET RSS integration
 Real-time NSE/BSE price API
 User authentication (Clerk)
 PostgreSQL for user data
Phase 2 (Month 1):

 What-If scenario engine ("If oil +20%, show impact")
 Email/WhatsApp daily brief
 Mobile PWA
 Hindi/Marathi language support
Phase 3 (Quarter 1):

 ET Portfolio OAuth sync
 Behavioral pattern detection (ML)
 Cohort benchmarking
 Premium tier ($5/month)
🎓 Hackathon Fit
Theme: AI for the Indian Investor

Uniqueness:

India-First Graph: Monsoon, PLI, GST—not US factors
ET-Native: Only ET has this content+portfolio stack
Noise Firewall: 1000s of stories → 3 actionable signals
Goal-Aware: Ties news to retirement/education goals
Impact:

Target: 14cr+ demat users
Solves: ₹50L cr annual retail losses from poor timing
Monetization: ET Prime upsell ($10/month → $15 with MarketLens)
👥 Team
Built by Swapnil and Aditya for ET Hackathon 2026

📄 License
MIT License - See LICENSE file

🙏 Acknowledgments
Economic Times for the hackathon opportunity
Neo4j for Aura free tier
OpenAI for GPT-4o API
Vercel & Render for hosting credits
📞 Contact
Demo: https://etmarketlens.vercel.app
GitHub: https://github.com/yourusername/et-marketlens
Email: your.email@example.com
Built with ❤️ for Indian retail investors 🇮🇳