// import { createFileRoute, useNavigate } from "@tanstack/react-router";
// import { useState } from "react";
// import { toast } from "sonner";
// import { Button } from "@/components/ui/button";
// import { Textarea } from "@/components/ui/textarea";
// import {
//   Select,
//   SelectContent,
//   SelectItem,
//   SelectTrigger,
//   SelectValue,
// } from "@/components/ui/select";
// import { UnderstandingCard } from "@/components/UnderstandingCard";
// import { AIActionBar, type BarAction } from "@/components/AIActionBar";
// import { OfflineModeNotice } from "@/components/OfflineModeNotice";
// import {
//   AUDIENCES,
//   CONTEXTS,
//   PIPELINE_STAGES,
//   TONES,
//   improveText,
//   translate,
//   type Tone,
//   type TranslationResult,
// } from "@/lib/myantone-engine";
// import { history } from "@/lib/store";
// import { Copy, Eraser, ClipboardPaste, Sparkles, Mail } from "lucide-react";

// export const Route = createFileRoute("/translate")({
//   head: () => ({
//     meta: [
//       { title: "Translate Myanmar to Natural English — MyanTone AI" },
//       {
//         name: "description",
//         content:
//           "Say what you mean in Myanmar and get natural English in five tones: simple, polite, friendly, professional and formal.",
//       },
//       { property: "og:title", content: "Translate Myanmar to Natural English — MyanTone AI" },
//       {
//         property: "og:description",
//         content: "Meaning-first Myanmar to English translation with tone control.",
//       },
//     ],
//   }),
//   component: TranslatePage,
// });

// const SAMPLE = "ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်…";

// function TranslatePage() {
//   const navigate = useNavigate();
//   const [text, setText] = useState("");
//   const [context, setContext] = useState<string>("General");
//   const [audience, setAudience] = useState<string>("Auto-detect");
//   const [tone, setTone] = useState<Tone>("professional");
//   const [busy, setBusy] = useState(false);
//   const [result, setResult] = useState<TranslationResult | null>(null);

//   async function run() {
//     if (!text.trim()) {
//       toast.error("Please write what you want to say first.");
//       return;
//     }
//     setBusy(true);
//     const r = await translate(text, { audience, tone, context });
//     setResult(r);
//     setBusy(false);
//     history.add({
//       kind: "translation",
//       original: text,
//       output: r.variants.find((v) => v.tone === tone)?.text ?? r.variants[0]!.text,
//       tone,
//       audience: r.understanding.audience,
//     });
//   }

//   async function onAction(a: BarAction) {
//     if (!result) return;
//     const current = result.variants.find((v) => v.tone === tone) ?? result.variants[0]!;
//     if (a === "copy") {
//       await navigator.clipboard.writeText(current.text);
//       toast.success("Copied to clipboard");
//       return;
//     }
//     if (a === "regenerate") return run();
//     setBusy(true);
//     const improved = await improveText(current.text, a);
//     setResult({
//       ...result,
//       variants: result.variants.map((v) => (v.tone === current.tone ? { ...v, text: improved } : v)),
//     });
//     setBusy(false);
//   }

//   return (
//     <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
//       <header className="mb-8">
//         <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">Myanmar → English</p>
//         <h1 className="mt-2 text-3xl sm:text-4xl">Say what you mean.</h1>
//         <p className="mt-2 text-muted-foreground">We'll help you say it naturally.</p>
//       </header>

//       <div className="grid gap-6 lg:grid-cols-[1.15fr_.85fr]">
//         <section className="card-soft p-5 sm:p-6">
//           <div className="mb-3 flex items-center justify-between">
//             <label htmlFor="source" className="text-sm font-semibold text-primary">
//               What do you want to say?
//             </label>
//             <div className="flex gap-1">
//               <Button
//                 size="sm"
//                 variant="ghost"
//                 onClick={async () => {
//                   try {
//                     setText(await navigator.clipboard.readText());
//                   } catch {
//                     toast.error("Clipboard not available");
//                   }
//                 }}
//               >
//                 <ClipboardPaste /> Paste
//               </Button>
//               <Button size="sm" variant="ghost" onClick={() => setText("")}>
//                 <Eraser /> Clear
//               </Button>
//             </div>
//           </div>
//           <Textarea
//             id="source"
//             value={text}
//             onChange={(e) => setText(e.target.value)}
//             placeholder={SAMPLE}
//             className="font-my min-h-44 resize-y rounded-2xl border-border bg-background text-base"
//           />
//           <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
//             <span>Myanmar, English, or a natural mix of both.</span>
//             <span>{text.length} characters</span>
//           </div>

