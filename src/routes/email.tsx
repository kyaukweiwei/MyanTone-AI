// import { createFileRoute } from "@tanstack/react-router";
// import { useEffect, useState } from "react";
// import { z } from "zod";
// import { toast } from "sonner";
// import { Button } from "@/components/ui/button";
// import { Textarea } from "@/components/ui/textarea";
// import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
// import { UnderstandingCard } from "@/components/UnderstandingCard";
// import { EmailHealthCard } from "@/components/EmailHealthCard";
// import { ImproveEmailPanel } from "@/components/ImproveEmailPanel";
// import { OfflineModeNotice } from "@/components/OfflineModeNotice";
// import { TEMPLATES } from "@/lib/templates";
// import {
//   AUDIENCES,
//   PURPOSES,
//   TONES,
//   generateEmail,
//   improveText,
//   type EmailLength,
//   type GeneratedEmail,
//   type Tone,
// } from "@/lib/myantone-engine";
// import { history } from "@/lib/store";
// import { Copy, Save, Sparkles, Wand2 } from "lucide-react";

// export const Route = createFileRoute("/email")({
//   validateSearch: z.object({ seed: z.string().optional(), template: z.string().optional() }),
//   head: () => ({
//     meta: [
//       { title: "Email Studio — Myanmar to Complete English Emails | MyanTone AI" },
//       {
//         name: "description",
//         content:
//           "Turn a simple Myanmar explanation into a complete, ready-to-send English email with subject lines and a quality check.",
//       },
//       { property: "og:title", content: "Email Studio — MyanTone AI" },
//       {
//         property: "og:description",
//         content: "Myanmar intention in, professional English email out.",
//       },
//     ],
//   }),
//   component: EmailStudio,
// });

// const LENGTHS: { id: EmailLength; label: string }[] = [
//   { id: "short", label: "Short" },
//   { id: "standard", label: "Standard" },
//   { id: "detailed", label: "Detailed" },
// ];

// function Chip({
//   active,
//   children,
//   onClick,
// }: {
//   active: boolean;
//   children: React.ReactNode;
//   onClick: () => void;
// }) {
//   return (
//     <button
//       onClick={onClick}
//       aria-pressed={active}
//       className={`rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors ${
//         active
//           ? "border-teal bg-teal text-teal-foreground"
//           : "border-border bg-card text-muted-foreground hover:border-teal/40 hover:text-primary"
//       }`}
//     >
//       {children}
//     </button>
//   );
// }

// function Step({
//   n,
//   title,
//   children,
// }: {
//   n: number;
//   title: string;
//   children: React.ReactNode;
// }) {
//   return (
//     <div className="border-b border-border/70 px-5 py-5 last:border-0 sm:px-6">
//       <div className="mb-3 flex items-center gap-2.5">
//         <span className="grid size-6 place-items-center rounded-full bg-primary text-[11px] font-bold text-primary-foreground">
//           {n}
//         </span>
//         <h2 className="text-sm font-semibold text-primary">{title}</h2>
//       </div>
//       {children}
//     </div>
//   );
// }

// function EmailStudio() {
//   const { seed, template } = Route.useSearch();
//   const [text, setText] = useState(seed ?? "");
//   const [audience, setAudience] = useState("Manager");
//   const [purpose, setPurpose] = useState("Leave");
//   const [tone, setTone] = useState<Tone>("professional");
//   const [length, setLength] = useState<EmailLength>("standard");
//   const [busy, setBusy] = useState(false);
//   const [email, setEmail] = useState<GeneratedEmail | null>(null);

//   useEffect(() => {
//     const tpl = TEMPLATES.find((t) => t.id === template);
//     if (tpl) {
//       setText(tpl.seed);
//       setAudience(tpl.audience);
//       setPurpose(tpl.purpose);
//       setTone(tpl.tone);
//       setLength(tpl.length);
//     }
//   }, [template]);

//   async function generate() {
//     if (!text.trim()) {
//       toast.error("Tell MyanTone what you want to say first.");
//       return;
//     }
//     setBusy(true);
//     const e = await generateEmail({ text, audience, purpose, tone, length });
//     setEmail(e);
//     setBusy(false);
//     history.add({
//       kind: "email",
//       original: text,
//       output: `${e.greeting}\n\n${e.body}\n\n${e.closing}`,
//       subject: e.subject,
//       tone,
//       audience,
//     });
//   }

//   const fullEmail = email ? `${email.greeting}\n\n${email.body}\n\n${email.closing}` : "";

