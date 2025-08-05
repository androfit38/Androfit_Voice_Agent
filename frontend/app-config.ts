import type { AppConfig } from './lib/types';

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'AndrofitAI',
  pageTitle: 'AndrofitAI - Your Personal Fitness Coach',
  pageDescription: 'An energetic, voice-interactive AI personal gym coach for personalized workout sessions',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/logo.svg',
  accent: '#3b82f6',
  logoDark: '/logo-dark.svg',
  accentDark: '#60a5fa',
  startButtonText: 'Start Workout',
};