//           <div className="mt-5 grid gap-4 sm:grid-cols-2">
//             <div>
//               <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
//                 Context
//               </label>
//               <Select value={context} onValueChange={setContext}>
//                 <SelectTrigger aria-label="Context">
//                   <SelectValue />
//                 </SelectTrigger>
//                 <SelectContent>
//                   {CONTEXTS.map((c) => (
//                     <SelectItem key={c} value={c}>
//                       {c}
//                     </SelectItem>
//                   ))}
//                 </SelectContent>
//               </Select>
//             </div>
//             <div>
//               <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
//                 Audience
//               </label>
//               <Select value={audience} onValueChange={setAudience}>
//                 <SelectTrigger aria-label="Audience">
//                   <SelectValue placeholder="Choose audience" />
//                 </SelectTrigger>
//                 <SelectContent>
//                   <SelectItem value="Auto-detect">Auto-detect</SelectItem>
//                   {AUDIENCES.map((a) => (
//                     <SelectItem key={a} value={a}>
//                       {a}
//                     </SelectItem>
//                   ))}
//                 </SelectContent>
//               </Select>
//             </div>
//           </div>

//           <div className="mt-5">
//             <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
//               Tone
//             </span>
//             <div className="flex flex-wrap gap-2" role="radiogroup" aria-label="Tone">
//               {TONES.map((t) => (
//                 <button
//                   key={t.id}
//                   role="radio"
//                   aria-checked={tone === t.id}
//                   onClick={() => setTone(t.id)}
//                   className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
//                     tone === t.id
//                       ? "border-teal bg-teal text-teal-foreground"
//                       : "border-border bg-card text-muted-foreground hover:border-teal/40 hover:text-primary"
//                   }`}
//                 >
//                   {t.label}
//                 </button>
//               ))}
//             </div>
//           </div>

//           <Button className="mt-6 w-full" size="lg" variant="teal" onClick={run} disabled={busy}>
//             <Sparkles /> {busy ? "Understanding your meaning…" : "Translate Naturally"}
//           </Button>
//         </section>

//         <aside className="space-y-6">
//           {result ? (
//             <UnderstandingCard u={result.understanding} />
//           ) : (
//             <section className="card-soft p-5">
//               <h2 className="text-sm font-semibold">How MyanTone thinks</h2>
//               <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
//                 {PIPELINE_STAGES.map((s, i) => (
//                   <li key={s} className="flex gap-3">
//                     <span className="grid size-5 shrink-0 place-items-center rounded-full bg-secondary text-[10px] font-bold text-primary">
//                       {i + 1}
//                     </span>
//                     {s}
//                   </li>
//                 ))}
//               </ol>
//             </section>
//           )}
//         </aside>
//       </div>

//       {result && (
//         <section className="mt-8" aria-label="Translation results">
//           <OfflineModeNotice reason={result.degraded} />
//           <h2 className="mb-4 mt-4 text-lg">Your message, in five tones</h2>
//           <div className="grid gap-4 sm:grid-cols-2">
//             {result.variants.map((v) => (
//               <article
//                 key={v.tone}
//                 className={`card-soft p-5 transition-shadow hover:shadow-[var(--shadow-lift)] ${
//                   v.tone === tone ? "ring-2 ring-teal/40" : ""
//                 }`}
//               >
//                 <div className="flex items-center justify-between">
//                   <span className="text-[11px] font-bold uppercase tracking-widest text-teal">
//                     {v.tone}
//                   </span>
//                   <Button
//                     size="sm"
//                     variant="ghost"
//                     aria-label={`Copy ${v.tone} version`}
//                     onClick={async () => {
//                       await navigator.clipboard.writeText(v.text);
//                       toast.success("Copied");
//                     }}
//                   >
//                     <Copy /> Copy
//                   </Button>
//                 </div>
//                 <p className="mt-2 text-[15px] leading-relaxed text-primary">{v.text}</p>
//               </article>
//             ))}
//           </div>

