'use client';

import React, { useState } from 'react';
import { BarChart3, Upload, Sparkles, TrendingUp } from 'lucide-react';

interface Holding {
  symbol: string;
  quantity: number;
  avg_buy_price: number;
}

export default function Dashboard() {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [showUpload, setShowUpload] = useState(true);

  const loadSamplePortfolio = () => {
    const sample: Holding[] = [
      { symbol: 'RELIANCE', quantity: 10, avg_buy_price: 2450.50 },
      { symbol: 'HDFCBANK', quantity: 20, avg_buy_price: 1580.00 },
      { symbol: 'TCS', quantity: 5, avg_buy_price: 3600.00 },
    ];
    setHoldings(sample);
    setShowUpload(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Sparkles className="w-8 h-8 text-orange-500" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">ET MarketLens</h1>
                <p className="text-sm text-gray-600">Portfolio-Aware News Intelligence</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Demo User</p>
              <p className="text-xs text-gray-500">SIP Investor</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {showUpload && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-6 text-center">
            <Upload className="w-16 h-16 text-blue-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Upload Your Portfolio</h2>
            <p className="text-gray-600 mb-6">Get personalized impact analysis for your holdings</p>
            <button
              onClick={loadSamplePortfolio}
              className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition"
            >
              Load Sample Portfolio
            </button>
          </div>
        )}

        {holdings.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <BarChart3 className="w-6 h-6 text-blue-600" />
                <h2 className="text-xl font-bold">Your Portfolio</h2>
              </div>
              <button
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition"
              >
                Generate Daily Brief
              </button>
            </div>

            <div className="grid grid-cols-3 gap-4">
              {holdings.map((h, idx) => (
                <div key={idx} className="bg-gray-50 p-4 rounded-lg">
                  <p className="font-bold text-lg">{h.symbol}</p>
                  <p className="text-sm text-gray-600">{h.quantity} shares @ ₹{h.avg_buy_price.toFixed(2)}</p>
                  <p className="text-sm font-semibold text-blue-600">
                    ₹{(h.quantity * h.avg_buy_price).toLocaleString('en-IN')}
                  </p>
                </div>
              ))}
            </div>

            <div className="mt-8 space-y-4">
              <h3 className="text-xl font-bold text-gray-800">Impact Cards (Demo)</h3>
              
              <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-gray-900">Crude Oil Spike Affects Energy Stocks</h4>
                    <p className="text-sm text-gray-600">Factor: CrudeOilPrice</p>
                  </div>
                  <span className="px-3 py-1 bg-red-200 text-red-800 rounded-full text-xs font-semibold">HIGH</span>
                </div>
                <p className="text-gray-700 mb-3">
                  Crude oil prices at $85/barrel impact your Reliance holdings. Higher oil prices can squeeze refining margins but boost upstream profits. For long-term SIP investors, this is normal volatility.
                </p>
                <div className="flex gap-4 text-sm">
                  <div><strong>Sensitivity:</strong> 95.0%</div>
                  <div><strong>Affected:</strong> RELIANCE</div>
                </div>
              </div>

              <div className="bg-orange-50 border-l-4 border-orange-500 rounded-lg p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-gray-900">RBI Rate Hike Impacts Bank Stocks</h4>
                    <p className="text-sm text-gray-600">Factor: RepoRate</p>
                  </div>
                  <span className="px-3 py-1 bg-orange-200 text-orange-800 rounded-full text-xs font-semibold">HIGH</span>
                </div>
                <p className="text-gray-700 mb-3">
                  Repo rate at 6.5% affects banking stocks like HDFC Bank. Higher rates improve Net Interest Margins (NIM) but may slow loan growth. Banks typically adjust within 2-3 quarters.
                </p>
                <div className="flex gap-4 text-sm">
                  <div><strong>Sensitivity:</strong> 90.0%</div>
                  <div><strong>Affected:</strong> HDFCBANK</div>
                </div>
              </div>

              <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-gray-900">Rupee Movement Benefits IT Exporters</h4>
                    <p className="text-sm text-gray-600">Factor: USDINRRate</p>
                  </div>
                  <span className="px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-xs font-semibold">HIGH</span>
                </div>
                <p className="text-gray-700 mb-3">
                  USD/INR at 83 improves revenue realization for IT companies like TCS. A weaker rupee means higher rupee earnings from dollar revenues. Good news for IT holdings.
                </p>
                <div className="flex gap-4 text-sm">
                  <div><strong>Sensitivity:</strong> 80.0%</div>
                  <div><strong>Affected:</strong> TCS</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-12 py-4">
        <div className="max-w-7xl mx-auto px-6 text-center text-sm text-gray-600">
          Built for ET Hackathon 2026 • Powered by Neo4j + LangChain
        </div>
      </footer>
    </div>
  );
}