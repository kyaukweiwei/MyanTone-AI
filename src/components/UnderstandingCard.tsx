import type { Understanding } from "@/lib/myantone-engine";
import { Paperclip, Target, Users, Wand2, AlertTriangle } from "lucide-react";

function Row({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-start gap-3">
      <span className="mt-0.5 grid size-7 shrink-0 place-items-center rounded-lg bg-teal-soft text-accent-foreground">
        {icon}
      </span>
      <div>
        <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          {label}
        </p>
        <p className="text-sm font-medium text-primary">{value}</p>
      </div>
    </div>
  );
}

export function UnderstandingCard({ u }: { u: Understanding }) {
  return (
    <section className="card-soft p-5" aria-label="AI understanding">
      <header className="mb-4 flex items-center gap-2">
        <Wand2 className="size-4 text-teal" aria-hidden />
        <h3 className="text-sm font-semibold">AI Understanding</h3>
        <span className="ml-auto rounded-full bg-secondary px-2.5 py-1 text-[11px] font-medium text-muted-foreground">
          {u.languageMix}
        </span>
      </header>
      <div className="grid gap-4 sm:grid-cols-2">
        <Row icon={<Target className="size-4" />} label="Intent" value={u.intent} />
        <Row icon={<Users className="size-4" />} label="Audience" value={u.audience} />
        <Row icon={<Wand2 className="size-4" />} label="Situation" value={u.situation} />
        <Row
          icon={<Wand2 className="size-4" />}
          label="Recommended tone"
          value={u.tone.charAt(0).toUpperCase() + u.tone.slice(1)}
        />
      </div>
      {u.attachment && (
        <p className="mt-4 flex items-center gap-2 rounded-xl bg-amber-soft px-3 py-2 text-sm text-primary">
          <Paperclip className="size-4" aria-hidden />
          Attachment mentioned: <strong>{u.attachment}</strong>
          <span className="text-xs text-muted-foreground">(not uploaded yet)</span>
        </p>
      )}
      {u.missing.length > 0 && (
        <ul className="mt-3 space-y-1.5">
          {u.missing.map((m) => (
            <li key={m} className="flex items-start gap-2 text-sm text-muted-foreground">
              <AlertTriangle className="mt-0.5 size-4 shrink-0 text-amber" aria-hidden />
              {m}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
