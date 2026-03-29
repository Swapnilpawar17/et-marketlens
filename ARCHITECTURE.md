\# ET MarketLens - Architecture Document

\*\*Team GenX | ET GenAI Hackathon 2026\*\*



\---



\## System Architecture Overview



\### High-Level Architecture

┌─────────────────────────────────────────────────────────────────┐

│ USER LAYER │

│ Web Browser (Desktop/Mobile) → https://etmarketlens.vercel.app │

└────────────────────────┬────────────────────────────────────────┘

│

▼

┌─────────────────────────────────────────────────────────────────┐

│ PRESENTATION LAYER │

│ ┌──────────────────────────────────────────────────────────┐ │

│ │ Next.js 15 Frontend (React 18) │ │

│ │ - Server-Side Rendering (SSR) │ │

│ │ - Tailwind CSS for responsive UI │ │

│ │ - Axios for API communication │ │

│ │ Deployed: Vercel Edge Network │ │

│ └──────────────────────────────────────────────────────────┘ │

└────────────────────────┬────────────────────────────────────────┘

│ HTTPS REST API

▼

┌─────────────────────────────────────────────────────────────────┐

│ APPLICATION LAYER │

│ ┌──────────────────────────────────────────────────────────┐ │

│ │ FastAPI Backend (Python 3.11) │ │

│ │ https://et-marketlens.onrender.com │ │

│ │ │ │

│ │ ┌─────────────────────────────────────────────────┐ │ │

│ │ │ API Endpoints │ │ │

│ │ │ - POST /api/portfolio/upload │ │ │

│ │ │ - POST /api/impact/analyze │ │ │

│ │ │ - POST /api/impact/daily-brief │ │ │

│ │ │ - GET /docs (Swagger UI) │ │ │

│ │ └─────────────────────────────────────────────────┘ │ │

│ │ │ │

│ │ ┌─────────────────────────────────────────────────┐ │ │

│ │ │ LangChain Agent Layer │ │ │

│ │ │ - Impact Analyzer Agent │ │ │

│ │ │ - Portfolio Context Manager │ │ │

│ │ │ - RAG Pipeline (Graph + LLM) │ │ │

│ │ └─────────────────────────────────────────────────┘ │ │

│ │ │ │

│ │ Deployed: Render (Auto-scaling) │ │

│ └──────────────────────────────────────────────────────────┘ │

└────────────┬────────────────────┬─────────────────────────────┘

│ │

▼ ▼

┌─────────────────────┐ ┌──────────────────────────────────────┐

│ DATA LAYER │ │ AI/ML LAYER │

│ Neo4j Aura Cloud │ │ OpenAI GPT-4o Mini │

│ Knowledge Graph │ │ (via LangChain) │

│ │ │ │

│ 32 Nodes: │ │ Tasks: │

│ - 15 Stocks │ │ - Natural language generation │

│ - 8 Sectors │ │ - Impact card creation │

│ - 6 Macro Factors │ │ - Sentiment analysis │

│ - 3 News Articles │ │ - Action recommendation │

│ │ │ │

│ 23 Relationships │ │ Fallback: Mock Analyzer │

│ Cypher Queries │ │ (No API key needed) │

└─────────────────────┘ └──────────────────────────────────────┘



text





\---



\## Agent Architecture



\### Agent Roles \& Communication



\#### \*\*1. Impact Analyzer Agent\*\*

\*\*Role:\*\* Analyzes portfolio exposure to macro factors



\*\*Inputs:\*\*

\- User portfolio holdings (symbols, quantities, prices)

\- User persona (sip\_investor, trader, value\_investor)



\*\*Process:\*\*

1\. Extract stock symbols from portfolio

2\. Query Neo4j graph for factor exposure

3\. Calculate sensitivity scores (beta × factor weight)

4\. Rank factors by impact level



\*\*Outputs:\*\*

\- Top 3 impact factors

\- Sensitivity scores (0-100%)

\- Affected holdings list



\*\*Communication:\*\*

