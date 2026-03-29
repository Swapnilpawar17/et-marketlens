from app.graph.neo4j_connection import neo4j_conn

def get_portfolio_exposure(symbols: list):
    """Get all factors affecting portfolio stocks"""
    query = """
    MATCH (s:Stock)-[:BELONGS_TO]->(sec:Sector)-[r:SENSITIVE_TO]->(f:Factor)
    WHERE s.symbol IN $symbols
    RETURN s.symbol AS stock, 
           sec.name AS sector, 
           f.name AS factor, 
           r.sensitivity AS sensitivity,
           f.current_value AS factor_value
    ORDER BY r.sensitivity DESC
    """
    return neo4j_conn.execute_query(query, {"symbols": symbols})

def get_news_impact(stock_symbol: str):
    """Get recent news mentioning a stock"""
    query = """
    MATCH (n:News)-[:MENTIONS]->(s:Stock {symbol: $symbol})
    RETURN n.id AS news_id,
           n.title AS title,
           n.sentiment AS sentiment,
           n.published_date AS date
    ORDER BY n.published_date DESC
    LIMIT 5
    """
    return neo4j_conn.execute_query(query, {"symbol": stock_symbol})

def get_stock_info(symbol: str):
    """Get detailed stock information"""
    query = """
    MATCH (s:Stock {symbol: $symbol})-[:BELONGS_TO]->(sec:Sector)
    RETURN s.symbol AS symbol,
           s.name AS name,
           s.beta AS beta,
           s.market_cap AS market_cap,
           sec.name AS sector,
           sec.type AS sector_type
    """
    result = neo4j_conn.execute_query(query, {"symbol": symbol})
    return result[0] if result else None

def get_sector_peers(symbol: str, limit: int = 5):
    """Get peer stocks in the same sector"""
    query = """
    MATCH (s:Stock {symbol: $symbol})-[:BELONGS_TO]->(sec:Sector)<-[:BELONGS_TO]-(peer:Stock)
    WHERE s.symbol <> peer.symbol
    RETURN peer.symbol AS symbol,
           peer.name AS name,
           peer.beta AS beta
    ORDER BY peer.market_cap DESC
    LIMIT $limit
    """
    return neo4j_conn.execute_query(query, {"symbol": symbol, "limit": limit})