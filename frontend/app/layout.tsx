import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ET MarketLens - Portfolio Intelligence',
  description: 'AI-powered portfolio impact analysis for Indian investors',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}