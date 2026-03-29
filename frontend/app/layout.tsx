import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ET MarketLens - Portfolio Intelligence',
  description: 'AI-powered portfolio impact analysis for Indian investors. Know exactly how today\'s news affects YOUR holdings.',
  keywords: 'portfolio analysis, stock market, Indian stocks, AI investing, ET Markets',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✨</text></svg>" />
      </head>
      <body>{children}</body>
    </html>
  );
}