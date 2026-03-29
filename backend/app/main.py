from app.api.impact import router as impact_router
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import json
import pandas as pd
from io import StringIO

load_dotenv()

app = FastAPI(
    title="ET MarketLens API",
    description="Portfolio-Aware News Intelligence Engine",
    version="0.1.0"
)
# Include routers
app.include_router(impact_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://et-marketlens.vercel.app",
        "https://*.vercel.app",  # Allow all Vercel preview URLs
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    neo4j_connected: bool
    openai_configured: bool

class Holding(BaseModel):
    symbol: str
    quantity: int
    avg_buy_price: float
    goal_id: Optional[str] = None

class Goal(BaseModel):
    name: str
    target_amount: float
    target_year: int
    risk_profile: str

class Portfolio(BaseModel):
    user_id: str
    holdings: List[Holding]
    goals: List[Goal]
    persona: Optional[str] = "sip_investor"

portfolios_db = {}

@app.get("/", response_model=HealthResponse)
async def health_check():
    neo4j_ok = bool(os.getenv("NEO4J_URI"))
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    
    return HealthResponse(
        status="healthy" if (neo4j_ok and openai_ok) else "degraded",
        neo4j_connected=neo4j_ok,
        openai_configured=openai_ok
    )

@app.post("/api/portfolio/upload")
async def upload_portfolio(portfolio: Portfolio):
    try:
        portfolios_db[portfolio.user_id] = portfolio.model_dump()
        
        return {
            "message": "Portfolio uploaded successfully",
            "user_id": portfolio.user_id,
            "holdings_count": len(portfolio.holdings),
            "goals_count": len(portfolio.goals)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/portfolio/upload-csv")
async def upload_portfolio_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        required_columns = ['symbol', 'quantity', 'avg_buy_price']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"CSV must contain columns: {required_columns}"
            )
        
        holdings = []
        for _, row in df.iterrows():
            holdings.append({
                "symbol": str(row['symbol']).upper(),
                "quantity": int(row['quantity']),
                "avg_buy_price": float(row['avg_buy_price']),
                "goal_id": row.get('goal_id', None)
            })
        
        return {
            "message": "CSV processed successfully",
            "holdings": holdings,
            "count": len(holdings)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/portfolio/{user_id}")
async def get_portfolio(user_id: str):
    if user_id not in portfolios_db:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return portfolios_db[user_id]

@app.get("/api/test")
async def test_endpoint():
    return {
        "message": "ET MarketLens API is running!",
        "environment": {
            "neo4j_uri": os.getenv("NEO4J_URI", "NOT_SET")[:30] + "...",
            "openai_key": "CONFIGURED" if os.getenv("OPENAI_API_KEY") else "NOT_SET"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))