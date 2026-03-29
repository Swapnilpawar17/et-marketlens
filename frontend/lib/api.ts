import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Holding {
  symbol: string;
  quantity: number;
  avg_buy_price: number;
  goal_id?: string;
}

export interface ImpactCard {
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
}

export interface DailyBrief {
  date: string;
  portfolio_summary: {
    total_holdings: number;
    total_value: number;
    symbols: string[];
  };
  impact_cards: ImpactCard[];
  headline: string;
}

export const api = {
  async analyzeImpact(holdings: Holding[], persona: string = 'sip_investor') {
    const response = await axios.post(`${API_BASE_URL}/api/impact/analyze`, {
      user_id: 'demo_user',
      holdings,
      persona,
    });
    return response.data;
  },

  async getDailyBrief(holdings: Holding[], persona: string = 'sip_investor'): Promise<DailyBrief> {
    const response = await axios.post(`${API_BASE_URL}/api/impact/daily-brief`, {
      user_id: 'demo_user',
      holdings,
      persona,
    });
    return response.data;
  },

  async uploadPortfolio(holdings: Holding[], goals: any[], persona: string) {
    const response = await axios.post(`${API_BASE_URL}/api/portfolio/upload`, {
      user_id: 'demo_user',
      holdings,
      goals,
      persona,
    });
    return response.data;
  },
};