//           <div className="mt-6 flex flex-col gap-3">
//             <AIActionBar onAction={onAction} busy={busy} />
//             <Button
//               variant="amber"
//               className="self-start"
//               onClick={() => navigate({ to: "/email", search: { seed: text } })}
//             >
//               <Mail /> Create Email from this
//             </Button>
//           </div>
//         </section>
//       )}
//     </div>
//   );
// }




import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { UnderstandingCard } from "@/components/UnderstandingCard";
import { AIActionBar, type BarAction } from "@/components/AIActionBar";
import { OfflineModeNotice } from "@/components/OfflineModeNotice";
import {
  AUDIENCES,
  CONTEXTS,
  PIPELINE_STAGES,
  TONES,
  improveText,
  translate,
  type Tone,
  type TranslationResult,
} from "@/lib/myantone-engine";
import { history } from "@/lib/store";
import { Copy, Eraser, ClipboardPaste, Sparkles, Mail } from "lucide-react";

export const Route = createFileRoute("/translate")({
  head: () => ({
    meta: [
      { title: "Translate Myanmar to Natural English — MyanTone AI" },
      {
        name: "description",
        content:
          "Say what you mean in Myanmar and get natural English with your selected tone.",
      },
      {
        property: "og:title",
        content: "Translate Myanmar to Natural English — MyanTone AI",
      },
      {
        property: "og:description",
        content: "Meaning-first Myanmar to English translation with tone control.",
      },
    ],
  }),
  component: TranslatePage,
});

const SAMPLE =
  "ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်…";

