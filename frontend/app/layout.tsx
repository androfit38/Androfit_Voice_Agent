import { Public_Sans } from 'next/font/google';
import localFont from 'next/font/local';
import { headers } from 'next/headers';
import { ClerkProvider } from '@clerk/nextjs';
import { dark } from '@clerk/themes';
import { ApplyThemeScript, ThemeToggle } from '@/components/theme-toggle';
import { getAppConfig } from '@/lib/utils';
import './globals.css';

const publicSans = Public_Sans({
  variable: '--font-public-sans',
  subsets: ['latin'],
});

const commitMono = localFont({
  src: [
    {
      path: './fonts/CommitMono-400-Regular.otf',
      weight: '400',
      style: 'normal',
    },
    {
      path: './fonts/CommitMono-700-Regular.otf',
      weight: '700',
      style: 'normal',
    },
    {
      path: './fonts/CommitMono-400-Italic.otf',
      weight: '400',
      style: 'italic',
    },
    {
      path: './fonts/CommitMono-700-Italic.otf',
      weight: '700',
      style: 'italic',
    },
  ],
  variable: '--font-commit-mono',
});

interface RootLayoutProps {
  children: React.ReactNode;
}

export default async function RootLayout({ children }: RootLayoutProps) {
  const hdrs = await headers();
  const { accent, accentDark, pageTitle, pageDescription } = await getAppConfig(hdrs);

  const styles = [
    accent ? `:root { --primary: ${accent}; }` : '',
    accentDark ? `.dark { --primary: ${accentDark}; }` : '',
  ]
    .filter(Boolean)
    .join('\n');

  return (
    <ClerkProvider
      appearance={{
        baseTheme: dark,
        variables: {
          borderRadius: '8px',
        },
        elements: {
          userButtonAvatarBox: 'w-8 h-8 md:w-9 md:h-9',
        },
      }}
    >
      <html lang="en" suppressHydrationWarning className="scroll-smooth dark">
        <head>
          {styles && <style>{styles}</style>}
          <title>{pageTitle}</title>
          <meta name="description" content={pageDescription} />
          <link rel="icon" href="/logo.svg" type="image/svg+xml" />
          <link rel="apple-touch-icon" href="/logo.svg" />
          <meta name="theme-color" content={accent} />
          <ApplyThemeScript />
        </head>
        <body
          className={`${publicSans.variable} ${commitMono.variable} overflow-x-hidden antialiased dark bg-black text-white`}
        >
          {children}
          <div className="group fixed bottom-0 left-1/2 z-50 mb-2 -translate-x-1/2">
            <ThemeToggle className="translate-y-20 transition-transform delay-150 duration-300 group-hover:translate-y-0" />
          </div>
        </body>
      </html>
    </ClerkProvider>
  );
}