```python

\# Internal message flow

portfolio\_data → graph\_query\_tool → exposure\_results → 

scoring\_engine → ranked\_factors → card\_generator\_agent

Error Handling:



If Neo4j unavailable: Return cached factor relationships

If symbols not found: Log warning, continue with valid symbols

If API timeout: Return top factors from last successful query

2\. Card Generator Agent

Role: Creates plain-language impact cards using LLM



Inputs:



Factor exposure data from Analyzer Agent

User persona context

Portfolio value \& goals

Tools Integrated:



OpenAI GPT-4o: For natural language generation

Prompt Template Engine: Persona-aware prompts

Structured Output Parser: JSON response validation

Process:



Python



def generate\_card(factor\_data, persona):

&#x20;   # 1. Build context

&#x20;   context = {

&#x20;       "factor": factor\_data.factor\_name,

&#x20;       "sensitivity": factor\_data.max\_sensitivity,

&#x20;       "affected\_stocks": factor\_data.stocks,

&#x20;       "persona": persona\_profiles\[persona]

&#x20;   }

&#x20;   

&#x20;   # 2. Create prompt

&#x20;   prompt = ChatPromptTemplate(\[

&#x20;       SystemMessage("You are ET MarketLens AI..."),

&#x20;       HumanMessage(context)

&#x20;   ])

&#x20;   

&#x20;   # 3. Call LLM

&#x20;   response = llm.invoke(prompt)

&#x20;   

&#x20;   # 4. Parse \& validate

&#x20;   card = parse\_impact\_card(response.content)

&#x20;   

&#x20;   # 5. Error handling

&#x20;   if not card.is\_valid():

&#x20;       return fallback\_card(factor\_data)

&#x20;   

&#x20;   return card

Outputs:



Impact card JSON with:

Title (8 words max)

Summary (3 sentences, simple Hindi-English)

Impact level (high/moderate/mild/low)

Action options (2 choices)

Error Handling:



If OpenAI API fails: Use mock analyzer with pre-defined templates

If response parsing fails: Return structured fallback card

If rate limit hit: Queue request, return "Analyzing..." placeholder

3\. Graph Query Tool

Role: Fetch factor relationships from Neo4j



Queries:



cypher



// Get portfolio exposure

MATCH (s:Stock)-\[:BELONGS\_TO]->(sec:Sector)-\[r:SENSITIVE\_TO]->(f:Factor)

WHERE s.symbol IN $symbols

RETURN s.symbol, sec.name, f.name, r.sensitivity, f.current\_value

ORDER BY r.sensitivity DESC



// Get peer stocks

MATCH (s:Stock {symbol: $symbol})-\[:BELONGS\_TO]->(sec)<-\[:BELONGS\_TO]-(peer)

WHERE s <> peer

RETURN peer.symbol, peer.name, peer.beta

ORDER BY peer.market\_cap DESC

LIMIT 5

Error Handling:



Retry logic: 3 attempts with exponential backoff

Connection pooling: Reuse driver sessions

Fallback: Return last cached query results (5 min TTL)

Data Flow - End-to-End Example

User Action: "Generate Daily Brief"

text



1\. USER CLICKS BUTTON

&#x20;  ↓

2\. FRONTEND (Next.js)

&#x20;  - Collects portfolio state

&#x20;  - POST /api/impact/daily-brief

&#x20;  - Shows loading spinner

&#x20;  ↓

3\. API ENDPOINT (FastAPI)

&#x20;  - Validates request (Pydantic schema)

&#x20;  - Calls impact\_analyzer.generate\_daily\_brief()

&#x20;  ↓

4\. IMPACT ANALYZER AGENT

&#x20;  - Extracts symbols: \["RELIANCE", "HDFCBANK", "TCS"]

&#x20;  - Calls graph\_query\_tool.get\_portfolio\_exposure(symbols)

&#x20;  ↓

5\. NEO4J GRAPH TOOL

&#x20;  - Executes Cypher query

&#x20;  - Returns exposure data:

&#x20;    {

&#x20;      "RELIANCE": {"CrudeOilPrice": 0.95},

&#x20;      "HDFCBANK": {"RepoRate": 0.90},

&#x20;      "TCS": {"USDINRRate": 0.80}

&#x20;    }

&#x20;  ↓

6\. IMPACT ANALYZER

&#x20;  - Groups by factor

&#x20;  - Scores impact: CrudeOilPrice (95%), RepoRate (90%), USDINRRate (80%)

&#x20;  - Selects top 3

&#x20;  ↓

7\. CARD GENERATOR AGENT (for each factor)

&#x20;  - Builds persona-aware prompt

&#x20;  - Calls OpenAI GPT-4o via LangChain

&#x20;  - Parses response into structured JSON

&#x20;  ↓

8\. LLM RESPONSE

&#x20;  {

&#x20;    "title": "Crude Oil Spike Affects Energy Stocks",

&#x20;    "summary": "Crude oil at $85/barrel impacts Reliance...",

&#x20;    "impact\_level": "high",

&#x20;    "action\_options": \[...]

&#x20;  }

&#x20;  ↓

9\. API RESPONSE

&#x20;  - Aggregates 3 cards

&#x20;  - Returns JSON to frontend

&#x20;  ↓

10\. FRONTEND RENDERS

&#x20;   - Displays impact cards with color coding

&#x20;   - Shows action buttons

&#x20;   - Updates portfolio summary

Total Latency: 2-4 seconds



Neo4j query: 200ms

LLM calls (3): 1.5-2s

API processing: 300ms

Error Handling Strategy

Layered Fallbacks

Level 1: Component Retry



Python



@retry(stop=stop\_after\_attempt(3), wait=wait\_exponential(min=1, max=10))

def query\_graph(symbols):

&#x20;   return neo4j\_conn.execute\_query(query, {"symbols": symbols})

Level 2: Service Fallback



Python



try:

&#x20;   result = openai\_analyzer.generate\_card(data)

except OpenAIError:

&#x20;   logger.warning("OpenAI failed, using mock analyzer")

&#x20;   result = mock\_analyzer.generate\_card(data)

Level 3: Graceful Degradation



Python



if not neo4j\_conn.driver:

&#x20;   # Use cached factor mappings

&#x20;   return FALLBACK\_FACTOR\_MAP\[symbol]

Level 4: User-Facing Error



JSON



{

&#x20; "error": "Unable to generate impact cards",

&#x20; "fallback": "Showing static portfolio summary",

&#x20; "retry\_in": 30

}

Deployment Architecture

Production Environment

Frontend (Vercel):



Region: Global Edge Network

CDN: Automatic

SSL: Auto-provisioned

Scaling: Auto (serverless)

Environment: Production + Preview branches

Backend (Render):



Region: Singapore (closest to India)

Instance: Free tier (512MB RAM)

Scaling: Manual (upgradeable)

Auto-deploy: On git push

Health checks: Every 5 minutes

Database (Neo4j Aura):



Region: GCP asia-south1 (Mumbai)

Tier: Free (200k ops/month)

Backup: Daily snapshots

Security: TLS 1.2+

CI/CD Pipeline

text



git push origin main

&#x20;     ↓

GitHub Actions (optional)

&#x20;     ↓

&#x20;  ┌──────┴──────┐

&#x20;  ▼             ▼

Vercel        Render

Auto-deploy   Auto-deploy

&#x20;  │             │

&#x20;  ▼             ▼

Production    Production

Frontend      Backend

Security Considerations

API Keys: Environment variables only (never in code)

CORS: Whitelist specific origins

Rate Limiting: 100 req/min per IP (future)

Input Validation: Pydantic schemas enforce types

SQL Injection: N/A (using Cypher, parameterized queries)

Authentication: Not implemented in MVP (future: OAuth)

Scalability Roadmap

Current Capacity:



10 concurrent users

100 portfolios/hour

300 impact cards/hour

Phase 1 Scaling (Month 1):



Redis caching (95% cache hit rate)

PostgreSQL for user data

Load balancer (2 backend instances)

Target: 1000 concurrent users

Phase 2 Scaling (Quarter 1):



Kubernetes deployment

Horizontal pod autoscaling

Neo4j Enterprise (sharding)

Target: 100k concurrent users

Document Version: 1.0

Last Updated: March 2026

Team: GenX

