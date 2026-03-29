from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
# Use mock for testing without OpenAI key
from app.agents.mock_impact_analyzer import mock_impact_analyzer as impact_analyzer
router = APIRouter(prefix="/api/impact", tags=["Impact Analysis"])

class ImpactRequest(BaseModel):
    user_id: str
    holdings: List[Dict[str, Any]]
    persona: Optional[str] = "sip_investor"

@router.post("/analyze")
async def analyze_portfolio_impact(request: ImpactRequest):
    """Analyze portfolio and generate impact cards"""
    try:
        impact_cards = impact_analyzer.analyze_portfolio_impact(
            holdings=request.holdings,
            persona=request.persona
        )
        
        return {
            "user_id": request.user_id,
            "impact_cards": impact_cards,
            "count": len(impact_cards)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/daily-brief")
async def generate_daily_brief(request: ImpactRequest):
    """Generate daily portfolio brief"""
    try:
        brief = impact_analyzer.generate_daily_brief(
            holdings=request.holdings,
            persona=request.persona
        )
        
        return brief
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))