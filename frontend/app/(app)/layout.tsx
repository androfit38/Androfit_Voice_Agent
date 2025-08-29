import { headers } from 'next/headers';
import { getAppConfig } from '@/lib/utils';
import { UserProfile } from '@/components/user-profile';

interface AppLayoutProps {
  children: React.ReactNode;
}

export default async function AppLayout({ children }: AppLayoutProps) {
  const hdrs = await headers();
  const { companyName, logo, logoDark } = await getAppConfig(hdrs);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center p-4 md:p-6">
        <div className="flex items-center gap-3">
          <div className="scale-100 transition-transform duration-300 hover:scale-110">
            <img src={logo} alt={`${companyName} Logo`} className="block size-5 md:size-6 dark:hidden" />
            <img
              src={logoDark ?? logo}
              alt={`${companyName} Logo`}
              className="hidden size-5 md:size-6 dark:block"
            />
          </div>
          <span className="text-foreground font-mono text-xs md:text-sm font-bold tracking-wider uppercase">
            AndrofitAI
          </span>
        </div>
        <div className="flex items-center">
          <UserProfile />
        </div>
      </header>
      {children}
    </>
  );
}