//   async function transform(action: Parameters<typeof improveText>[1]) {
//     if (!email) return;
//     setBusy(true);
//     const body = await improveText(email.body, action);
//     setEmail({ ...email, body });
//     setBusy(false);
//   }

//   return (
//     <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
//       <header className="mb-8">
//         <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">Email Studio</p>
//         <h1 className="mt-2 text-3xl sm:text-4xl">From a Myanmar note to a ready-to-send email</h1>
//         <p className="mt-2 max-w-2xl text-muted-foreground">
//           Explain the situation in Myanmar. MyanTone handles the subject line, structure, tone and
//           the polite English your reader expects.
//         </p>
//       </header>

//       <Tabs defaultValue="create">
//         <TabsList className="mb-6">
//           <TabsTrigger value="create">Create email</TabsTrigger>
//           <TabsTrigger value="improve">Improve my email</TabsTrigger>
//         </TabsList>

//         <TabsContent value="create">
//           <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
//             <section className="card-soft overflow-hidden p-0">
//               <Step n={1} title="What do you want to say?">
//                 <Textarea
//                   value={text}
//                   onChange={(e) => setText(e.target.value)}
//                   placeholder="မနက်ဖြန် အဖျားရှိလို့ အလုပ်မလာနိုင်ဘူး။ Manager ကို ခွင့်တောင်းတဲ့ email ရေးချင်တယ်။"
//                   className="font-my min-h-36 rounded-2xl text-base"
//                   aria-label="Your message in Myanmar"
//                 />
//                 <p className="mt-2 text-xs text-muted-foreground">
//                   {text.length} characters · Myanmar + English mixing is fully supported
//                 </p>
//               </Step>

//               <Step n={2} title="Who are you emailing?">
//                 <div className="flex flex-wrap gap-2">
//                   {AUDIENCES.map((a) => (
//                     <Chip key={a} active={audience === a} onClick={() => setAudience(a)}>
//                       {a}
//                     </Chip>
//                   ))}
//                 </div>
//               </Step>

//               <Step n={3} title="What is the purpose?">
//                 <div className="flex flex-wrap gap-2">
//                   {PURPOSES.map((p) => (
//                     <Chip key={p} active={purpose === p} onClick={() => setPurpose(p)}>
//                       {p}
//                     </Chip>
//                   ))}
//                 </div>
//                 <Button
//                   size="sm"
//                   variant="soft"
//                   className="mt-3"
//                   onClick={async () => {
//                     setBusy(true);
//                     const e = await generateEmail({ text, audience, purpose, tone, length });
//                     setPurpose(
//                       PURPOSES.find((p) => e.understanding.intent.toLowerCase().includes(p.toLowerCase())) ??
//                         purpose,
//                     );
//                     setBusy(false);
//                     toast.success("Purpose detected from your message");
//                   }}
//                 >
//                   <Wand2 /> Let AI detect purpose
//                 </Button>
//               </Step>

//               <Step n={4} title="Tone">
//                 <div className="flex flex-wrap gap-2">
//                   {TONES.map((t) => (
//                     <Chip key={t.id} active={tone === t.id} onClick={() => setTone(t.id)}>
//                       {t.label}
//                     </Chip>
//                   ))}
//                 </div>
//               </Step>

//               <Step n={5} title="Email length">
//                 <div className="flex flex-wrap gap-2">
//                   {LENGTHS.map((l) => (
//                     <Chip key={l.id} active={length === l.id} onClick={() => setLength(l.id)}>
//                       {l.label}
//                     </Chip>
//                   ))}
//                 </div>
//                 <Button className="mt-5 w-full" size="lg" variant="teal" onClick={generate} disabled={busy}>
//                   <Sparkles /> {busy ? "Writing your email…" : "Generate Email"}
//                 </Button>
//               </Step>
//             </section>

//             <section className="space-y-6">
//               {!email && (
//                 <div className="card-soft grid place-items-center p-10 text-center text-sm text-muted-foreground">
//                   <div>
//                     <Sparkles className="mx-auto mb-3 size-6 text-teal" aria-hidden />
//                     Your generated email will appear here, with subject options and a quality check.
//                   </div>
//                 </div>
//               )}

