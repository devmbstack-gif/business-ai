import Link from "next/link";
import Image from "next/image";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-brand-background px-4">
      <Image
        src="/logo.jpeg"
        alt="Business AI"
        width={320}
        height={120}
        className="rounded-xl"
        priority
      />
      <h1 className="mt-8 text-3xl font-bold text-brand-text">
        Smart Proposals. <span className="gradient-text">Better Wins.</span>
      </h1>
      <p className="mt-3 max-w-md text-center text-brand-text-muted">
        AI-powered job analysis and proposal generation for freelancers and business developers.
      </p>
      <div className="mt-8 flex gap-4">
        <Link
          href="/admin/login"
          className="gradient-primary rounded-lg px-6 py-3 text-sm font-medium text-white shadow-sm transition-opacity hover:opacity-90"
        >
          Admin Panel
        </Link>
      </div>
    </div>
  );
}
