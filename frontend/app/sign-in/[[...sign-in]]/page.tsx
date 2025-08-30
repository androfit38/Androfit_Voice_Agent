import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative">
        <SignIn
          routing="path"
          path="/sign-in"
          redirectUrl="/"
          afterSignInUrl="/"
          afterSignUpUrl="/"
        />
      </div>
    </div>
  );
}