//               {email && (
//                 <>
//                   <OfflineModeNotice reason={email.degraded} />
//                   <article className="card-soft overflow-hidden">
//                     <div className="border-b border-border bg-secondary/60 px-5 py-4">
//                       <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
//                         Subject
//                       </p>
//                       <p className="text-base font-semibold text-primary">{email.subject}</p>
//                       <p className="mt-2 text-xs text-muted-foreground">To: {email.to}</p>
//                     </div>
//                     <div className="whitespace-pre-wrap px-5 py-5 text-[15px] leading-relaxed text-primary">
//                       {fullEmail}
//                     </div>
//                     {email.placeholders.length > 0 && (
//                       <div className="border-t border-border bg-amber-soft/60 px-5 py-3 text-sm text-primary">
//                         Some details are missing — fill these in before sending:{" "}
//                         <span className="font-medium">{email.placeholders.join(", ")}</span>
//                       </div>
//                     )}
//                     <div className="flex flex-wrap gap-2 border-t border-border px-5 py-4">
//                       <Button
//                         size="sm"
//                         variant="teal"
//                         onClick={async () => {
//                           await navigator.clipboard.writeText(fullEmail);
//                           toast.success("Email copied");
//                         }}
//                       >
//                         <Copy /> Copy Email
//                       </Button>
//                       <Button
//                         size="sm"
//                         variant="outline"
//                         onClick={async () => {
//                           await navigator.clipboard.writeText(email.subject);
//                           toast.success("Subject copied");
//                         }}
//                       >
//                         <Copy /> Copy Subject
//                       </Button>
//                       <Button size="sm" variant="outline" onClick={generate} disabled={busy}>
//                         Regenerate
//                       </Button>
//                       <Button size="sm" variant="outline" onClick={() => transform("shorten")}>
//                         Make Shorter
//                       </Button>
//                       <Button size="sm" variant="outline" onClick={() => transform("formal")}>
//                         Make More Formal
//                       </Button>
//                       <Button size="sm" variant="outline" onClick={() => transform("friendly")}>
//                         Make Friendlier
//                       </Button>
//                       <Button size="sm" variant="outline" onClick={() => transform("improve")}>
//                         Rewrite
//                       </Button>
//                       <Button
//                         size="sm"
//                         variant="outline"
//                         onClick={() => {
//                           history.add({
//                             kind: "email",
//                             original: text,
//                             output: fullEmail,
//                             subject: email.subject,
//                             tone,
//                             audience,
//                             saved: true,
//                           });
//                           toast.success("Saved to History");
//                         }}
//                       >
//                         <Save /> Save
//                       </Button>
//                     </div>
//                   </article>

//                   <section className="card-soft p-5" aria-label="Subject line options">
//                     <h3 className="text-sm font-semibold">Subject line options</h3>
//                     <ul className="mt-3 space-y-2">
//                       {email.subjectOptions.map((s) => (
//                         <li
//                           key={s.label}
//                           className="flex flex-wrap items-center justify-between gap-2 rounded-xl bg-secondary/70 px-3.5 py-2.5"
//                         >
//                           <span>
//                             <span className="mr-2 text-[11px] font-bold uppercase tracking-widest text-teal">
//                               {s.label}
//                             </span>
//                             <span className="text-sm text-primary">{s.value}</span>
//                           </span>
//                           <Button size="sm" variant="ghost" onClick={() => setEmail({ ...email, subject: s.value })}>
//                             Use this subject
//                           </Button>
//                         </li>
//                       ))}
//                     </ul>
//                   </section>

//                   <UnderstandingCard u={email.understanding} />
//                   <EmailHealthCard health={email.health} />
//                 </>
//               )}
//             </section>
//           </div>
//         </TabsContent>

//         <TabsContent value="improve">
//           <ImproveEmailPanel />
//         </TabsContent>
//       </Tabs>
//     </div>
//   );
// }


import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { z } from "zod";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { UnderstandingCard } from "@/components/UnderstandingCard";
import { EmailHealthCard } from "@/components/EmailHealthCard";
import { ImproveEmailPanel } from "@/components/ImproveEmailPanel";
import { OfflineModeNotice } from "@/components/OfflineModeNotice";
import { TEMPLATES } from "@/lib/templates";
import {
  AUDIENCES,
  PURPOSES,
  TONES,
  generateEmail,
  improveText,
  type EmailLength,
  type GeneratedEmail,
  type Tone,
} from "@/lib/myantone-engine";
import { history } from "@/lib/store";
import { Copy, Save, Sparkles, Wand2 } from "lucide-react";

