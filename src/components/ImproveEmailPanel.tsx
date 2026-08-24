import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  improveTextResult,
  type AIFallbackReason,
  type ImproveAction,
} from "@/lib/myantone-engine";
import { OfflineModeNotice } from "@/components/OfflineModeNotice";
import { ArrowRight, Copy, Sparkles } from "lucide-react";

const ACTIONS: { id: ImproveAction; label: string }[] = [
  { id: "professional", label: "Make Professional" },
  { id: "polite", label: "Make Polite" },
  { id: "friendly", label: "Make Friendly" },
  { id: "shorten", label: "Make Shorter" },
  { id: "clearer", label: "Make Clearer" },
  { id: "formal", label: "Make More Formal" },
  { id: "persuasive", label: "Make More Persuasive" },
  { id: "grammar", label: "Fix Grammar" },
];

export function ImproveEmailPanel() {
  const [original, setOriginal] = useState("");
  const [improved, setImproved] = useState("");
  const [degraded, setDegraded] = useState<AIFallbackReason | undefined>(undefined);
  const [busy, setBusy] = useState(false);

  async function run(a: ImproveAction) {
    if (!original.trim()) {
      toast.error("Paste an email first.");
      return;
    }
    setBusy(true);
    const r = await improveTextResult(original, a);
    setImproved(r.text);
    setDegraded(r.degraded);
    setBusy(false);
  }

  return (
    <div className="space-y-6">
      <section className="card-soft p-5 sm:p-6">
        <h2 className="text-sm font-semibold text-primary">Improve My Email</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Paste an English email you already wrote and let MyanTone polish it.
        </p>
        <Textarea
          value={original}
          onChange={(e) => setOriginal(e.target.value)}
          placeholder="Paste your English email here…"
          className="mt-4 min-h-40 rounded-2xl text-base"
          aria-label="Original email"
        />
        <div className="mt-4 flex flex-wrap gap-2">
          {ACTIONS.map((a) => (
            <Button key={a.id} size="sm" variant="outline" disabled={busy} onClick={() => run(a.id)}>
              <Sparkles /> {a.label}
            </Button>
          ))}
        </div>
      </section>

      <OfflineModeNotice reason={degraded} />

      {improved && (
        <div className="grid gap-4 md:grid-cols-[1fr_auto_1fr] md:items-center">
          <article className="card-soft p-5">
            <p className="mb-2 text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              Original
            </p>
            <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-muted-foreground">
              {original}
            </p>
          </article>
          <ArrowRight className="mx-auto hidden size-5 text-teal md:block" aria-hidden />
          <article className="card-soft border-teal/40 p-5 ring-2 ring-teal/20">
            <div className="mb-2 flex items-center justify-between">
              <p className="text-[11px] font-bold uppercase tracking-widest text-teal">Improved</p>
              <Button
                size="sm"
                variant="ghost"
                onClick={async () => {
                  await navigator.clipboard.writeText(improved);
                  toast.success("Copied");
                }}
              >
                <Copy /> Copy
              </Button>
            </div>
            <p className="whitespace-pre-wrap text-[15px] leading-relaxed text-primary">{improved}</p>
          </article>
        </div>
      )}
    </div>
  );
}
