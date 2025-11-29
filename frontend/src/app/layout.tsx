import type { Metadata } from 'next';
import './globals.css';
import { cn } from '@/lib/utils';
import { Toaster } from '@/components/ui/toaster';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import LoaderSplash from '@/components/LoaderSplash';   // ✅ NEW

export const metadata: Metadata = {
  title: 'Alertrix - Disaster Management Dashboard',
  description: 'An AI-integrated disaster management system.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
      </head>

      <body className={cn('min-h-screen bg-background font-body antialiased')}>
        
        {/* 🔥 NEW: Splash Animation Component */}
        <LoaderSplash />

        <div className="relative flex min-h-screen flex-col">
          <Header />
          
          <main className="flex-1">
            {children}
          </main>

          <Footer />
        </div>

        <Toaster />
      </body>
    </html>
  );
}
