import Link from "next/link";
import Image from "next/image";

export function CtaSection() {
  return (
    <section className="mx-auto max-w-6xl px-6 pb-20">
      <div className="overflow-hidden rounded-3xl gradient-primary p-10 text-center sm:p-14">
        <h2 className="text-3xl font-bold text-white sm:text-4xl">
          Ready to win your next project?
        </h2>
        <p className="mx-auto mt-4 max-w-lg text-white/80">
          Start analyzing jobs and generating winning proposals with Business AI today.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="#features"
            className="rounded-xl bg-white px-8 py-3.5 text-sm font-semibold text-brand-primary-dark transition-all hover:bg-white/90 active:scale-[0.98]"
          >
            Learn More
          </Link>
          <Link
            href="/admin/login"
            className="rounded-xl border border-white/30 px-8 py-3.5 text-sm font-semibold text-white transition-all hover:bg-white/10"
          >
            Admin Login
          </Link>
        </div>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-brand-border bg-brand-surface">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 sm:flex-row">
        <div className="flex items-center gap-3">
          <Image
            src="/logo.jpeg"
            alt="Business AI"
            width={32}
            height={32}
            className="rounded-md"
          />
          <p className="text-sm text-brand-text-muted">
            Smart Proposals. Better Wins.
          </p>
        </div>
        <p className="text-xs text-brand-text-muted">
          © {new Date().getFullYear()} Business AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
