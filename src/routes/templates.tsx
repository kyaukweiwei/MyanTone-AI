import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { TEMPLATES, TEMPLATE_CATEGORIES } from "@/lib/templates";
import { ArrowUpRight } from "lucide-react";

export const Route = createFileRoute("/templates")({
  head: () => ({
    meta: [
      { title: "Email Templates for Work, University & Business — MyanTone AI" },
      {
        name: "description",
        content:
          "Ready-made English email templates for sick leave, deadline extensions, job applications, client follow-ups and more — written from Myanmar input.",
      },
      { property: "og:title", content: "Email Templates — MyanTone AI" },
      {
        property: "og:description",
        content: "Pick a situation, open Email Studio pre-filled, and send with confidence.",
      },
    ],
  }),
  component: TemplatesPage,
});

function TemplatesPage() {
  const [cat, setCat] = useState<string>("All");
  const list = cat === "All" ? TEMPLATES : TEMPLATES.filter((t) => t.category === cat);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <header className="mb-8">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">Templates</p>
        <h1 className="mt-2 text-3xl sm:text-4xl">Start from a real situation</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Every template opens Email Studio pre-filled with a Myanmar starting sentence, the right
          audience, purpose and tone.
        </p>
      </header>

      <div className="mb-6 flex flex-wrap gap-2">
        {["All", ...TEMPLATE_CATEGORIES].map((c) => (
          <button
            key={c}
            onClick={() => setCat(c)}
            aria-pressed={cat === c}
            className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
              cat === c
                ? "border-primary bg-primary text-primary-foreground"
                : "border-border bg-card text-muted-foreground hover:text-primary"
            }`}
          >
            {c}
          </button>
        ))}
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((t) => (
          <article
            key={t.id}
            className="card-soft flex flex-col p-5 transition-shadow hover:shadow-[var(--shadow-lift)]"
          >
            <span className="text-[11px] font-bold uppercase tracking-widest text-teal">
              {t.category}
            </span>
            <h2 className="mt-1.5 text-base font-semibold text-primary">{t.title}</h2>
            <p className="mt-1 text-sm text-muted-foreground">{t.blurb}</p>
            <p className="font-my mt-3 line-clamp-2 rounded-xl bg-secondary/70 px-3 py-2 text-[13px] text-muted-foreground">
              {t.seed}
            </p>
            <Button asChild size="sm" variant="soft" className="mt-4 self-start">
              <Link to="/email" search={{ template: t.id }}>
                Use Template <ArrowUpRight />
              </Link>
            </Button>
          </article>
        ))}
      </div>
    </div>
  );
}
