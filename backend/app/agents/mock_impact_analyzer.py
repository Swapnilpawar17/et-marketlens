from typing import List, Dict, Any
from app.graph import get_portfolio_exposure

class MockImpactAnalyzer:
    """Mock analyzer that doesn't use LLM - for testing without OpenAI key"""
    
    def analyze_portfolio_impact(
        self, 
        holdings: List[Dict[str, Any]], 
        persona: str = "sip_investor"
    ) -> List[Dict[str, Any]]:
        """Generate mock impact cards"""
        
        symbols = [h['symbol'] for h in holdings]
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
        
        # Generate cards
        impact_cards = []
        sorted_factors = sorted(
            factor_impacts.values(), 
            key=lambda x: x['max_sensitivity'], 
            reverse=True
        )[:3]
        
        # Mock card templates
        templates = {
            "CrudeOilPrice": {
                "title": "Crude Oil Spike Affects Energy Stocks",
                "summary": "Crude oil prices at ${value}/barrel impact your Reliance holdings. Higher oil prices can squeeze refining margins but boost upstream profits. For long-term SIP investors, this is normal volatility."
            },
            "RepoRate": {
                "title": "RBI Rate Hike Impacts Bank Stocks",
                "summary": "Repo rate at {value}% affects banking stocks like HDFC Bank. Higher rates improve Net Interest Margins (NIM) but may slow loan growth. Banks typically adjust within 2-3 quarters."
            },
            "USDINRRate": {
                "title": "Rupee Movement Benefits IT Exporters",
                "summary": "USD/INR at {value} improves revenue realization for IT companies like TCS. A weaker rupee means higher rupee earnings from dollar revenues. Good news for IT holdings."
            },
            "FIIFlow": {
                "title": "Foreign Fund Outflows Create Volatility",
                "summary": "FII outflow of ₹{value}cr creates short-term market pressure. This affects all your stocks but is typically temporary. Good time to continue SIPs at lower prices."
            },
            "Monsoon": {
                "title": "Monsoon Progress Affects Rural Demand",
                "summary": "Monsoon at {value}% of normal affects consumer and auto stocks. Better monsoon = higher rural income = more demand for your FMCG holdings."
            },
            "GST_Collections": {
                "title": "Strong GST Collections Signal Economic Health",
                "summary": "GST collections at ₹{value}cr indicate robust economic activity. This is positive for all your holdings, especially banking and consumer stocks."
            }
        }
        
        for factor_data in sorted_factors:
            factor_name = factor_data['factor']
            template = templates.get(factor_name, {
                "title": f"{factor_name} Movement Detected",
                "summary": f"{factor_name} at {factor_data['factor_value']} affects your portfolio."
            })
            
            card = {
                "factor": factor_name,
                "title": template["title"],
                "impact_level": self._calculate_impact_level(factor_data['max_sensitivity']),
                "summary": template["summary"].replace("{value}", str(factor_data['factor_value'])),
                "affected_holdings": [s['symbol'] for s in factor_data['stocks']],
                "sensitivity_score": round(factor_data['max_sensitivity'] * 100, 1),
                "action_options": [
                    {"action": "Hold & Monitor", "reason": "Continue your SIP as planned"},
                    {"action": "Review Allocation", "reason": "Check if rebalancing needed"}
                ],
                "llm_explanation": f"[Mock] {template['summary']}"
            }
            impact_cards.append(card)
        
        return impact_cards
    
    def _calculate_impact_level(self, sensitivity: float) -> str:
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
        """Generate mock daily brief"""
        
        impact_cards = self.analyze_portfolio_impact(holdings, persona)
        symbols = [h['symbol'] for h in holdings]
        total_value = sum(h['quantity'] * h['avg_buy_price'] for h in holdings)
        
        return {
            "date": "2024-01-15",
            "portfolio_summary": {
                "total_holdings": len(holdings),
                "total_value": round(total_value, 2),
                "symbols": symbols
            },
            "impact_cards": impact_cards,
            "headline": f"{impact_cards[0]['impact_level'].upper()}: {impact_cards[0]['title']}" if impact_cards else "No major impacts today"
        }

# Singleton
mock_impact_analyzer = MockImpactAnalyzer()