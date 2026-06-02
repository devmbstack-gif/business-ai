import { Navbar } from "@/components/home/navbar";
import { Hero } from "@/components/home/hero";
import { Features } from "@/components/home/features";
import { CtaSection, Footer } from "@/components/home/footer";

export default function HomePage() {
  return (
    <div className="page-bg min-h-screen">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <CtaSection />
      </main>
      <Footer />
    </div>
  );
}
