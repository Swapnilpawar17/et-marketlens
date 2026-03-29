from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
from typing import List, Dict, Any
from app.graph import get_portfolio_exposure, get_stock_info, get_news_impact

class ImpactAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Using mini for faster/cheaper responses
            temperature=0.3,  # Lower temperature for more factual responses
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def analyze_portfolio_impact(
        self, 
        holdings: List[Dict[str, Any]], 
        persona: str = "sip_investor"
    ) -> List[Dict[str, Any]]:
        """Generate impact cards for a portfolio"""
        
        # Extract symbols
        symbols = [h['symbol'] for h in holdings]
        
        # Get factor exposure from graph
        exposure_data = get_portfolio_exposure(symbols)
        
        # Group by factor
        factor_impacts = {}
        for item in exposure_data:
            factor = item['factor']
            if factor not in factor_impacts:
                factor_impacts[factor] = {
                    'factor': factor,
                    'stocks': [],
                    'max_sensitivity': 0,
                    'factor_value': item.get('factor_value', 0)
                }
            factor_impacts[factor]['stocks'].append({
                'symbol': item['stock'],
                'sector': item['sector'],
                'sensitivity': item['sensitivity']
            })
            factor_impacts[factor]['max_sensitivity'] = max(
                factor_impacts[factor]['max_sensitivity'],
                item['sensitivity']
            )
        
        # Generate impact cards for top 3 factors
        impact_cards = []
        sorted_factors = sorted(
            factor_impacts.values(), 
            key=lambda x: x['max_sensitivity'], 
            reverse=True
        )[:3]
        
        for factor_data in sorted_factors:
            card = self._generate_impact_card(factor_data, holdings, persona)
            impact_cards.append(card)
        
        return impact_cards
    
    def _generate_impact_card(
        self, 
        factor_data: Dict, 
        holdings: List[Dict], 
        persona: str
    ) -> Dict[str, Any]:
        """Generate a single impact card using LLM"""
        
        # Create context for LLM
        affected_stocks = factor_data['stocks']
        factor_name = factor_data['factor']
        
        # Build holdings context
        holdings_str = "\n".join([
            f"- {h['symbol']}: {h['quantity']} shares @ ₹{h['avg_buy_price']}"
            for h in holdings
        ])
        
        # Build exposure context
        exposure_str = "\n".join([
            f"- {s['symbol']} ({s['sector']}): {s['sensitivity']*100:.0f}% sensitivity"
            for s in affected_stocks
        ])
        
        # Persona definitions
        persona_context = {
            "sip_investor": "conservative long-term investor doing monthly SIPs, focused on retirement goals 15-20 years away",
            "trader": "active trader looking for short-term opportunities, holding period 1-3 months",
            "value_investor": "fundamental analyst seeking undervalued companies for 3-5 year hold"
        }
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""You are ET MarketLens, an AI assistant for Indian retail investors.
Your job is to explain macro events in simple language and show portfolio impact.

User Profile: {persona_context.get(persona, persona_context['sip_investor'])}

Rules:
1. Use simple Hindi-English terms (like "repo rate" not "policy rate")
2. Be specific about INR amounts and percentages
3. Provide 2 action options: one conservative, one opportunistic
4. Keep explanations under 100 words
5. No jargon unless you immediately explain it"""),
            
            HumanMessage(content=f"""Portfolio Holdings:
{holdings_str}

Factor: {factor_name} (current value: {factor_data['factor_value']})

Affected Stocks:
{exposure_str}

Generate a brief impact analysis with:
1. Title (8 words max, engaging)
2. Impact summary (3 sentences, explain WHAT happened and WHY it matters)
3. Severity: low/mild/moderate/high
4. Two action options with reasoning
5. One-line bottom line for this investor type

Format as JSON.""")
        ])
        
        # Get LLM response
        response = self.llm.invoke(prompt.format_messages())
        
        # Parse response (simplified - in production, use structured output)
        content = response.content
        
        # Build structured card
        card = {
            "factor": factor_name,
            "title": self._extract_title(content, factor_name),
            "impact_level": self._calculate_impact_level(factor_data['max_sensitivity']),
            "summary": self._extract_summary(content),
            "affected_holdings": [s['symbol'] for s in affected_stocks],
            "sensitivity_score": round(factor_data['max_sensitivity'] * 100, 1),
            "action_options": self._extract_actions(content),
            "llm_explanation": content
        }
        
        return card
    
    def _extract_title(self, content: str, factor: str) -> str:
        """Extract title from LLM response"""
        # Simple extraction - look for first line or use factor name
        lines = content.strip().split('\n')
        for line in lines:
            if 'title' in line.lower() or len(line) < 80:
                return line.replace('"', '').replace('Title:', '').strip()
        return f"Impact Alert: {factor} Movement"
    
    def _extract_summary(self, content: str) -> str:
        """Extract summary from LLM response"""
        # Look for summary section
        if 'summary' in content.lower():
            parts = content.lower().split('summary')
            if len(parts) > 1:
                return parts[1][:300].strip()
        return content[:300]
    
    def _extract_actions(self, content: str) -> List[Dict[str, str]]:
        """Extract action options from LLM response"""
        # Default actions if parsing fails
        return [
            {"action": "Hold & Monitor", "reason": "Wait for trend confirmation"},
            {"action": "Review Allocation", "reason": "Consider rebalancing if impact persists"}
        ]
    
    def _calculate_impact_level(self, sensitivity: float) -> str:
        """Calculate impact severity"""
        if sensitivity >= 0.8:
            return "high"
        elif sensitivity >= 0.6:
            return "moderate"
        elif sensitivity >= 0.4:
            return "mild"
        else:
            return "low"
    
    def generate_daily_brief(
        self, 
        holdings: List[Dict[str, Any]], 
        persona: str = "sip_investor"
    ) -> Dict[str, Any]:
        """Generate daily brief with top 3 impacts"""
        
        impact_cards = self.analyze_portfolio_impact(holdings, persona)
        
        # Generate overall summary
        symbols = [h['symbol'] for h in holdings]
        total_value = sum(h['quantity'] * h['avg_buy_price'] for h in holdings)
        
        brief = {
            "date": "2024-01-15",  # In production, use actual date
            "portfolio_summary": {
                "total_holdings": len(holdings),
                "total_value": round(total_value, 2),
                "symbols": symbols
            },
            "impact_cards": impact_cards,
            "headline": self._generate_headline(impact_cards)
        }
        
        return brief
    
    def _generate_headline(self, cards: List[Dict]) -> str:
        """Generate headline for daily brief"""
        if not cards:
            return "No major impacts detected for your portfolio today"
        
        top_card = cards[0]
        return f"{top_card['impact_level'].upper()}: {top_card['title']}"

# Singleton instance
impact_analyzer = ImpactAnalyzer()