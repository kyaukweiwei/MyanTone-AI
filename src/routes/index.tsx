import { createFileRoute, Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { PIPELINE_STAGES } from "@/lib/myantone-engine";
import {
  ArrowRight,
  Clock,
  Languages,
  Mail,
  Sparkles,
  Target,
  Users,
  Wand2,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MyanTone AI — Say it in Myanmar. Send it naturally in English." },
      {
        name: "description",
        content:
          "MyanTone AI is a Myanmar-first AI communication assistant: turn Myanmar thoughts into natural English messages and complete, professional emails.",
      },
      { property: "og:title", content: "MyanTone AI — Myanmar-first AI communication assistant" },
      {
        property: "og:description",
        content:
          "Turn your Myanmar thoughts into natural English messages and professional emails — with the right words, tone and context.",
      },
    ],
  }),
  component: Landing,
});

function Landing() {
  return (
    <div>
      {/* Hero */}
      <section className="mesh-bg relative overflow-hidden border-b border-border">
        <div className="grid-motif absolute inset-0 opacity-40" aria-hidden />
        <div className="relative mx-auto grid max-w-7xl gap-12 px-4 py-16 sm:px-6 lg:grid-cols-[1.05fr_.95fr] lg:py-24">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full border border-teal/30 bg-card px-3.5 py-1.5 text-xs font-semibold text-teal">
              <Sparkles className="size-3.5" aria-hidden /> Powered by AI · Myanmar-first
            </span>
            <h1 className="mt-6 text-4xl leading-[1.1] sm:text-5xl lg:text-6xl">
              Say it in Myanmar.
              <br />
              <span className="text-teal">Send it naturally in English.</span>
            </h1>
            <p className="mt-5 max-w-xl text-lg text-muted-foreground">
              Turn your Myanmar thoughts into natural English messages and professional emails — with
              the right words, tone, and context.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button asChild size="lg" variant="teal">
                <Link to="/translate">
                  Try MyanTone Free <ArrowRight />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link to="/email">Create an Email</Link>
              </Button>
            </div>
            <p className="mt-6 text-sm text-muted-foreground">
              Understand what I mean · Translate naturally · Choose the right tone · Send with
              confidence
            </p>
          </div>

          {/* Live example card */}
          <div className="card-soft overflow-hidden shadow-[var(--shadow-lift)]">
            <div className="border-b border-border px-5 py-4">
              <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                You write
              </p>
              <p className="font-my mt-1.5 text-[15px] text-primary">
                မနက်ဖြန် ဆရာ့ကို assignment နောက်ကျတင်မယ်လို့ ပြောချင်တယ်
              </p>
            </div>
            <div className="grid gap-3 border-b border-border bg-secondary/50 px-5 py-4 sm:grid-cols-3">
              {[
                { icon: Target, label: "Intent", value: "Deadline extension" },
                { icon: Users, label: "Audience", value: "Lecturer" },
                { icon: Wand2, label: "Tone", value: "Professional" },
              ].map(({ icon: Icon, label, value }) => (
                <div key={label}>
                  <p className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    <Icon className="size-3 text-teal" aria-hidden /> {label}
                  </p>
                  <p className="mt-0.5 text-sm font-medium text-primary">{value}</p>
                </div>
              ))}
            </div>
            <div className="px-5 py-5">
              <p className="text-[11px] font-bold uppercase tracking-widest text-teal">
                MyanTone writes
              </p>
              <p className="mt-2 whitespace-pre-line text-[15px] leading-relaxed text-primary">
                {`Dear Sir,

I would like to kindly request an extension for the assignment submission deadline. I would be grateful if I could submit the assignment tomorrow.

Thank you for your understanding.

Best regards,
[Your Name]`}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Capabilities */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
        <h2 className="text-3xl">Two ways to be understood</h2>
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          {[
            {
              icon: Languages,
              title: "Translate",
              copy: "Myanmar → natural English in five tones. Meaning first, never word-for-word.",
              to: "/translate" as const,
              cta: "Open Translate",
            },
            {
              icon: Mail,
              title: "Email Studio",
              copy: "A Myanmar intention becomes a complete English email — subject, structure, tone and quality check.",
              to: "/email" as const,
              cta: "Open Email Studio",
            },
          ].map(({ icon: Icon, title, copy, to, cta }) => (
            <article key={title} className="card-soft p-7">
              <span className="grid size-11 place-items-center rounded-2xl bg-teal-soft text-accent-foreground">
                <Icon className="size-5" aria-hidden />
              </span>
              <h3 className="mt-4 text-xl">{title}</h3>
              <p className="mt-2 text-muted-foreground">{copy}</p>
              <Button asChild variant="ghost" className="mt-4 px-0 hover:bg-transparent">
                <Link to={to}>
                  {cta} <ArrowRight />
                </Link>
              </Button>
            </article>
          ))}
        </div>
      </section>

      {/* Dashboard preview */}
      <section className="border-y border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <h2 className="text-3xl">Good morning 👋</h2>
              <p className="mt-2 text-muted-foreground">Pick up where you left off.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button asChild variant="teal" size="sm">
                <Link to="/translate">Translate</Link>
              </Button>
              <Button asChild variant="outline" size="sm">
                <Link to="/email">Create Email</Link>
              </Button>
              <Button asChild variant="outline" size="sm">
                <Link to="/email">Improve Email</Link>
              </Button>
            </div>
          </div>

          <div className="mt-8 grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
            <div className="grid content-start gap-4 sm:grid-cols-3">
              {[
                { label: "Translations this month", value: "48" },
                { label: "Emails created", value: "23" },
                { label: "Saved templates", value: "9" },
              ].map((s) => (
                <div key={s.label} className="card-soft p-5">
                  <p className="text-3xl font-bold text-primary">{s.value}</p>
                  <p className="mt-1 text-sm text-muted-foreground">{s.label}</p>
                </div>
              ))}
            </div>
            <div className="card-soft p-5">
              <h3 className="text-sm font-semibold">Recent activity</h3>
              <ul className="mt-3 space-y-3 text-sm">
                {["Meeting reschedule email", "Assignment extension", "Leave request"].map((a) => (
                  <li key={a} className="flex items-center gap-2.5 text-muted-foreground">
                    <Clock className="size-4 text-teal" aria-hidden />
                    {a}
                  </li>
                ))}
              </ul>
              <Button asChild size="sm" variant="ghost" className="mt-3 px-0 hover:bg-transparent">
                <Link to="/history">
                  View history <ArrowRight />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Pipeline */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
        <h2 className="text-3xl">Not a dictionary. A language pipeline.</h2>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Every message runs through normalization, mixed-language detection, intent understanding,
          neural translation, tone control and a final quality evaluation.
        </p>
        <ol className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {PIPELINE_STAGES.map((s, i) => (
            <li key={s} className="card-soft flex items-center gap-3 px-4 py-3.5 text-sm">
              <span className="grid size-7 shrink-0 place-items-center rounded-full bg-primary text-[11px] font-bold text-primary-foreground">
                {i + 1}
              </span>
              <span className="font-medium text-primary">{s}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Final CTA */}
      <section className="bg-primary">
        <div className="mx-auto max-w-3xl px-4 py-20 text-center sm:px-6">
          <h2 className="text-3xl text-primary-foreground sm:text-4xl">
            Your thoughts are already clear.
            <br />
            Now say them naturally.
          </h2>
          <p className="mt-4 text-lg text-primary-foreground/70">
            Write it in Myanmar. Send it with confidence.
          </p>
          <Button asChild size="lg" variant="amber" className="mt-8">
            <Link to="/translate">Try MyanTone Free</Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
