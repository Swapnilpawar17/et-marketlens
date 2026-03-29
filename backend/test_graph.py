from app.graph import neo4j_conn, get_portfolio_exposure, get_stock_info

neo4j_conn.connect()

print("\n📊 Testing Graph Queries...\n")

# Test 1: Get stock info
print("1️⃣ Stock Info for RELIANCE:")
stock = get_stock_info("RELIANCE")
print(stock)

# Test 2: Portfolio exposure analysis
print("\n2️⃣ Factor Exposure for Portfolio [RELIANCE, HDFCBANK, TCS]:")
exposure = get_portfolio_exposure(["RELIANCE", "HDFCBANK", "TCS"])
for item in exposure:
    print(f"  {item['stock']} → {item['factor']} (sensitivity: {item['sensitivity']})")

neo4j_conn.close()