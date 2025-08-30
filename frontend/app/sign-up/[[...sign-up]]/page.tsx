import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative">
        <SignUp
          routing="path"
          path="/sign-up"
          redirectUrl="/"
          afterSignUpUrl="/"
          afterSignInUrl="/"
        />
      </div>
    </div>
  );
}
