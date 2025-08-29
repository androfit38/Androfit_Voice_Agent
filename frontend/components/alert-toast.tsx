'use client';

import { ReactNode } from 'react';
import { toast as sonnerToast } from 'sonner';
import { WarningIcon } from '@phosphor-icons/react/dist/ssr';
import { Alert, AlertDescription, AlertTitle } from './ui/alert';

interface ToastProps {
  id: string | number;
  title: ReactNode;
  description: ReactNode;
}

export function toastAlert(toast: Omit<ToastProps, 'id'>) {
  return sonnerToast.custom(
    (id) => <AlertToast id={id} title={toast.title} description={toast.description} />,
    { duration: 10_000 }
  );
}

function AlertToast(props: ToastProps) {
  const { title, description, id } = props;

  return (
    <Alert 
      onClick={() => sonnerToast.dismiss(id)} 
      className="bg-background border-2 border-orange-200 dark:border-orange-800 shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer"
    >
      <WarningIcon weight="bold" className="text-orange-500" />
      <AlertTitle className="text-foreground font-semibold">{title}</AlertTitle>
      {description && <AlertDescription className="text-muted-foreground">{description}</AlertDescription>}
    </Alert>
  );
}
