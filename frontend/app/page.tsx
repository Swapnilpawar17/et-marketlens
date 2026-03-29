'use client';

import React, { useState } from 'react';
import { BarChart3, Upload, Sparkles, TrendingUp, AlertCircle } from 'lucide-react';

interface Holding {
  symbol: string;
  quantity: number;
  avg_buy_price: number;
}

interface ImpactCard {
  factor: string;
  title: string;
  impact_level: 'high' | 'moderate' | 'mild' | 'low';
  summary: string;
  affected_holdings: string[];
  sensitivity_score: number;
  action_options: Array<{
    action: string;
    reason: string;
  }>;
  news_count?: number;
  last_updated?: string;
}

interface DailyBrief {
  date: string;
  portfolio_summary: {
    total_holdings: number;
    total_value: number;
    symbols: string[];
    day_change?: number;
    day_change_pct?: number;
  };
  impact_cards: ImpactCard[];
  headline: string;
  market_mood?: string;
  top_news?: Array<{
    title: string;
    source: string;
    time: string;
  }>;
}

export default function Dashboard() {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [dailyBrief, setDailyBrief] = useState<DailyBrief | null>(null);
  const [loading, setLoading] = useState(false);
  const [showUpload, setShowUpload] = useState(true);

  const generateMockBrief = (currentHoldings: Holding[]) => {
    setLoading(true);
    
    setTimeout(() => {
      const mockBrief: DailyBrief = {
        date: new Date().toISOString().split('T')[0],
        portfolio_summary: {
          total_holdings: currentHoldings.length,
          total_value: currentHoldings.reduce((sum, h) => sum + (h.quantity * h.avg_buy_price), 0),
          symbols: currentHoldings.map(h => h.symbol),
          day_change: 2350.50,
          day_change_pct: 1.2,
        },
        impact_cards: [
          {
            factor: 'CrudeOilPrice',
            title: '🛢️ Crude Oil Surge Impacts Energy Holdings',
            impact_level: 'high',
            summary: 'Brent crude at $87/barrel (+12% this month) directly impacts Reliance Industries refining margins. While higher oil prices pressure downstream operations, upstream E&P benefits from improved realization. For long-term SIP investors, this is typical commodity volatility. Reliance has hedged 60% of FY25 crude exposure.',
            affected_holdings: ['RELIANCE'],
            sensitivity_score: 95.0,
            action_options: [
              { action: '✓ Hold & Monitor', reason: 'Continue SIP as planned. Oil prices historically mean-revert within 6 months.' },
              { action: '⚡ Opportunistic Add', reason: 'If Reliance corrects >5%, consider increasing SIP amount next month.' }
            ],
            news_count: 3,
            last_updated: '2 hours ago'
          },
          {
            factor: 'RepoRate',
            title: '💹 RBI Rate Pause Benefits Banking Stocks',
            impact_level: 'high',
            summary: 'RBI held repo rate at 6.5% (in line with expectations). HDFC Bank and other lenders benefit from stable Net Interest Margins (NIM) while credit growth remains strong at 16% YoY. PSU banks show NIM expansion of 20-30 bps. Deposit costs have peaked, improving profitability outlook for H2 FY25.',
            affected_holdings: ['HDFCBANK'],
            sensitivity_score: 90.0,
            action_options: [
              { action: '✓ Stay Invested', reason: 'Banking sector trades at 2.5x P/B vs 10-year avg of 2.8x. Room for rerating.' },
              { action: '📊 Diversify Within Sector', reason: 'Consider adding PSU banks (SBI/PNB) for better NIM expansion play.' }
            ],
            news_count: 5,
            last_updated: '4 hours ago'
          },
          {
            factor: 'USDINRRate',
            title: '💵 Rupee Weakness Boosts IT Exporters',
            impact_level: 'moderate',
            summary: 'USD/INR at ₹83.2 (+0.8% this quarter) improves revenue realization for TCS and Infosys. Every ₹1 depreciation adds 40-50 bps to EBITDA margins. Q3 earnings will reflect this tailwind. However, RBI intervention may cap further depreciation. Cross-currency headwinds (EUR weakness) partially offset gains.',
            affected_holdings: ['TCS', 'INFY'],
            sensitivity_score: 80.0,
            action_options: [
              { action: '✓ Book Partial Profits', reason: 'If IT stocks rally 5%+ post-Q3 results, consider profit booking.' },
              { action: '🔄 Rebalance', reason: 'Maintain IT allocation at 20-25% of equity portfolio for diversification.' }
            ],
            news_count: 2,
            last_updated: '1 day ago'
          },
          {
            factor: 'FIIFlow',
            title: '🌍 FII Selling Creates Short-Term Pressure',
            impact_level: 'mild',
            summary: 'Foreign investors sold ₹12,500 crore in cash segment this month amid US Fed hawkishness. This creates temporary volatility across your portfolio, especially in large-caps like TCS and HDFC Bank. However, DII buying (₹15,200 crore) has absorbed selling. Historically, FII selling phases last 2-3 months before reversal.',
            affected_holdings: ['TCS', 'HDFCBANK', 'RELIANCE', 'INFY'],
            sensitivity_score: 70.0,
            action_options: [
              { action: '💪 Increase SIP', reason: 'Market corrections are buying opportunities for long-term investors.' },
              { action: '⏳ Wait & Watch', reason: 'If correction deepens >8%, deploy lumpsum in quality stocks.' }
            ],
            news_count: 7,
            last_updated: '6 hours ago'
          },
          {
            factor: 'GST_Collections',
            title: '📈 Strong GST Collections Signal Economic Health',
            impact_level: 'low',
            summary: 'November GST collections at ₹1.68 lakh crore (+15% YoY) indicate robust consumption and compliance. This is positive for consumer-facing stocks like ITC (cigarettes + FMCG). Sustained collections above ₹1.6L cr support government capex, indirectly benefiting infrastructure and banking sectors.',
            affected_holdings: ['ITC'],
            sensitivity_score: 60.0,
            action_options: [
              { action: '✓ Stay Course', reason: 'ITC valuation at 22x PE is reasonable. Dividend yield of 4% adds cushion.' },
              { action: '🎯 Set Target', reason: 'Book profits if ITC crosses ₹480 (10% upside from current levels).' }
            ],
            news_count: 1,
            last_updated: '3 days ago'
          }
        ],
        headline: 'MODERATE IMPACT: 5 Key Factors Affecting Your Portfolio Today',
        market_mood: 'Cautiously Optimistic',
        top_news: [
          { title: 'RBI holds rates, maintains accommodative stance', source: 'ET Markets', time: '2h ago' },
          { title: 'Crude oil hits $87 on supply concerns', source: 'ET Energy', time: '4h ago' },
          { title: 'IT sector braces for strong Q3 on rupee tailwind', source: 'ET Tech', time: '1d ago' },
        ]
      };
      
      setDailyBrief(mockBrief);
      setLoading(false);
    }, 2500);
  };

  const loadSamplePortfolio = () => {
    const sample: Holding[] = [
      { symbol: 'RELIANCE', quantity: 10, avg_buy_price: 2450.50 },
      { symbol: 'HDFCBANK', quantity: 20, avg_buy_price: 1580.00 },
      { symbol: 'TCS', quantity: 5, avg_buy_price: 3600.00 },
      { symbol: 'INFY', quantity: 15, avg_buy_price: 1450.75 },
      { symbol: 'ITC', quantity: 100, avg_buy_price: 420.00 },
    ];
    setHoldings(sample);
    setShowUpload(false);
    
    setTimeout(() => {
      generateMockBrief(sample);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2 rounded-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-orange-600 bg-clip-text text-transparent">
                  ET MarketLens
                </h1>
                <p className="text-sm text-gray-600">Portfolio-Aware News Intelligence</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-700">Demo User</p>
                <p className="text-xs text-gray-500">SIP Investor • ₹10.5L Portfolio</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                DU
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Upload Section */}
        {showUpload && (
          <div className="bg-white rounded-2xl shadow-xl p-12 mb-6 text-center border border-gray-100">
            <div className="bg-gradient-to-br from-blue-100 to-orange-100 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <Upload className="w-10 h-10 text-blue-600" />
            </div>
            <h2 className="text-3xl font-bold mb-3 text-gray-900">Upload Your Portfolio</h2>
            <p className="text-gray-600 mb-8 text-lg max-w-2xl mx-auto">
              Get AI-powered impact analysis showing exactly how today's news affects YOUR holdings
            </p>
            <button
              onClick={loadSamplePortfolio}
              className="bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              🚀 Load Sample Portfolio & Analyze
            </button>
            <p className="text-sm text-gray-500 mt-4">
              Demo includes: RELIANCE, HDFC Bank, TCS, Infosys, ITC
            </p>
          </div>
        )}

        {/* Portfolio Summary */}
        {holdings.length > 0 && !dailyBrief && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <BarChart3 className="w-7 h-7 text-blue-600" />
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Your Portfolio</h2>
                  <p className="text-sm text-gray-600">
                    {holdings.length} holdings • ₹{holdings.reduce((sum, h) => sum + (h.quantity * h.avg_buy_price), 0).toLocaleString('en-IN')} total value
                  </p>
                </div>
              </div>
              <button
                onClick={() => generateMockBrief(holdings)}
                disabled={loading}
                className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-6 py-3 rounded-xl font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Your Portfolio...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Daily Brief
                  </>
                )}
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {holdings.map((h, idx) => (
                <div key={idx} className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200 hover:shadow-md transition">
                  <p className="font-bold text-lg text-gray-900">{h.symbol}</p>
                  <p className="text-sm text-gray-600 mt-1">{h.quantity} shares</p>
                  <p className="text-xs text-gray-500">@ ₹{h.avg_buy_price.toFixed(2)}</p>
                  <p className="text-sm font-bold text-blue-600 mt-2">
                    ₹{(h.quantity * h.avg_buy_price).toLocaleString('en-IN')}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Daily Brief */}
        {dailyBrief && (
          <>
            {/* Market Summary Banner */}
            <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-orange-600 text-white rounded-2xl shadow-2xl p-8 mb-8">
              <div className="flex items-center justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle className="w-6 h-6" />
                    <span className="text-sm font-semibold uppercase tracking-wide">Daily Intelligence Brief</span>
                  </div>
                  <h2 className="text-3xl font-bold mb-2">📰 {dailyBrief.headline}</h2>
                  <p className="text-sm opacity-90">
                    {dailyBrief.portfolio_summary.total_holdings} holdings • 
                    ₹{dailyBrief.portfolio_summary.total_value.toLocaleString('en-IN')} total value
                    {dailyBrief.portfolio_summary.day_change !== undefined && (
                      <span className={`ml-3 font-semibold ${dailyBrief.portfolio_summary.day_change >= 0 ? 'text-green-200' : 'text-red-200'}`}>
                        {dailyBrief.portfolio_summary.day_change >= 0 ? '↑' : '↓'} 
                        ₹{Math.abs(dailyBrief.portfolio_summary.day_change).toLocaleString('en-IN')} 
                        ({dailyBrief.portfolio_summary.day_change_pct?.toFixed(2)}%) today
                      </span>
                    )}
                  </p>
                </div>
                {dailyBrief.market_mood && (
                  <div className="bg-white/20 backdrop-blur px-6 py-3 rounded-xl border border-white/30">
                    <p className="text-xs opacity-75 mb-1">Market Mood</p>
                    <p className="font-bold text-lg">{dailyBrief.market_mood}</p>
                  </div>
                )}
              </div>
              
              {/* Top News Ticker */}
              {dailyBrief.top_news && (
                <div className="bg-white/10 backdrop-blur rounded-xl px-5 py-3 border border-white/20">
                  <p className="text-xs font-semibold mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    📡 Live ET Stories Analyzed:
                  </p>
                  <div className="space-y-1.5">
                    {dailyBrief.top_news.map((news, idx) => (
                      <div key={idx} className="flex items-center justify-between text-sm">
                        <span className="flex-1">• {news.title}</span>
                        <span className="text-xs opacity-75 ml-4 whitespace-nowrap">{news.source} • {news.time}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Impact Cards */}
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-2xl font-bold text-gray-900">
                  🎯 {dailyBrief.impact_cards.length} Impact Insights for Your Portfolio
                </h3>
                <button className="text-sm text-blue-600 hover:text-blue-700 font-medium hover:underline flex items-center gap-1">
                  View Analysis History →
                </button>
              </div>
              
              {dailyBrief.impact_cards.map((card, idx) => (
                <div 
                  key={idx} 
                  className={`bg-gradient-to-br ${
                    card.impact_level === 'high' ? 'from-red-50 via-orange-50 to-yellow-50 border-red-400' :
                    card.impact_level === 'moderate' ? 'from-orange-50 via-yellow-50 to-amber-50 border-orange-400' :
                    card.impact_level === 'mild' ? 'from-blue-50 via-indigo-50 to-purple-50 border-blue-400' :
                    'from-green-50 via-emerald-50 to-teal-50 border-green-400'
                  } border-l-4 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.01]`}
                >
                  
                  {/* Card Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h4 className="text-xl font-bold text-gray-900 mb-2">{card.title}</h4>
                      <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600">
                        <span className="bg-white px-3 py-1 rounded-full border border-gray-200">
                          Factor: <strong className="text-gray-900">{card.factor}</strong>
                        </span>
                        <span className="bg-white px-3 py-1 rounded-full border border-gray-200">
                          Sensitivity: <strong className="text-gray-900">{card.sensitivity_score}%</strong>
                        </span>
                        {card.news_count && (
                          <span className="bg-white px-3 py-1 rounded-full border border-gray-200">
                            {card.news_count} ET stories analyzed
                          </span>
                        )}
                        {card.last_updated && (
                          <span className="text-gray-500 text-xs">
                            Updated {card.last_updated}
                          </span>
                        )}
                      </div>
                    </div>
                    <span className={`px-4 py-2 rounded-full text-xs font-bold uppercase whitespace-nowrap ml-4 ${
                      card.impact_level === 'high' ? 'bg-red-200 text-red-900 border-2 border-red-300' :
                      card.impact_level === 'moderate' ? 'bg-orange-200 text-orange-900 border-2 border-orange-300' :
                      card.impact_level === 'mild' ? 'bg-blue-200 text-blue-900 border-2 border-blue-300' :
                      'bg-green-200 text-green-900 border-2 border-green-300'
                    }`}>
                      {card.impact_level} Impact
                    </span>
                  </div>

                  {/* Summary */}
                  <p className="text-gray-700 leading-relaxed mb-5 text-base bg-white/50 backdrop-blur p-4 rounded-xl">
                    {card.summary}
                  </p>

                  {/* Affected Holdings */}
                  <div className="flex items-center gap-3 mb-5">
                    <span className="text-sm font-semibold text-gray-700">📊 Affects Your Holdings:</span>
                    <div className="flex flex-wrap gap-2">
                      {card.affected_holdings.map((symbol, i) => (
                        <span 
                          key={i} 
                          className="bg-white px-4 py-1.5 rounded-full text-sm font-bold border-2 border-gray-300 text-gray-900 shadow-sm"
                        >
                          {symbol}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Action Options */}
                  <div className="space-y-3">
                    <p className="text-sm font-bold text-gray-800 flex items-center gap-2">
                      <span className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs">💡</span>
                      Recommended Actions for SIP Investors:
                    </p>
                    {card.action_options.map((option, i) => (
                      <div 
                        key={i} 
                        className="bg-white/90 backdrop-blur p-4 rounded-xl border-2 border-gray-200 hover:border-blue-400 transition-all hover:shadow-md cursor-pointer"
                      >
                        <p className="font-bold text-gray-900 mb-1.5 text-base">{option.action}</p>
                        <p className="text-sm text-gray-600 leading-relaxed">{option.reason}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Analysis Footer */}
            <div className="mt-8 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-6 border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Powered by</p>
                  <p className="font-bold text-gray-900">Neo4j Knowledge Graph • OpenAI GPT-4o • LangChain</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition">
                  📧 Email This Brief
                </button>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16 py-6">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              <p className="font-semibold text-gray-900">ET MarketLens</p>
              <p>Built for ET GenAI Hackathon 2026 • Team GenX</p>
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-600">
              <a href="https://github.com/YOUR-USERNAME/et-marketlens" className="hover:text-blue-600">GitHub</a>
              <a href="https://et-marketlens.onrender.com/docs" className="hover:text-blue-600">API Docs</a>
              <span>Powered by Neo4j + LangChain + OpenAI</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}