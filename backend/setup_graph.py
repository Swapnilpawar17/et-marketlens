"""
One-time script to initialize Neo4j graph database
Run this after setting up Neo4j Aura
"""
from app.graph import initialize_schema, initialize_sample_data, neo4j_conn

def main():
    print("=" * 60)
    print("ET MarketLens - Neo4j Graph Initialization")
    print("=" * 60)
    
    # Test connection
    if not neo4j_conn.connect():
        print("\n❌ Failed to connect to Neo4j")
        print("Please check your .env file has correct credentials:")
        print("  NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io")
        print("  NEO4J_USER=neo4j")
        print("  NEO4J_PASSWORD=your-password")
        return
    
    # Initialize schema
    initialize_schema()
    
    # Load sample data
    initialize_sample_data()
    
    # Verify data
    print("\n🔍 Verifying data...")
    result = neo4j_conn.execute_query("MATCH (n) RETURN count(n) AS total_nodes")
    print(f"✅ Total nodes in database: {result[0]['total_nodes']}")
    
    # Close connection
    neo4j_conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Graph initialization complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()