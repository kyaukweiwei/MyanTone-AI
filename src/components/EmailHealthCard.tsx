import type { EmailHealth } from "@/lib/myantone-engine";
import { AlertTriangle, Check, ShieldCheck } from "lucide-react";

export function EmailHealthCard({ health }: { health: EmailHealth }) {
  const r = 34;
  const c = 2 * Math.PI * r;
  return (
    <section className="card-soft p-5" aria-label="Email health">
      <header className="mb-4 flex items-center gap-2">
        <ShieldCheck className="size-4 text-teal" aria-hidden />
        <h3 className="text-sm font-semibold">Email Health · Before You Send</h3>
      </header>

      <div className="flex flex-col gap-5 sm:flex-row sm:items-center">
        <div className="relative grid size-24 shrink-0 place-items-center">
          <svg viewBox="0 0 80 80" className="size-24 -rotate-90">
            <circle cx="40" cy="40" r={r} fill="none" stroke="var(--secondary)" strokeWidth="8" />
            <circle
              cx="40"
              cy="40"
              r={r}
              fill="none"
              stroke="var(--teal)"
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={c}
              strokeDashoffset={c - (c * health.score) / 100}
            />
          </svg>
          <div className="absolute text-center">
            <p className="text-xl font-bold text-primary">{health.score}</p>
            <p className="text-[10px] text-muted-foreground">/ 100</p>
          </div>
        </div>

        <ul className="flex-1 space-y-2">
          {health.checks.map((c2, i) => (
            <li key={`${c2.label}-${i}`} className="flex items-start gap-2.5 text-sm">
              {c2.status === "good" ? (
                <Check className="mt-0.5 size-4 shrink-0 text-success" aria-hidden />
              ) : (
                <AlertTriangle className="mt-0.5 size-4 shrink-0 text-amber" aria-hidden />
              )}
              <span>
                <span className="font-medium text-primary">{c2.label}</span>{" "}
                <span className="text-muted-foreground">— {c2.note}</span>
              </span>
            </li>
          ))}
        </ul>
      </div>

      {health.suggestions.length > 0 && (
        <ul className="mt-4 space-y-2 rounded-xl bg-amber-soft/70 p-3.5 text-sm text-primary">
          {health.suggestions.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