function TranslatePage() {
  const navigate = useNavigate();

  const [text, setText] = useState("");
  const [context, setContext] = useState<string>("General");
  const [audience, setAudience] = useState<string>("Auto-detect");
  const [tone, setTone] = useState<Tone>("professional");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<TranslationResult | null>(null);

  async function run() {
    if (!text.trim()) {
      toast.error("Please write what you want to say first.");
      return;
    }

    setBusy(true);

    try {
      const r = await translate(text, {
        audience,
        tone,
        context,
      });

      setResult(r);

      const selectedVariant =
        r.variants.find((v) => v.tone === tone) ?? r.variants[0];

      if (selectedVariant) {
        history.add({
          kind: "translation",
          original: text,
          output: selectedVariant.text,
          tone,
          audience: r.understanding.audience,
        });
      }
    } catch (error) {
      console.error("Translation failed:", error);
      toast.error("Translation failed. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  async function onAction(a: BarAction) {
    if (!result) return;

    const current =
      result.variants.find((v) => v.tone === tone) ?? result.variants[0];

    if (!current) return;

    if (a === "copy") {
      await navigator.clipboard.writeText(current.text);
      toast.success("Copied to clipboard");
      return;
    }

    if (a === "regenerate") {
      return run();
    }

    setBusy(true);

    try {
      const improved = await improveText(current.text, a);

      setResult({
        ...result,
        variants: result.variants.map((v) =>
          v.tone === current.tone
            ? {
                ...v,
                text: improved,
              }
            : v,
        ),
      });
    } catch (error) {
      console.error("Improve text failed:", error);
      toast.error("Could not improve the translation.");
    } finally {
      setBusy(false);
    }
  }

  /*
   * Only show the currently selected tone.
   *
   * Example:
   * tone = "simple"
   * → only Simple result appears
   *
   * tone = "professional"
   * → only Professional result appears
   */
  const selectedVariant =
    result?.variants.find((v) => v.tone === tone) ??
    result?.variants[0] ??
    null;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <header className="mb-8">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">
          Myanmar → English
        </p>

        <h1 className="mt-2 text-3xl sm:text-4xl">
          Say what you mean.
        </h1>

        <p className="mt-2 text-muted-foreground">
          We'll help you say it naturally.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-[1.15fr_.85fr]">
        {/* INPUT SECTION */}
        <section className="card-soft p-5 sm:p-6">
          <div className="mb-3 flex items-center justify-between">
            <label
              htmlFor="source"
              className="text-sm font-semibold text-primary"
            >
              What do you want to say?
            </label>

            <div className="flex gap-1">
              <Button
                size="sm"
                variant="ghost"
                onClick={async () => {
                  try {
                    setText(await navigator.clipboard.readText());
                  } catch {
                    toast.error("Clipboard not available");
                  }
                }}
              >
                <ClipboardPaste />
                Paste
              </Button>

              <Button
                size="sm"
                variant="ghost"
                onClick={() => setText("")}
              >
                <Eraser />
                Clear
              </Button>
            </div>
          </div>

          <Textarea
            id="source"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={SAMPLE}
            className="font-my min-h-44 resize-y rounded-2xl border-border bg-background text-base"
          />

          <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
            <span>
              Myanmar, English, or a natural mix of both.
            </span>

            <span>{text.length} characters</span>
          </div>

          {/* CONTEXT + AUDIENCE */}
          <div className="mt-5 grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Context
              </label>

              <Select
                value={context}
                onValueChange={setContext}
              >
                <SelectTrigger aria-label="Context">
                  <SelectValue />
                </SelectTrigger>

                <SelectContent>
                  {CONTEXTS.map((c) => (
                    <SelectItem key={c} value={c}>
                      {c}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Audience
              </label>

              <Select
                value={audience}
                onValueChange={setAudience}
              >
                <SelectTrigger aria-label="Audience">
                  <SelectValue placeholder="Choose audience" />
                </SelectTrigger>

                <SelectContent>
                  <SelectItem value="Auto-detect">
                    Auto-detect
                  </SelectItem>

                  {AUDIENCES.map((a) => (
                    <SelectItem key={a} value={a}>
                      {a}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* TONE */}
          <div className="mt-5">
            <span className="mb-2 block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Tone
            </span>

            <div
              className="flex flex-wrap gap-2"
              role="radiogroup"
              aria-label="Tone"
            >
              {TONES.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  role="radio"
                  aria-checked={tone === t.id}
                  onClick={() => setTone(t.id)}
                  className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
                    tone === t.id
                      ? "border-teal bg-teal text-teal-foreground"
                      : "border-border bg-card text-muted-foreground hover:border-teal/40 hover:text-primary"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          {/* TRANSLATE BUTTON */}
          <Button
            className="mt-6 w-full"
            size="lg"
            variant="teal"
            onClick={run}
            disabled={busy}
          >
            <Sparkles />

            {busy
              ? "Understanding your meaning…"
              : "Translate Naturally"}
          </Button>
        </section>

        {/* AI UNDERSTANDING */}
        <aside className="space-y-6">
          {result ? (
            <UnderstandingCard u={result.understanding} />
          ) : (
            <section className="card-soft p-5">
              <h2 className="text-sm font-semibold">
                How MyanTone thinks
              </h2>

              <ol className="mt-3 space-y-2 text-sm text-muted-foreground">
                {PIPELINE_STAGES.map((s, i) => (
                  <li key={s} className="flex gap-3">
                    <span className="grid size-5 shrink-0 place-items-center rounded-full bg-secondary text-[10px] font-bold text-primary">
                      {i + 1}
                    </span>

                    {s}
                  </li>
                ))}
              </ol>
            </section>
          )}
        </aside>
      </div>

      {/* TRANSLATION RESULT */}
      {result && selectedVariant && (
        <section
          className="mt-8"
          aria-label="Translation result"
        >
          <OfflineModeNotice reason={result.degraded} />

          <h2 className="mb-4 mt-4 text-lg">
            Your translation
          </h2>

          {/* ONLY SELECTED TONE IS DISPLAYED */}
          <article className="card-soft p-5 transition-shadow hover:shadow-[var(--shadow-lift)] ring-2 ring-teal/40">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-widest text-teal">
                {selectedVariant.tone}
              </span>

              <Button
                size="sm"
                variant="ghost"
                aria-label={`Copy ${selectedVariant.tone} version`}
                onClick={async () => {
                  await navigator.clipboard.writeText(
                    selectedVariant.text,
                  );

                  toast.success("Copied");
                }}
              >
                <Copy />
                Copy
              </Button>
            </div>

            <p className="mt-2 text-[15px] leading-relaxed text-primary">
              {selectedVariant.text}
            </p>
          </article>

          {/* ACTION BAR */}
          <div className="mt-6 flex flex-col gap-3">
            <AIActionBar
              onAction={onAction}
              busy={busy}
            />

            <Button
              variant="amber"
              className="self-start"
              onClick={() =>
                navigate({
                  to: "/email",
                  search: { seed: text },
                })
              }
            >
              <Mail />
              Create Email from this
            </Button>
          </div>
        </section>
      )}
    </div>
  );
}
