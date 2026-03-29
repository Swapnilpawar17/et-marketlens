from app.agents.mock_impact_analyzer import mock_impact_analyzer as impact_analyzer
# Sample portfolio
test_holdings = [
    {
        "symbol": "RELIANCE",
        "quantity": 10,
        "avg_buy_price": 2450.50,
        "goal_id": "retirement"
    },
    {
        "symbol": "HDFCBANK",
        "quantity": 20,
        "avg_buy_price": 1580.00,
        "goal_id": "retirement"
    },
    {
        "symbol": "TCS",
        "quantity": 5,
        "avg_buy_price": 3600.00,
        "goal_id": "education"
    }
]

print("\n" + "="*60)
print("🧪 Testing Impact Analyzer")
print("="*60 + "\n")

# Test 1: Impact Analysis
print("1️⃣ Generating Impact Cards...\n")
cards = impact_analyzer.analyze_portfolio_impact(test_holdings, "sip_investor")

for i, card in enumerate(cards, 1):
    print(f"\n📊 Card {i}: {card['title']}")
    print(f"   Factor: {card['factor']}")
    print(f"   Impact: {card['impact_level'].upper()}")
    print(f"   Sensitivity: {card['sensitivity_score']}%")
    print(f"   Affected: {', '.join(card['affected_holdings'])}")
    print(f"   Summary: {card['summary'][:150]}...")

# Test 2: Daily Brief
print("\n" + "="*60)
print("2️⃣ Generating Daily Brief...\n")
brief = impact_analyzer.generate_daily_brief(test_holdings, "sip_investor")

print(f"📅 Date: {brief['date']}")
print(f"💼 Portfolio: {brief['portfolio_summary']['total_holdings']} stocks, ₹{brief['portfolio_summary']['total_value']:,.0f}")
print(f"📰 Headline: {brief['headline']}")
print(f"📊 Impact Cards: {len(brief['impact_cards'])}")

print("\n" + "="*60)
print("✅ Impact Analyzer Test Complete!")
print("="*60 + "\n")