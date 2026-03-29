from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME", os.getenv("NEO4J_USER", "neo4j"))
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.driver = None
        
    def connect(self):
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            # Test connection
            self.driver.verify_connectivity()
            print(f"✅ Connected to Neo4j at {self.uri}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            return False
    
    def close(self):
        """Close connection"""
        if self.driver:
            self.driver.close()
            print("🔌 Neo4j connection closed")
    
    def execute_query(self, query, parameters=None):
        """Execute a Cypher query"""
        if not self.driver:
            self.connect()
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def execute_write(self, query, parameters=None):
        """Execute a write query"""
        if not self.driver:
            self.connect()
        
        with self.driver.session(database=self.database) as session:
            result = session.execute_write(
                lambda tx: tx.run(query, parameters or {})
            )
            return result

# Singleton instance
neo4j_conn = Neo4jConnection()