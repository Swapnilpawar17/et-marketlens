import React from 'react';
import { AlertCircle, TrendingUp, TrendingDown, Activity } from 'lucide-react';

interface ImpactCardProps {
  card: {
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
  };
}

const impactIcons = {
  high: <AlertCircle className="w-6 h-6 text-red-500" />,
  moderate: <TrendingDown className="w-6 h-6 text-orange-500" />,
  mild: <Activity className="w-6 h-6 text-blue-500" />,
  low: <TrendingUp className="w-6 h-6 text-green-500" />,
};

const impactColors = {
  high: 'bg-red-50 border-red-200',
  moderate: 'bg-orange-50 border-orange-200',
  mild: 'bg-blue-50 border-blue-200',
  low: 'bg-green-50 border-green-200',
};

export default function ImpactCard({ card }: ImpactCardProps) {
  return (
    <div className={`rounded-lg border-2 p-6 card-shadow impact-${card.impact_level} ${impactColors[card.impact_level]}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {impactIcons[card.impact_level]}
          <div>
            <h3 className="text-lg font-bold text-gray-900">{card.title}</h3>
            <p className="text-sm text-gray-600">Factor: {card.factor}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase ${
          card.impact_level === 'high' ? 'bg-red-200 text-red-800' :
          card.impact_level === 'moderate' ? 'bg-orange-200 text-orange-800' :
          card.impact_level === 'mild' ? 'bg-blue-200 text-blue-800' :
          'bg-green-200 text-green-800'
        }`}>
          {card.impact_level}
        </span>
      </div>

      <p className="text-gray-700 mb-4 leading-relaxed">{card.summary}</p>

      <div className="flex items-center gap-4 mb-4 text-sm">
        <div className="flex items-center gap-2">
          <span className="font-semibold">Sensitivity:</span>
          <span className="bg-white px-2 py-1 rounded">{card.sensitivity_score}%</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold">Affected:</span>
          <span className="bg-white px-2 py-1 rounded">{card.affected_holdings.join(', ')}</span>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-gray-700">Action Options:</p>
        {card.action_options.map((option, idx) => (
          <div key={idx} className="bg-white p-3 rounded border border-gray-200">
            <p className="font-medium text-gray-900">✓ {option.action}</p>
            <p className="text-sm text-gray-600">{option.reason}</p>
          </div>
        ))}
      </div>
    </div>
  );
}