export const Route = createFileRoute("/email")({
  validateSearch: z.object({
    seed: z.string().optional(),
    template: z.string().optional(),
  }),

  head: () => ({
    meta: [
      {
        title:
          "Email Studio — Myanmar to Complete English Emails | MyanTone AI",
      },
      {
        name: "description",
        content:
          "Turn a simple Myanmar explanation into a complete, ready-to-send English email with subject lines and a quality check.",
      },
      {
        property: "og:title",
        content: "Email Studio — MyanTone AI",
      },
      {
        property: "og:description",
        content:
          "Myanmar intention in, professional English email out.",
      },
    ],
  }),

  component: EmailStudio,
});

const LENGTHS: {
  id: EmailLength;
  label: string;
}[] = [
  {
    id: "short",
    label: "Short",
  },
  {
    id: "standard",
    label: "Standard",
  },
  {
    id: "detailed",
    label: "Detailed",
  },
];

function Chip({
  active,
  children,
  onClick,
}: {
  active: boolean;
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors ${
        active
          ? "border-teal bg-teal text-teal-foreground"
          : "border-border bg-card text-muted-foreground hover:border-teal/40 hover:text-primary"
      }`}
    >
      {children}
    </button>
  );
}

function Step({
  n,
  title,
  children,
}: {
  n: number;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="border-b border-border/70 px-5 py-5 last:border-0 sm:px-6">
      <div className="mb-3 flex items-center gap-2.5">
        <span className="grid size-6 place-items-center rounded-full bg-primary text-[11px] font-bold text-primary-foreground">
          {n}
        </span>

        <h2 className="text-sm font-semibold text-primary">
          {title}
        </h2>
      </div>

      {children}
    </div>
  );
}

function EmailStudio() {
  const { seed, template } = Route.useSearch();

  const [text, setText] = useState(seed ?? "");
  const [audience, setAudience] = useState("Manager");
  const [purpose, setPurpose] = useState("Leave");
  const [tone, setTone] = useState<Tone>("professional");
  const [length, setLength] =
    useState<EmailLength>("standard");

  const [busy, setBusy] = useState(false);
  const [email, setEmail] =
    useState<GeneratedEmail | null>(null);

  useEffect(() => {
    const tpl = TEMPLATES.find(
      (t) => t.id === template,
    );

    if (tpl) {
      setText(tpl.seed);
      setAudience(tpl.audience);
      setPurpose(tpl.purpose);
      setTone(tpl.tone);
      setLength(tpl.length);

      // Prevent an old generated email from
      // being displayed with the new template.
      setEmail(null);
    }
  }, [template]);

  async function generate() {
    if (!text.trim()) {
      toast.error(
        "Tell MyanTone what you want to say first.",
      );
      return;
    }

    setBusy(true);

    try {
      /*
       * IMPORTANT:
       * Only the currently selected tone is sent
       * to generateEmail().
       */
      const e = await generateEmail({
        text,
        audience,
        purpose,
        tone,
        length,
      });

      setEmail(e);

      history.add({
        kind: "email",
        original: text,
        output: `${e.greeting}\n\n${e.body}\n\n${e.closing}`,
        subject: e.subject,
        tone,
        audience,
      });
    } catch (error) {
      console.error("Email generation failed:", error);
      toast.error(
        "Could not generate the email. Please try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  const fullEmail = email
    ? `${email.greeting}\n\n${email.body}\n\n${email.closing}`
    : "";

  async function transform(
    action: Parameters<typeof improveText>[1],
  ) {
    if (!email) return;

    setBusy(true);

    try {
      const body = await improveText(
        email.body,
        action,
      );

      setEmail({
        ...email,
        body,
      });
    } catch (error) {
      console.error("Email transformation failed:", error);
      toast.error(
        "Could not update the email.",
      );
    } finally {
      setBusy(false);
    }
  }

  /*
   * When the user changes tone, remove the previous
   * result so that an old tone is never shown under
   * the newly selected tone.
   */
  function handleToneChange(newTone: Tone) {
    setTone(newTone);

    if (email) {
      setEmail(null);
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
      <header className="mb-8">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">
          Email Studio
        </p>

        <h1 className="mt-2 text-3xl sm:text-4xl">
          From a Myanmar note to a ready-to-send email
        </h1>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          Explain the situation in Myanmar. MyanTone
          handles the subject line, structure, tone and
          the polite English your reader expects.
        </p>
      </header>

      <Tabs defaultValue="create">
        <TabsList className="mb-6">
          <TabsTrigger value="create">
            Create email
          </TabsTrigger>

          <TabsTrigger value="improve">
            Improve my email
          </TabsTrigger>
        </TabsList>

        <TabsContent value="create">
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
            {/* LEFT SIDE */}
            <section className="card-soft overflow-hidden p-0">
              {/* STEP 1 */}
              <Step
                n={1}
                title="What do you want to say?"
              >
                <Textarea
                  value={text}
                  onChange={(e) =>
                    setText(e.target.value)
                  }
                  placeholder="မနက်ဖြန် အဖျားရှိလို့ အလုပ်မလာနိုင်ဘူး။ Manager ကို ခွင့်တောင်းတဲ့ email ရေးချင်တယ်။"
                  className="font-my min-h-36 rounded-2xl text-base"
                  aria-label="Your message in Myanmar"
                />

                <p className="mt-2 text-xs text-muted-foreground">
                  {text.length} characters · Myanmar +
                  English mixing is fully supported
                </p>
              </Step>

              {/* STEP 2 */}
              <Step
                n={2}
                title="Who are you emailing?"
              >
                <div className="flex flex-wrap gap-2">
                  {AUDIENCES.map((a) => (
                    <Chip
                      key={a}
                      active={audience === a}
                      onClick={() => {
                        setAudience(a);

                        // Remove previous result because
                        // the email configuration changed.
                        if (email) {
                          setEmail(null);
                        }
                      }}
                    >
                      {a}
                    </Chip>
                  ))}
                </div>
              </Step>

              {/* STEP 3 */}
              <Step
                n={3}
                title="What is the purpose?"
              >
                <div className="flex flex-wrap gap-2">
                  {PURPOSES.map((p) => (
                    <Chip
                      key={p}
                      active={purpose === p}
                      onClick={() => {
                        setPurpose(p);

                        if (email) {
                          setEmail(null);
                        }
                      }}
                    >
                      {p}
                    </Chip>
                  ))}
                </div>

                <Button
                  size="sm"
                  variant="soft"
                  className="mt-3"
                  onClick={async () => {
                    if (!text.trim()) {
                      toast.error(
                        "Write your message first.",
                      );
                      return;
                    }

                    setBusy(true);

                    try {
                      const e =
                        await generateEmail({
                          text,
                          audience,
                          purpose,
                          tone,
                          length,
                        });

                      setPurpose(
                        PURPOSES.find((p) =>
                          e.understanding.intent
                            .toLowerCase()
                            .includes(
                              p.toLowerCase(),
                            ),
                        ) ?? purpose,
                      );

                      setEmail(null);

                      toast.success(
                        "Purpose detected from your message",
                      );
                    } catch (error) {
                      console.error(
                        "Purpose detection failed:",
                        error,
                      );

                      toast.error(
                        "Could not detect the purpose.",
                      );
                    } finally {
                      setBusy(false);
                    }
                  }}
                >
                  <Wand2 />
                  Let AI detect purpose
                </Button>
              </Step>

              {/* STEP 4 — TONE */}
              <Step n={4} title="Tone">
                <div className="flex flex-wrap gap-2">
                  {TONES.map((t) => (
                    <Chip
                      key={t.id}
                      active={tone === t.id}
                      onClick={() =>
                        handleToneChange(t.id)
                      }
                    >
                      {t.label}
                    </Chip>
                  ))}
                </div>

                <p className="mt-3 text-xs text-muted-foreground">
                  Select one tone. MyanTone will generate
                  the email in this tone only.
                </p>
              </Step>

              {/* STEP 5 */}
              <Step
                n={5}
                title="Email length"
              >
                <div className="flex flex-wrap gap-2">
                  {LENGTHS.map((l) => (
                    <Chip
                      key={l.id}
                      active={length === l.id}
                      onClick={() => {
                        setLength(l.id);

                        if (email) {
                          setEmail(null);
                        }
                      }}
                    >
                      {l.label}
                    </Chip>
                  ))}
                </div>

                <Button
                  className="mt-5 w-full"
                  size="lg"
                  variant="teal"
                  onClick={generate}
                  disabled={busy}
                >
                  <Sparkles />

                  {busy
                    ? "Writing your email…"
                    : "Generate Email"}
                </Button>
              </Step>
            </section>

            {/* RIGHT SIDE */}
            <section className="space-y-6">
              {!email && (
                <div className="card-soft grid place-items-center p-10 text-center text-sm text-muted-foreground">
                  <div>
                    <Sparkles
                      className="mx-auto mb-3 size-6 text-teal"
                      aria-hidden
                    />

                    <p>
                      Your generated email will
                      appear here.
                    </p>

                    <p className="mt-2 text-xs">
                      Selected tone:{" "}
                      <span className="font-semibold text-primary">
                        {TONES.find(
                          (t) => t.id === tone,
                        )?.label ?? tone}
                      </span>
                    </p>
                  </div>
                </div>
              )}

              {email && (
                <>
                  <OfflineModeNotice
                    reason={email.degraded}
                  />

                  {/* GENERATED EMAIL */}
                  <article className="card-soft overflow-hidden">
                    <div className="border-b border-border bg-secondary/60 px-5 py-4">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div>
                          <p className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                            Generated Email
                          </p>

                          <p className="mt-1 text-xs text-teal">
                            Tone:{" "}
                            <span className="font-bold uppercase">
                              {tone}
                            </span>
                          </p>
                        </div>
                      </div>

                      <p className="mt-3 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                        Subject
                      </p>

                      <p className="text-base font-semibold text-primary">
                        {email.subject}
                      </p>

                      <p className="mt-2 text-xs text-muted-foreground">
                        To: {email.to}
                      </p>
                    </div>

                    <div className="whitespace-pre-wrap px-5 py-5 text-[15px] leading-relaxed text-primary">
                      {fullEmail}
                    </div>

                    {email.placeholders.length > 0 && (
                      <div className="border-t border-border bg-amber-soft/60 px-5 py-3 text-sm text-primary">
                        Some details are missing —
                        fill these in before sending:{" "}
                        <span className="font-medium">
                          {email.placeholders.join(
                            ", ",
                          )}
                        </span>
                      </div>
                    )}

                    {/* ACTIONS */}
                    <div className="flex flex-wrap gap-2 border-t border-border px-5 py-4">
                      <Button
                        size="sm"
                        variant="teal"
                        onClick={async () => {
                          await navigator.clipboard.writeText(
                            fullEmail,
                          );

                          toast.success(
                            "Email copied",
                          );
                        }}
                      >
                        <Copy />
                        Copy Email
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={async () => {
                          await navigator.clipboard.writeText(
                            email.subject,
                          );

                          toast.success(
                            "Subject copied",
                          );
                        }}
                      >
                        <Copy />
                        Copy Subject
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={generate}
                        disabled={busy}
                      >
                        Regenerate
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          transform("shorten")
                        }
                        disabled={busy}
                      >
                        Make Shorter
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          transform("formal")
                        }
                        disabled={busy}
                      >
                        Make More Formal
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          transform("friendly")
                        }
                        disabled={busy}
                      >
                        Make Friendlier
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          transform("improve")
                        }
                        disabled={busy}
                      >
                        Rewrite
                      </Button>

                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          history.add({
                            kind: "email",
                            original: text,
                            output: fullEmail,
                            subject: email.subject,
                            tone,
                            audience,
                            saved: true,
                          });

                          toast.success(
                            "Saved to History",
                          );
                        }}
                      >
                        <Save />
                        Save
                      </Button>
                    </div>
                  </article>

                  {/* SUBJECT OPTIONS */}
                  <section
                    className="card-soft p-5"
                    aria-label="Subject line options"
                  >
                    <h3 className="text-sm font-semibold">
                      Subject line options
                    </h3>

                    <ul className="mt-3 space-y-2">
                      {email.subjectOptions.map(
                        (s) => (
                          <li
                            key={s.label}
                            className="flex flex-wrap items-center justify-between gap-2 rounded-xl bg-secondary/70 px-3.5 py-2.5"
                          >
                            <span>
                              <span className="mr-2 text-[11px] font-bold uppercase tracking-widest text-teal">
                                {s.label}
                              </span>

                              <span className="text-sm text-primary">
                                {s.value}
                              </span>
                            </span>

                            <Button
                              size="sm"
                              variant="ghost"
                              onClick={() =>
                                setEmail({
                                  ...email,
                                  subject: s.value,
                                })
                              }
                            >
                              Use this subject
                            </Button>
                          </li>
                        ),
                      )}
                    </ul>
                  </section>

                  {/* UNDERSTANDING */}
                  <UnderstandingCard
                    u={email.understanding}
                  />

                  {/* EMAIL HEALTH */}
                  <EmailHealthCard
                    health={email.health}
                  />
                </>
              )}
            </section>
          </div>
        </TabsContent>

        {/* IMPROVE EMAIL */}
        <TabsContent value="improve">
          <ImproveEmailPanel />
        </TabsContent>
      </Tabs>
    </div>
  );
}
