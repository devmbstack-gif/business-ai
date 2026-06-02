import Link from "next/link";
import Image from "next/image";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-brand-border/60 bg-brand-surface/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/logo.jpeg"
            alt="Business AI"
            width={44}
            height={44}
            className="rounded-lg"
          />
          <span className="hidden text-sm font-bold tracking-wide text-brand-text sm:block">
            BUSINESS AI
          </span>
        </Link>

        <nav className="flex items-center gap-3">
          <Link
            href="/admin/login"
            className="rounded-xl border border-brand-border bg-brand-surface px-4 py-2 text-sm font-medium text-brand-text transition-colors hover:border-brand-primary/40 hover:bg-brand-primary/5"
          >
            Admin
          </Link>
          <Link
            href="#features"
            className="gradient-primary hidden rounded-xl px-4 py-2 text-sm font-semibold text-white shadow-md shadow-brand-primary/25 sm:inline-block"
          >
            Get Started
          </Link>
        </nav>
      </div>
    </header>
  );
}
