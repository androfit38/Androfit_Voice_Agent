'use client';

import { UserButton } from '@clerk/nextjs';

export function UserProfile() {
  return (
    <div className="flex items-center">
      <UserButton
        showName={false}
      />
    </div>
  );
}
