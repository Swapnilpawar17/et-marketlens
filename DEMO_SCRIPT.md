[0:00-0:20] OPENING + PROBLEM
"Hi, I'm [Name] from Team GenX. India has 14 crore demat accounts, but investors drown in ET news without knowing what matters for THEIR money.

[Show ET MarketLens homepage]

When RBI hikes rates, should I sell my SBI stock? When crude spikes, how does it affect Reliance? Current solutions give generic alerts with no portfolio context."

[0:20-1:00] SOLUTION OVERVIEW
"We built ET MarketLens—an AI brain that answers 'What does today's news mean for MY portfolio?'

[Point to architecture on screen]

Under the hood: A Neo4j knowledge graph maps 15 Indian stocks to India-first factors like monsoon, PLI schemes, and FII flows. FastAPI backend with LangChain queries this graph. OpenAI generates insights in plain Hindi-English. Next.js frontend displays results.

[Show quick diagram]

Let me show you how it works."

[1:00-2:00] LIVE DEMO
"I visit etmarketlens.vercel.app...

[Navigate to site]

...and click 'Load Sample Portfolio.'

[Click button - show 3 stocks appear]

I have Reliance, HDFC Bank, and TCS. Now I click 'Generate Daily Brief.'

[Click - wait for cards]

In 3 seconds, MarketLens shows me 3 personalized impact cards.

[Point to each card]

Card 1: Crude oil spike. HIGH impact. 95% sensitivity. Affects my Reliance holdings. Plain language summary—no jargon. Action options: Hold & Monitor, or Review Allocation.

Card 2: RBI rate hike impacts bank stocks. 90% sensitivity on HDFC Bank. Banks benefit from higher margins.

Card 3: Rupee weakness helps IT exporters. TCS benefits from better dollar realization.

Each card shows exactly which of MY stocks are affected and WHY."

[2:00-2:40] DIFFERENTIATION
"What makes this unique?

First, only ET can build this—you own the content, portfolio data, and trust. Bloomberg doesn't model monsoon or PLI.

Second, it's a noise firewall. 1000 ET stories become 3 actionable signals for MY goals.

Third, it's goal-aware. If I'm a long-term SIP investor, it prevents panic selling. If I'm a trader, it shows opportunities.

[Show backend API docs quickly]

The system handles errors gracefully—if OpenAI fails, we use mock templates. If Neo4j is slow, we cache queries. Everything is production-ready."

[2:40-3:00] CLOSING
"Business impact: 14 crore target users. At 1% penetration, that's ₹500 crore ARR. We save investors time and money—₹3.5 lakh value per year for just ₹18,000 subscription.

Live demo: etmarketlens.vercel.app
GitHub: github.com/[YOUR-USERNAME]/et-marketlens

Thank you! Team GenX."

[Show URL on screen for 3 seconds]