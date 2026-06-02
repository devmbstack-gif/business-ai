import Link from "next/link";
import Image from "next/image";

export function Hero() {
  return (
    <section className="relative mx-auto max-w-6xl px-6 pb-20 pt-16 text-center lg:pt-24">
      <div className="mx-auto mb-8 inline-flex items-center gap-2 rounded-full border border-brand-primary/20 bg-brand-primary/5 px-4 py-1.5 text-sm font-medium text-brand-primary-dark">
        <span className="h-2 w-2 rounded-full bg-brand-primary" />
        AI Proposal Writer & Job Analyzer
      </div>

      <div className="mx-auto flex justify-center">
        <Image
          src="/logo.jpeg"
          alt="Business AI"
          width={300}
          height={120}
          className="rounded-2xl shadow-lg shadow-brand-primary/15"
          priority
        />
      </div>

      <h1 className="mx-auto mt-10 max-w-3xl text-4xl font-bold leading-tight tracking-tight text-brand-text sm:text-5xl lg:text-6xl">
        Smart Proposals.{" "}
        <span className="gradient-text">Better Wins.</span>
      </h1>

      <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-brand-text-muted">
        Analyze job postings, calculate success scores, and generate
        high-converting proposals — built for freelancers and business developers.
      </p>

      <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
        <Link
          href="#features"
          className="gradient-primary rounded-xl px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-brand-primary/25 transition-all hover:brightness-110 active:scale-[0.98]"
        >
          Explore Features
        </Link>
        <Link
          href="/admin/login"
          className="rounded-xl border border-brand-border bg-brand-surface px-8 py-3.5 text-sm font-semibold text-brand-text shadow-sm transition-all hover:border-brand-primary/40 hover:shadow-md"
        >
          Admin Panel
        </Link>
      </div>

      <div className="mx-auto mt-16 grid max-w-3xl grid-cols-3 gap-6 border-t border-brand-border pt-10">
        <div>
          <p className="text-3xl font-bold gradient-text">AI</p>
          <p className="mt-1 text-sm text-brand-text-muted">Powered Analysis</p>
        </div>
        <div>
          <p className="text-3xl font-bold gradient-text">100</p>
          <p className="mt-1 text-sm text-brand-text-muted">Success Score</p>
        </div>
        <div>
          <p className="text-3xl font-bold gradient-text">PDF</p>
          <p className="mt-1 text-sm text-brand-text-muted">Proposal Export</p>
        </div>
      </div>
    </section>
  );
}
