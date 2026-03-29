from app.graph.neo4j_connection import neo4j_conn

def create_constraints():
    """Create uniqueness constraints"""
    constraints = [
        "CREATE CONSTRAINT stock_symbol IF NOT EXISTS FOR (s:Stock) REQUIRE s.symbol IS UNIQUE",
        "CREATE CONSTRAINT sector_name IF NOT EXISTS FOR (sec:Sector) REQUIRE sec.name IS UNIQUE",
        "CREATE CONSTRAINT factor_name IF NOT EXISTS FOR (f:Factor) REQUIRE f.name IS UNIQUE",
        "CREATE CONSTRAINT news_id IF NOT EXISTS FOR (n:News) REQUIRE n.id IS UNIQUE",
    ]
    
    for constraint in constraints:
        try:
            neo4j_conn.execute_write(constraint)
            print(f"✅ Created constraint: {constraint[:50]}...")
        except Exception as e:
            print(f"⚠️  Constraint may already exist: {e}")

def create_indexes():
    """Create indexes for performance"""
    indexes = [
        "CREATE INDEX stock_name IF NOT EXISTS FOR (s:Stock) ON (s.name)",
        "CREATE INDEX news_date IF NOT EXISTS FOR (n:News) ON (n.published_date)",
    ]
    
    for index in indexes:
        try:
            neo4j_conn.execute_write(index)
            print(f"✅ Created index: {index[:50]}...")
        except Exception as e:
            print(f"⚠️  Index may already exist: {e}")

def initialize_schema():
    """Initialize complete graph schema"""
    print("\n🏗️  Initializing Neo4j Schema...")
    
    if not neo4j_conn.connect():
        print("❌ Cannot initialize schema without database connection")
        return False
    
    create_constraints()
    create_indexes()
    
    print("✅ Schema initialization complete!\n")
    return True