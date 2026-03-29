from app.graph.neo4j_connection import neo4j_conn

# Sample Indian stocks with metadata
SAMPLE_STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "Energy", "beta": 1.1, "market_cap": 1700000},
    {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "IT", "beta": 0.8, "market_cap": 1300000},
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "Banking", "beta": 1.0, "market_cap": 1200000},
    {"symbol": "INFY", "name": "Infosys", "sector": "IT", "beta": 0.9, "market_cap": 700000},
    {"symbol": "ICICIBANK", "name": "ICICI Bank", "sector": "Banking", "beta": 1.2, "market_cap": 650000},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever", "sector": "FMCG", "beta": 0.6, "market_cap": 600000},
    {"symbol": "ITC", "name": "ITC Limited", "sector": "FMCG", "beta": 0.7, "market_cap": 550000},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Banking", "beta": 1.3, "market_cap": 500000},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel", "sector": "Telecom", "beta": 0.9, "market_cap": 450000},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank", "sector": "Banking", "beta": 1.1, "market_cap": 400000},
    {"symbol": "LT", "name": "Larsen & Toubro", "sector": "Engineering", "beta": 1.2, "market_cap": 380000},
    {"symbol": "AXISBANK", "name": "Axis Bank", "sector": "Banking", "beta": 1.2, "market_cap": 350000},
    {"symbol": "WIPRO", "name": "Wipro", "sector": "IT", "beta": 0.85, "market_cap": 320000},
    {"symbol": "ASIANPAINT", "name": "Asian Paints", "sector": "Consumer Durables", "beta": 0.75, "market_cap": 300000},
    {"symbol": "MARUTI", "name": "Maruti Suzuki", "sector": "Automobile", "beta": 1.1, "market_cap": 280000},
]

# Macro factors affecting Indian markets
MACRO_FACTORS = [
    {"name": "RepoRate", "current_value": 6.5, "impact": "interest_rates"},
    {"name": "CrudeOilPrice", "current_value": 85.0, "impact": "commodity"},
    {"name": "USDINRRate", "current_value": 83.0, "impact": "forex"},
    {"name": "Monsoon", "current_value": 95.0, "impact": "agriculture"},
    {"name": "FIIFlow", "current_value": -2000.0, "impact": "liquidity"},
    {"name": "GST_Collections", "current_value": 165000.0, "impact": "economy"},
]

# Sector definitions
SECTORS = [
    {"name": "Banking", "type": "Financial"},
    {"name": "IT", "type": "Technology"},
    {"name": "Energy", "type": "Commodity"},
    {"name": "FMCG", "type": "Consumer"},
    {"name": "Automobile", "type": "Cyclical"},
    {"name": "Telecom", "type": "Services"},
    {"name": "Engineering", "type": "Infrastructure"},
    {"name": "Consumer Durables", "type": "Consumer"},
]

def load_stocks():
    """Load stock nodes"""
    query = """
    UNWIND $stocks AS stock
    MERGE (s:Stock {symbol: stock.symbol})
    SET s.name = stock.name,
        s.beta = stock.beta,
        s.market_cap = stock.market_cap,
        s.sector_name = stock.sector
    """
    neo4j_conn.execute_write(query, {"stocks": SAMPLE_STOCKS})
    print(f"✅ Loaded {len(SAMPLE_STOCKS)} stocks")

def load_sectors():
    """Load sector nodes"""
    query = """
    UNWIND $sectors AS sector
    MERGE (sec:Sector {name: sector.name})
    SET sec.type = sector.type
    """
    neo4j_conn.execute_write(query, {"sectors": SECTORS})
    print(f"✅ Loaded {len(SECTORS)} sectors")

def load_factors():
    """Load macro factor nodes"""
    query = """
    UNWIND $factors AS factor
    MERGE (f:Factor {name: factor.name})
    SET f.current_value = factor.current_value,
        f.impact = factor.impact
    """
    neo4j_conn.execute_write(query, {"factors": MACRO_FACTORS})
    print(f"✅ Loaded {len(MACRO_FACTORS)} macro factors")

def create_relationships():
    """Create relationships between entities"""
    
    # Stock -> Sector
    query1 = """
    MATCH (s:Stock), (sec:Sector)
    WHERE s.sector_name = sec.name
    MERGE (s)-[:BELONGS_TO]->(sec)
    """
    neo4j_conn.execute_write(query1)
    print("✅ Created Stock->Sector relationships")
    
    # Sector -> Factor (domain knowledge)
    relationships = [
        ("Banking", "RepoRate", 0.9),  # High sensitivity
        ("Banking", "FIIFlow", 0.7),
        ("IT", "USDINRRate", 0.8),
        ("IT", "FIIFlow", 0.6),
        ("Energy", "CrudeOilPrice", 0.95),
        ("FMCG", "Monsoon", 0.6),
        ("Automobile", "RepoRate", 0.7),
        ("Automobile", "CrudeOilPrice", 0.5),
    ]
    
    query2 = """
    UNWIND $rels AS rel
    MATCH (sec:Sector {name: rel.sector}), (f:Factor {name: rel.factor})
    MERGE (sec)-[r:SENSITIVE_TO]->(f)
    SET r.sensitivity = rel.sensitivity
    """
    
    rel_data = [
        {"sector": r[0], "factor": r[1], "sensitivity": r[2]} 
        for r in relationships
    ]
    neo4j_conn.execute_write(query2, {"rels": rel_data})
    print(f"✅ Created {len(relationships)} Sector->Factor relationships")

def load_sample_news():
    """Load sample news articles"""
    news_articles = [
        {
            "id": "news001",
            "title": "RBI hikes repo rate by 25 bps to 6.5%",
            "sentiment": -0.3,
            "published_date": "2024-01-15",
            "mentioned_stocks": ["HDFCBANK", "SBIN", "ICICIBANK"]
        },
        {
            "id": "news002",
            "title": "Crude oil prices surge to $90/barrel",
            "sentiment": -0.5,
            "published_date": "2024-01-16",
            "mentioned_stocks": ["RELIANCE", "MARUTI"]
        },
        {
            "id": "news003",
            "title": "IT sector sees strong Q3 results",
            "sentiment": 0.7,
            "published_date": "2024-01-17",
            "mentioned_stocks": ["TCS", "INFY", "WIPRO"]
        },
    ]
    
    # Create news nodes
    query1 = """
    UNWIND $news AS article
    MERGE (n:News {id: article.id})
    SET n.title = article.title,
        n.sentiment = article.sentiment,
        n.published_date = article.published_date
    """
    neo4j_conn.execute_write(query1, {"news": news_articles})
    
    # Link news to stocks
    query2 = """
    UNWIND $news AS article
    MATCH (n:News {id: article.id})
    UNWIND article.mentioned_stocks AS stock_symbol
    MATCH (s:Stock {symbol: stock_symbol})
    MERGE (n)-[:MENTIONS]->(s)
    """
    neo4j_conn.execute_write(query2, {"news": news_articles})
    
    print(f"✅ Loaded {len(news_articles)} news articles")

def initialize_sample_data():
    """Load all sample data"""
    print("\n📊 Loading Sample Data into Neo4j...")
    
    if not neo4j_conn.driver:
        neo4j_conn.connect()
    
    load_stocks()
    load_sectors()
    load_factors()
    create_relationships()
    load_sample_news()
    
    print("✅ Sample data loading complete!\n")