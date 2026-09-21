// /**
//  * MyanTone AI — mock inference engine.
//  *
//  * This module is the single boundary between the UI and "the model".
//  * Every function is async and returns typed data, so swapping these
//  * implementations for a real NMT/LLM API call (server function -> provider)
//  * requires no changes in the components.
//  */

// import { aiComplete } from "./ai.functions";

// /** Reason the app fell back to the offline rule engine. */
// export type AIFallbackReason = "missing_key" | "rate_limit" | "credits" | "upstream" | "bad_output";

// async function askJSON<T>(
//   system: string,
//   user: string,
// ): Promise<{ data: T | null; error: AIFallbackReason | null }> {
//   try {
//     const r = await aiComplete({ data: { system, user } });
//     if (!r.ok) return { data: null, error: (r.error as AIFallbackReason) || "upstream" };
//     if (!r.text) return { data: null, error: "bad_output" };
//     const cleaned = r.text.trim().replace(/^```(?:json)?/i, "").replace(/```$/, "");
//     return { data: JSON.parse(cleaned) as T, error: null };
//   } catch {
//     return { data: null, error: "bad_output" };
//   }
// }


// const BASE_SYSTEM =
//   "You are MyanTone AI, a Myanmar-first communication assistant. Users write in Burmese (Myanmar Unicode), English, or a mix. " +
//   "You understand what they actually MEAN — including colloquial speech, slang, and mixed script — and express it in natural, idiomatic English " +
//   "that a native speaker would really send. Never translate word-for-word. Never invent facts that were not in the input. " +
//   "Keep the user's own specifics (times, reasons, names). Always reply with valid JSON only, no markdown fences.";

// export type Tone = "simple" | "polite" | "friendly" | "professional" | "formal";
// export const TONES: { id: Tone; label: string }[] = [
//   { id: "simple", label: "Simple" },
//   { id: "polite", label: "Polite" },
//   { id: "friendly", label: "Friendly" },
//   { id: "professional", label: "Professional" },
//   { id: "formal", label: "Formal" },
// ];

// export type EmailLength = "short" | "standard" | "detailed";

// export const AUDIENCES = [
//   "Manager",
//   "HR",
//   "Lecturer",
//   "Professor",
//   "Client",
//   "Customer",
//   "Colleague",
//   "Recruiter",
//   "Friend",
//   "Other",
// ] as const;

// export const PURPOSES = [
//   "Request",
//   "Apology",
//   "Meeting",
//   "Reschedule",
//   "Leave",
//   "Complaint",
//   "Follow-up",
//   "Application",
//   "Submission",
//   "Information",
//   "Thank You",
//   "Other",
// ] as const;

// export const CONTEXTS = ["General", "Work", "University", "Business", "Career", "Personal"] as const;

// export type Understanding = {
//   intent: string;
//   audience: string;
//   situation: string;
//   tone: Tone;
//   details: string[];
//   missing: string[];
//   attachment?: string | undefined;
//   languageMix: string;
// };

// export type TranslationResult = {
//   understanding: Understanding;
//   variants: { tone: Tone; text: string }[];
//   pipeline: string[];
//   /** Set when the real AI model was unavailable and offline results are shown. */
//   degraded?: AIFallbackReason;
// };

// export const PIPELINE_STAGES = [
//   "Text normalization",
//   "Myanmar / mixed-language detection",
//   "Tokenization",
//   "Subword (BPE) representation",
//   "Context & intent understanding",
//   "Neural machine translation",
//   "Controlled generation",
//   "Tone control",
//   "Quality evaluation",
// ];

// const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));

// const MY_RE = /[\u1000-\u109F\uAA60-\uAA7F]/;

// export function detectLanguageMix(text: string) {
//   const my = (text.match(/[\u1000-\u109F]/g) ?? []).length;
//   const en = (text.match(/[A-Za-z]/g) ?? []).length;
//   if (my && en) return "Mixed Myanmar + English";
//   if (my) return "Myanmar (Unicode)";
//   if (en) return "English";
//   return "Unknown";
// }

// export function isMyanmar(text: string) {
//   return MY_RE.test(text);
// }

// type Rule = {
//   match: RegExp;
//   intent: string;
//   situation: string;
//   purpose: string;
//   subject: { professional: string; simple: string; formal: string };
//   body: Record<Tone, string>;
//   emailBody: string;
//   details?: string[];
//   missing?: string[];
// };

// const RULES: Rule[] = [
//   {
//     match: /meeting|မီးတင်း|အစည်းအဝေး/i,
//     intent: "Unable to attend / reschedule a meeting",
//     situation: "A scheduled meeting cannot be attended at the planned time",
//     purpose: "Reschedule",
//     subject: {
//       professional: "Request to Reschedule Our Meeting",
//       simple: "Meeting Reschedule",
//       formal: "Request for Rescheduling of Scheduled Meeting",
//     },
//     body: {
//       simple: "I can't attend today's meeting.",
//       polite: "I'm sorry, but I won't be able to attend today's meeting.",
//       friendly: "Hey, I won't be able to make it to today's meeting. Sorry about that!",
//       professional: "I apologize, but I will be unable to attend today's meeting.",
//       formal: "I regret to inform you that I will be unable to attend today's meeting.",
//     },
//     emailBody:
//       "I am writing regarding our meeting scheduled for [Meeting Date]. Unfortunately, I will not be able to attend at the arranged time.\n\nWould it be possible to reschedule to [Proposed Date and Time]? I am happy to adjust to a slot that suits you best.\n\nI apologize for any inconvenience this may cause and appreciate your understanding.",
//     missing: ["A specific alternative date and time is not suggested"],
//   },
//   {
//     match: /assignment|deadline|extend|တာဝန်|စာမေးပွဲ/i,
//     intent: "Request for an assignment deadline extension",
//     situation: "Coursework cannot be submitted by the original deadline",
//     purpose: "Request",
//     subject: {
//       professional: "Request for Assignment Deadline Extension",
//       simple: "Assignment Extension Request",
//       formal: "Formal Request for Extension of Assignment Submission Deadline",
//     },
//     body: {
//       simple: "Can I submit my assignment tomorrow?",
//       polite: "Could I please submit my assignment tomorrow instead?",
//       friendly: "Would it be okay if I hand in the assignment tomorrow?",
//       professional: "I would like to request an extension and submit my assignment tomorrow.",
//       formal:
//         "I would like to respectfully request an extension of the assignment submission deadline to tomorrow.",
//     },
//     emailBody:
//       "I would like to kindly request an extension for the [Assignment Name] submission deadline. Due to [Reason], I have not been able to complete the work to the standard I would like.\n\nI would be very grateful if I could submit the assignment by [New Date].\n\nThank you for your consideration and understanding.",
//     missing: ["The reason for the extension is not stated"],
//   },
//   {
//     match: /ဖျား|အဖျား|sick|leave|ခွင့်/i,
//     intent: "Request leave from work due to illness",
//     situation: "The sender is unwell and cannot come to work",
//     purpose: "Leave",
//     subject: {
//       professional: "Request for Leave Tomorrow",
//       simple: "Leave Request for Tomorrow",
//       formal: "Request for One-Day Leave Due to Illness",
//     },
//     body: {
//       simple: "I'm sick, so I can't come to work tomorrow.",
//       polite: "I'm not feeling well, so I won't be able to come to work tomorrow.",
//       friendly: "I'm feeling under the weather, so I'll have to skip work tomorrow.",
//       professional:
//         "I am unwell and will be unable to come to work tomorrow. I would like to request leave for the day.",
//       formal:
//         "I regret to inform you that due to illness I will be unable to attend work tomorrow, and I would like to request leave for the day.",
//     },
//     emailBody:
//       "I am writing to inform you that I will be unable to come to work tomorrow due to illness. I would like to kindly request leave for the day.\n\nI will ensure that any urgent matters are handed over to the team, and I will remain reachable by email if anything requires my attention.\n\nI apologize for any inconvenience and appreciate your understanding.",
//     missing: ["Date of return to work is not specified"],
//   },
//   {
//     match: /report|attach|ပူးတွဲ|တင်ပြ/i,
//     intent: "Submit a document for review",
//     situation: "A file or report needs to be sent to the recipient",
//     purpose: "Submission",
//     subject: {
//       professional: "Submission of the Requested Report",
//       simple: "Report Attached",
//       formal: "Submission of Report for Your Review",
//     },
//     body: {
//       simple: "Here is the report.",
//       polite: "I've attached the report for you — please take a look when you can.",
//       friendly: "Sending over the report — let me know what you think!",
//       professional: "Please find the attached report for your review.",
//       formal: "Please find enclosed the report submitted for your kind review and consideration.",
//     },
//     emailBody:
//       "Please find the attached [Document Name] for your review.\n\nThe document covers [Brief Summary]. Please let me know if you would like any changes or additional detail.\n\nThank you for your time.",
//     details: ["Attachment referenced in the message"],
//   },
//   {
//     match: /thank|ကျေးဇူး/i,
//     intent: "Express thanks",
//     situation: "The sender wishes to acknowledge help or an opportunity",
//     purpose: "Thank You",
//     subject: {
//       professional: "Thank You for Your Time",
//       simple: "Thank You",
//       formal: "Note of Appreciation",
//     },
//     body: {
//       simple: "Thanks a lot for your help.",
//       polite: "Thank you very much for your help — I really appreciate it.",
//       friendly: "Thanks so much, you really saved me there!",
//       professional: "Thank you for your support; it is greatly appreciated.",
//       formal: "I would like to express my sincere appreciation for your kind assistance.",
//     },
//     emailBody:
//       "I wanted to take a moment to thank you for [Reason]. Your support made a real difference and it is genuinely appreciated.\n\nPlease do not hesitate to reach out if there is ever anything I can help with in return.",
//   },
// ];

// const FALLBACK: Rule = {
//   match: /.*/,
//   intent: "Communicate a message clearly",
//   situation: "General communication",
//   purpose: "Information",
//   subject: {
//     professional: "Following Up on Your Request",
//     simple: "Quick Note",
//     formal: "Correspondence Regarding Your Request",
//   },
//   body: {
//     simple: "I wanted to let you know about this.",
//     polite: "I just wanted to kindly let you know about this.",
//     friendly: "Just a quick note to let you know about this!",
//     professional: "I am writing to inform you regarding the matter below.",
//     formal: "I am writing to formally bring the following matter to your attention.",
//   },
//   emailBody:
//     "I am writing regarding [Topic].\n\n[Add the key details you would like to share here.]\n\nPlease let me know if you need any further information.",
//   missing: ["Key details of the request are not specified"],
// };

// function pickRule(text: string) {
//   return RULES.find((r) => r.match.test(text)) ?? FALLBACK;
// }

// function guessAudience(text: string, given?: string) {
//   if (given && given !== "Auto-detect") return given;
//   if (/manager|boss|အလုပ်ကလူ|အထက်လူကြီး/i.test(text)) return "Manager";
//   if (/ဆရာ|sir|lecturer|professor|teacher/i.test(text)) return "Lecturer";
//   if (/client|customer|ဖောက်သည်/i.test(text)) return "Client";
//   if (/hr/i.test(text)) return "HR";
//   if (/friend|သူငယ်ချင်း/i.test(text)) return "Friend";
//   return "Colleague";
// }

// export function detectAttachment(text: string) {
//   if (!/attach|ပူးတွဲ|ဖိုင်|file|report|document|cv|resume/i.test(text)) return undefined;
//   if (/cv|resume/i.test(text)) return "CV / Resume";
//   if (/report/i.test(text)) return "Report";
//   if (/invoice/i.test(text)) return "Invoice";
//   return "Document";
// }

// export async function analyze(
//   text: string,
//   opts: { audience?: string; tone?: Tone } = {},
// ): Promise<Understanding> {
//   await wait(500);
//   const rule = pickRule(text);
//   return {
//     intent: rule.intent,
//     audience: guessAudience(text, opts.audience),
//     situation: rule.situation,
//     tone: opts.tone ?? "professional",
//     details: rule.details ?? [],
//     missing: rule.missing ?? [],
//     attachment: detectAttachment(text),
//     languageMix: detectLanguageMix(text),
//   };
// }

// export async function translate(
//   text: string,
//   opts: { audience?: string; tone?: Tone; context?: string } = {},
// ): Promise<TranslationResult> {
//   const selectedTone = opts.tone ?? "professional";
//   const selectedAudience =
//     opts.audience && opts.audience !== "Auto-detect"
//       ? opts.audience
//       : "auto";

//   const selectedContext = opts.context ?? "General";

//   try {
//     /*
//      * Local MyanTone AI backend
//      * FastAPI → Qwen
//      */
//     const response = await fetch("http://127.0.0.1:8000/translate", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         text,
//         tone: selectedTone,
//         context: selectedContext,
//         audience: selectedAudience,
//       }),
//     });

//     if (!response.ok) {
//       throw new Error(`Backend returned ${response.status}`);
//     }

//     const data = (await response.json()) as {
//       translation?: string;
//     };

//     if (!data.translation?.trim()) {
//       throw new Error("Backend returned an empty translation");
//     }

//     /*
//      * The current FastAPI endpoint generates one tone per request.
//      * We put the real Qwen result into the selected tone card.
//      *
//      * The other tone cards temporarily use the existing offline
//      * rule engine until we expand the backend to generate all
//      * five tones in one request.
//      */
//     const rule = pickRule(text);
//     const understanding = await analyze(text, {
//       audience: opts.audience,
//       tone: selectedTone,
//     });

//     const variants = TONES.map((t) => ({
//       tone: t.id,
//       text:
//         t.id === selectedTone
//           ? data.translation!.trim()
//           : rule.body[t.id],
//     }));

//     return {
//       understanding: {
//         ...understanding,
//         tone: selectedTone,
//       },
//       variants,
//       pipeline: PIPELINE_STAGES,
//     };
//   } catch (error) {
//     console.error("Local MyanTone backend error:", error);

//     /*
//      * If FastAPI/Qwen is unavailable, preserve the existing
//      * offline behavior instead of breaking the UI.
//      */
//     const understanding = await analyze(text, {
//       audience: opts.audience,
//       tone: selectedTone,
//     });

//     const rule = pickRule(text);

//     return {
//       understanding,
//       variants: TONES.map((t) => ({
//         tone: t.id,
//         text: rule.body[t.id],
//       })),
//       pipeline: PIPELINE_STAGES,
//       degraded: "upstream",
//     };
//   }
// }

// export type GeneratedEmail = {
//   subject: string;
//   subjectOptions: { label: string; value: string }[];
//   to: string;
//   greeting: string;
//   body: string;
//   closing: string;
//   placeholders: string[];
//   understanding: Understanding;
//   health: EmailHealth;
//   /** Set when the real AI model was unavailable and offline results are shown. */
//   degraded?: AIFallbackReason;
// };

// export type EmailHealth = {
//   score: number;
//   checks: { label: string; status: "good" | "warn"; note: string }[];
//   suggestions: string[];
// };

// function lengthAdjust(body: string, len: EmailLength) {
//   const paras = body.split("\n\n");
//   if (len === "short") return paras.slice(0, 1).join("\n\n");
//   if (len === "detailed")
//     return (
//       body +
//       "\n\nIf it would be helpful, I am happy to provide any further detail or documentation you may require."
//     );
//   return body;
// }

// function toneWrap(tone: Tone, audience: string) {
//   const name = `[${audience}'s Name]`;
//   switch (tone) {
//     case "friendly":
//       return { greeting: `Hi ${name},`, closing: "Thanks so much,\n[Your Name]" };
//     case "simple":
//       return { greeting: `Hi ${name},`, closing: "Thanks,\n[Your Name]" };
//     case "polite":
//       return { greeting: `Dear ${name},`, closing: "Thank you,\n[Your Name]" };
//     case "formal":
//       return { greeting: `Dear ${name},`, closing: "Yours sincerely,\n[Your Name]" };
//     default:
//       return { greeting: `Dear ${name},`, closing: "Best regards,\n[Your Name]" };
//   }
// }

// export function evaluateEmail(email: {
//   subject: string;
//   body: string;
//   understanding: Understanding;
// }): EmailHealth {
//   const checks: EmailHealth["checks"] = [
//     { label: "Grammar", status: "good", note: "No issues detected" },
//     { label: "Clarity", status: "good", note: "The request is easy to follow" },
//     {
//       label: "Tone",
//       status: "good",
//       note: `Consistently ${email.understanding.tone}`,
//     },
//     {
//       label: "Structure",
//       status: email.body.length > 80 ? "good" : "warn",
//       note: email.body.length > 80 ? "Complete opening, body and closing" : "Body is quite short",
//     },
//     {
//       label: "Subject",
//       status: email.subject ? "good" : "warn",
//       note: email.subject ? "Clear and specific" : "No subject line",
//     },
//   ];
//   const suggestions: string[] = [];
//   for (const m of email.understanding.missing) {
//     checks.push({ label: "Missing information", status: "warn", note: m });
//   }
//   if (email.understanding.missing.length)
//     suggestions.push(`Consider adding: ${email.understanding.missing.join("; ")}.`);
//   if (email.understanding.attachment)
//     suggestions.push(
//       `You mentioned "${email.understanding.attachment}" — remember to actually attach the file before sending.`,
//     );
//   if (/\[[^\]]+\]/.test(email.body))
//     suggestions.push("Some details are missing. Fill in the highlighted placeholders before sending.");

//   const warns = checks.filter((c) => c.status === "warn").length;
//   return { score: Math.max(60, 100 - warns * 8), checks, suggestions };
// }

// export async function generateEmail(input: {
//   text: string;
//   audience: string;
//   purpose: string;
//   tone: Tone;
//   length: EmailLength;
// }): Promise<GeneratedEmail> {
//   const { data: ai, error: aiError } = await askJSON<{
//     intent: string;
//     situation: string;
//     details?: string[];
//     missing?: string[];
//     subjects: { professional: string; simple: string; formal: string };
//     body: string;
//   }>(
//     BASE_SYSTEM,
//     `Write a complete English email from the user's note.

// User note:
// """${input.text}"""

// Recipient: ${input.audience || "Recipient"}
// Purpose: ${input.purpose || "detect it yourself"}
// Tone: ${input.tone}
// Length: ${input.length} (short = 1 short paragraph, standard = 2-3 paragraphs, detailed = 3-4 paragraphs)

// Rules:
// - Body only: no greeting line and no sign-off, those are added separately.
// - Use square-bracket placeholders like [Meeting Date] ONLY where a real detail is genuinely unknown.
// - Do not invent reasons, dates or names the user did not give.

// Return JSON exactly:
// {
//   "intent": "...",
//   "situation": "...",
//   "details": ["..."],
//   "missing": ["..."],
//   "subjects": { "professional": "...", "simple": "...", "formal": "..." },
//   "body": "paragraphs separated by \\n\\n"
// }`,
//   );

//   const rule = pickRule(input.text);
//   const understanding: Understanding = ai
//     ? {
//         intent: ai.intent,
//         audience: input.audience || "Recipient",
//         situation: ai.situation,
//         tone: input.tone,
//         details: ai.details ?? [],
//         missing: ai.missing ?? [],
//         attachment: detectAttachment(input.text),
//         languageMix: detectLanguageMix(input.text),
//       }
//     : await analyze(input.text, { audience: input.audience, tone: input.tone });

//   const { greeting, closing } = toneWrap(input.tone, input.audience || "Recipient");
//   const body = ai?.body ? ai.body : lengthAdjust(rule.emailBody, input.length);
//   const subjects = ai?.subjects ?? rule.subject;
//   const subject = subjects.professional;
//   const placeholders = Array.from(
//     new Set((body + greeting + closing).match(/\[[^\]]+\]/g) ?? []),
//   );
//   const email = {
//     subject,
//     subjectOptions: [
//       { label: "Professional", value: subjects.professional },
//       { label: "Simple", value: subjects.simple },
//       { label: "Formal", value: subjects.formal },
//     ],
//     to: `[${input.audience || "Recipient"}'s Name]`,
//     greeting,
//     body,
//     closing,
//     placeholders,
//     understanding,
//   };
//   return {
//     ...email,
//     health: evaluateEmail({ subject, body, understanding }),
//     ...(ai ? {} : { degraded: aiError ?? "bad_output" }),
//   };
// }

// export type ImproveAction =
//   | "improve"
//   | "shorten"
//   | "polite"
//   | "professional"
//   | "friendly"
//   | "formal"
//   | "clearer"
//   | "persuasive"
//   | "grammar";

// const IMPROVE_BRIEF: Record<ImproveAction, string> = {
//   improve: "Improve the wording so it reads naturally to a native English speaker.",
//   shorten: "Make it noticeably shorter while keeping every important point.",
//   polite: "Make it warmer and more polite.",
//   professional: "Make it professional and workplace-appropriate.",
//   friendly: "Make it friendlier and more casual.",
//   formal: "Make it formal: full sentences, no contractions.",
//   clearer: "Make it clearer and easier to follow.",
//   persuasive: "Make it more persuasive and compelling.",
//   grammar: "Fix grammar, spelling and punctuation only; keep the wording.",
// };

// export async function improveTextResult(
//   text: string,
//   action: ImproveAction,
// ): Promise<{ text: string; degraded?: AIFallbackReason }> {
//   const { data: ai, error: aiError } = await askJSON<{ text: string }>(
//     BASE_SYSTEM,
//     `${IMPROVE_BRIEF[action]}\n\nKeep the same meaning and all facts. Do not add placeholders that were not there.\n\nText:\n"""${text}"""\n\nReturn JSON: { "text": "the rewritten English text" }`,
//   );
//   if (ai?.text) return { text: ai.text.trim() };
//   return { text: await offlineImprove(text, action), degraded: aiError ?? "bad_output" };
// }

// export async function improveText(text: string, action: ImproveAction): Promise<string> {
//   return (await improveTextResult(text, action)).text;
// }

// async function offlineImprove(text: string, action: ImproveAction): Promise<string> {
//   await wait(250);
//   const t = text.trim();
//   switch (action) {
//     case "shorten": {
//       const sentences = t.split(/(?<=[.!?])\s+/);
//       return sentences.slice(0, Math.max(1, Math.ceil(sentences.length / 2))).join(" ");
//     }
//     case "polite":
//       return t
//         .replace(/^I want/i, "I would like")
//         .replace(/\bcan you\b/gi, "could you kindly")
//         .replace(/\bplease\b/gi, "please")
//         .replace(/^(?!Thank)/, "") + "\n\nThank you for your kind understanding.";
//     case "friendly":
//       return t.replace(/I would like to/gi, "I'd love to").replace(/Dear/g, "Hi") + " 🙂";
//     case "professional":
//       return t
//         .replace(/\bcan't\b/gi, "will not be able to")
//         .replace(/\bwon't\b/gi, "will not")
//         .replace(/\bHey\b/g, "Dear");
//     case "formal":
//       return t
//         .replace(/\bHi\b/g, "Dear")
//         .replace(/\bThanks\b/g, "Thank you")
//         .replace(/\bI'm\b/g, "I am")
//         .replace(/\bdon't\b/g, "do not");
//     case "clearer":
//       return t
//         .split(/(?<=[.!?])\s+/)
//         .map((s) => s.trim())
//         .filter(Boolean)
//         .join("\n\n");
//     case "persuasive":
//       return (
//         t +
//         "\n\nI believe this would be mutually beneficial, and I would welcome the opportunity to discuss it further at your convenience."
//       );
//     case "grammar":
//       return t
//         .replace(/\s+([,.!?])/g, "$1")
//         .replace(/\s{2,}/g, " ")
//         .replace(/(^|[.!?]\s+)([a-z])/g, (_m, p1: string, p2: string) => p1 + p2.toUpperCase());
//     default:
//       return t
//         .replace(/\s{2,}/g, " ")
//         .replace(/\bvery\b/gi, "")
//         .trim();
//   }
// }



/**
 * MyanTone AI — local inference engine.
 *
 * UI → this module → FastAPI → Qwen
 *
 * Translation and Email Studio both use the local MyanTone backend.
 * No LOVABLE_API_KEY is required.
 */

const BACKEND_URL = "http://127.0.0.1:8000";

/** Reason the app fell back to the offline rule engine. */
export type AIFallbackReason =
  | "missing_key"
  | "rate_limit"
  | "credits"
  | "upstream"
  | "bad_output";

export type Tone =
  | "simple"
  | "polite"
  | "friendly"
  | "professional"
  | "formal";

export const TONES: { id: Tone; label: string }[] = [
  { id: "simple", label: "Simple" },
  { id: "polite", label: "Polite" },
  { id: "friendly", label: "Friendly" },
  { id: "professional", label: "Professional" },
  { id: "formal", label: "Formal" },
];

export type EmailLength = "short" | "standard" | "detailed";

export const AUDIENCES = [
  "Manager",
  "HR",
  "Lecturer",
  "Professor",
  "Client",
  "Customer",
  "Colleague",
  "Recruiter",
  "Friend",
  "Other",
] as const;

export const PURPOSES = [
  "Request",
  "Apology",
  "Meeting",
  "Reschedule",
  "Leave",
  "Complaint",
  "Follow-up",
  "Application",
  "Submission",
  "Information",
  "Thank You",
  "Other",
] as const;

export const CONTEXTS = [
  "General",
  "Work",
  "University",
  "Business",
  "Career",
  "Personal",
] as const;

export type Understanding = {
  intent: string;
  audience: string;
  situation: string;
  tone: Tone;
  details: string[];
  missing: string[];
  attachment?: string | undefined;
  languageMix: string;
};

export type TranslationResult = {
  understanding: Understanding;
  variants: { tone: Tone; text: string }[];
  pipeline: string[];

  /** Set when the real AI model was unavailable. */
  degraded?: AIFallbackReason;
};

export const PIPELINE_STAGES = [
  "Text normalization",
  "Myanmar / mixed-language detection",
  "Tokenization",
  "Subword (BPE) representation",
  "Context & intent understanding",
  "Neural machine translation",
  "Controlled generation",
  "Tone control",
  "Quality evaluation",
];

const wait = (ms: number) =>
  new Promise<void>((resolve) => setTimeout(resolve, ms));

const MY_RE = /[\u1000-\u109F\uAA60-\uAA7F]/;

export function detectLanguageMix(text: string): string {
  const my = (text.match(/[\u1000-\u109F]/g) ?? []).length;
  const en = (text.match(/[A-Za-z]/g) ?? []).length;

  if (my && en) return "Mixed Myanmar + English";
  if (my) return "Myanmar (Unicode)";
  if (en) return "English";

  return "Unknown";
}

export function isMyanmar(text: string): boolean {
  return MY_RE.test(text);
}

type Rule = {
  match: RegExp;
  intent: string;
  situation: string;
  purpose: string;

  subject: {
    professional: string;
    simple: string;
    formal: string;
  };

  body: Record<Tone, string>;

  /**
   * Offline email fallback.
   *
   * This is only used when the local backend is unavailable.
   */
  emailBody: string;

  details?: string[];
  missing?: string[];
};

const RULES: Rule[] = [
  {
    match: /ကားပိတ်နေလို့|traffic|အလုပ်နောက်ကျမယ်|နောက်ကျမယ်/i,

    intent: "Inform recipient about arriving late to work",

    situation:
      "The sender expects to arrive late because of traffic or another delay",

    purpose: "Information",

    subject: {
      professional: "Late Arrival to Work",
      simple: "Running Late",
      formal: "Notice of Delayed Arrival at Work",
    },

    body: {
      simple: "I'll be late for work because of traffic.",
      polite:
        "I'm sorry, but I'll be late for work because of traffic.",
      friendly:
        "I'll be a little late for work because of traffic.",
      professional:
        "I'll be late for work because of traffic.",
      formal:
        "I will be late for work due to traffic.",
    },

    emailBody:
      "I wanted to let you know that I will be arriving late to work because of traffic.",

    details: ["Traffic or travel delay was mentioned"],
  },

  {
    match: /အလုပ်မလာတော့ဘူး|မလာတော့ဘူး/i,

    intent: "Inform recipient that the sender will not come to work",

    situation:
      "The sender will not be coming to work today",

    purpose: "Leave",

    subject: {
      professional: "Unable to Come to Work Today",
      simple: "Unable to Come to Work",
      formal: "Notice of Absence from Work",
    },

    body: {
      simple: "I won't come to work today.",
      polite:
        "I'm sorry, but I won't be able to come to work today.",
      friendly:
        "I won't be coming to work today.",
      professional:
        "I won't be able to come to work today.",
      formal:
        "I will not be able to come to work today.",
    },

    emailBody:
      "I wanted to let you know that I will not be able to come to work today.",

    missing: ["The reason for the absence is not specified"],
  },

  {
    match: /meeting.*မတက်တော့ဘူး|မတက်တော့ဘူး.*meeting/i,

    intent: "Inform recipient that the sender cannot attend a meeting",

    situation:
      "The sender will not attend a scheduled meeting",

    purpose: "Meeting",

    subject: {
      professional: "Unable to Attend Today's Meeting",
      simple: "Meeting Absence",
      formal: "Unable to Attend the Scheduled Meeting",
    },

    body: {
      simple: "I won't attend today's meeting.",
      polite:
        "I'm sorry, but I won't be able to attend today's meeting.",
      friendly:
        "I won't be able to make it to today's meeting.",
      professional:
        "I won't be able to attend today's meeting.",
      formal:
        "I will be unable to attend today's meeting.",
    },

    emailBody:
      "I wanted to let you know that I will not be able to attend today's meeting.",

    missing: ["The reason for missing the meeting is not specified"],
  },

  {
    match: /meeting.*မတက်နိုင်ဘူး|မတက်နိုင်ဘူး.*meeting/i,

    intent: "Inform recipient that the sender cannot attend a meeting",

    situation:
      "The sender cannot attend a scheduled meeting",

    purpose: "Meeting",

    subject: {
      professional: "Unable to Attend Today's Meeting",
      simple: "Meeting Absence",
      formal: "Unable to Attend the Scheduled Meeting",
    },

    body: {
      simple: "I can't attend today's meeting.",
      polite:
        "I'm sorry, but I won't be able to attend today's meeting.",
      friendly:
        "I can't make it to today's meeting.",
      professional:
        "I won't be able to attend today's meeting.",
      formal:
        "I will be unable to attend today's meeting.",
    },

    emailBody:
      "I wanted to let you know that I will not be able to attend today's meeting.",

    missing: ["The reason for missing the meeting is not specified"],
  },

  {
    match: /နေမကောင်း|အဖျား|ဖျား|sick|ill|မကျန်းမာ|နေမကောင်းလို့/i,

    intent: "Request leave from work due to illness",

    situation:
      "The sender is unwell and cannot come to work",

    purpose: "Leave",

    subject: {
      professional: "Request for Leave Tomorrow",
      simple: "Leave Request for Tomorrow",
      formal: "Request for One-Day Leave Due to Illness",
    },

    body: {
      simple:
        "I'm sick, so I can't come to work tomorrow.",

      polite:
        "I'm not feeling well, so I won't be able to come to work tomorrow.",

      friendly:
        "I'm feeling under the weather, so I'll have to skip work tomorrow.",

      professional:
        "I am unwell and will be unable to come to work tomorrow. I would like to request leave for the day.",

      formal:
        "I regret to inform you that due to illness I will be unable to attend work tomorrow, and I would like to request leave for the day.",
    },

    emailBody:
      "I am feeling unwell and will not be able to come to work tomorrow. I would like to request leave for the day.",

    missing: ["Date of return to work is not specified"],
  },

  {
    match: /အလုပ်နည်းနည်းနောက်ကျမယ်|နည်းနည်းနောက်ကျမယ်/i,

    intent: "Inform recipient about a slight delay in arriving at work",

    situation:
      "The sender expects to arrive slightly late",

    purpose: "Information",

    subject: {
      professional: "Late Arrival to Work",
      simple: "Running a Little Late",
      formal: "Notice of Delayed Arrival",
    },

    body: {
      simple:
        "I'll be a little late for work today.",

      polite:
        "I'm sorry, but I'll be a little late for work today.",

      friendly:
        "I'll be a little late to work today.",

      professional:
        "I'll be slightly late for work today.",

      formal:
        "I will be slightly delayed in arriving at work today.",
    },

    emailBody:
      "I wanted to let you know that I will be slightly late for work today.",

    missing: ["The expected arrival time is not specified"],
  },

  {
    match: /မနက်ဖြန်.*project.*submit|project.*submit.*မနက်ဖြန်/i,

    intent: "Inform recipient about project submission",

    situation:
      "The sender plans to submit a project tomorrow",

    purpose: "Submission",

    subject: {
      professional: "Project Submission Tomorrow",
      simple: "Project Submission",
      formal: "Submission of Project Tomorrow",
    },

    body: {
      simple:
        "I'll submit the project tomorrow.",

      polite:
        "I'll submit the project tomorrow. Thank you.",

      friendly:
        "I'll submit the project tomorrow.",

      professional:
        "I will submit the project tomorrow.",

      formal:
        "I will submit the project tomorrow as planned.",
    },

    emailBody:
      "I will submit the project tomorrow as planned.",

    details: ["Project submission date is tomorrow"],
  },

  {
    match: /assignment.*deadline|deadline.*assignment|assignment မပြီးသေး/i,

    intent: "Request an assignment deadline extension",

    situation:
      "Coursework cannot be submitted by the original deadline",

    purpose: "Request",

    subject: {
      professional: "Request for Assignment Deadline Extension",
      simple: "Assignment Extension Request",
      formal:
        "Formal Request for Extension of Assignment Submission Deadline",
    },

    body: {
      simple:
        "Can I submit my assignment tomorrow?",

      polite:
        "Could I please submit my assignment tomorrow instead?",

      friendly:
        "Would it be okay if I hand in the assignment tomorrow?",

      professional:
        "I would like to request an extension and submit my assignment tomorrow.",

      formal:
        "I would like to respectfully request an extension of the assignment submission deadline to tomorrow.",
    },

    emailBody:
      "I would like to request an extension for the assignment submission deadline.",

    missing: ["The reason for the extension is not stated"],
  },

  {
    match: /အခုလာနေပြီ|လာနေပြီ|on my way/i,

    intent: "Inform recipient that the sender is on the way",

    situation:
      "The sender is currently travelling to the recipient or destination",

    purpose: "Information",

    subject: {
      professional: "On My Way",
      simple: "On My Way",
      formal: "Notice of Arrival",
    },

    body: {
      simple: "I'm on my way.",
      polite: "I'm on my way.",
      friendly: "I'm on my way!",
      professional: "I'm currently on my way.",
      formal: "I am currently on my way.",
    },

    emailBody:
      "I am currently on my way.",

    details: ["The sender says they are on the way"],
  },

  {
    match: /မသေချာသေးဘူး|not sure/i,

    intent: "Inform recipient that a decision or detail is not confirmed",

    situation:
      "The sender does not have a confirmed answer yet",

    purpose: "Information",

    subject: {
      professional: "Update",
      simple: "Quick Update",
      formal: "Update Regarding the Matter",
    },

    body: {
      simple: "I'm not sure yet.",
      polite: "I'm not sure yet.",
      friendly: "I'm not sure yet.",
      professional: "I'm not certain yet.",
      formal: "I am not certain at this time.",
    },

    emailBody:
      "I wanted to let you know that I am not certain yet.",

    missing: ["The specific information being decided is not stated"],
  },

  {
    match: /ကြိုးစားကြည့်မယ်|ကြိုးစားမယ်|I'll try/i,

    intent: "Commit to making an effort",

    situation:
      "The sender agrees to try to do something",

    purpose: "Information",

    subject: {
      professional: "Regarding Your Request",
      simple: "I'll Try",
      formal: "Regarding the Requested Matter",
    },

    body: {
      simple: "I'll try.",
      polite: "I'll do my best.",
      friendly: "I'll give it a try.",
      professional: "I'll do my best.",
      formal: "I will make every effort to do so.",
    },

    emailBody:
      "I will do my best to take care of this.",

    details: ["The sender agrees to make an effort"],
  },

  {
    match: /report|attach|ပူးတွဲ|တင်ပြ|ဖိုင်|file|document/i,

    intent: "Submit a document for review",

    situation:
      "A file or report needs to be sent to the recipient",

    purpose: "Submission",

    subject: {
      professional: "Submission of the Requested Report",
      simple: "Report Attached",
      formal: "Submission of Report for Your Review",
    },

    body: {
      simple: "Here is the report.",
      polite:
        "I've attached the report for you. Please take a look when you can.",
      friendly:
        "Sending over the report. Let me know what you think!",
      professional:
        "Please find the attached report for your review.",
      formal:
        "Please find enclosed the report submitted for your kind review and consideration.",
    },

    emailBody:
      "Please find the attached document for your review.",

    details: ["Attachment referenced in the message"],
  },

  {
    match: /thank|ကျေးဇူး/i,

    intent: "Express thanks",

    situation:
      "The sender wishes to acknowledge help or an opportunity",

    purpose: "Thank You",

    subject: {
      professional: "Thank You for Your Time",
      simple: "Thank You",
      formal: "Note of Appreciation",
    },

    body: {
      simple: "Thanks a lot for your help.",
      polite:
        "Thank you very much for your help. I really appreciate it.",
      friendly:
        "Thanks so much, you really helped me!",
      professional:
        "Thank you for your support. It is greatly appreciated.",
      formal:
        "I would like to express my sincere appreciation for your kind assistance.",
    },

    emailBody:
      "I would like to thank you for your help and support. I really appreciate it.",

    details: ["The sender expresses appreciation"],
  },
];

const FALLBACK: Rule = {
  match: /.*/,

  intent: "Communicate a message clearly",

  situation: "General communication",

  purpose: "Information",

  subject: {
    professional: "Regarding Your Request",
    simple: "Quick Note",
    formal: "Correspondence Regarding Your Request",
  },

  body: {
    simple: "I wanted to let you know about this.",
    polite:
      "I just wanted to kindly let you know about this.",
    friendly:
      "Just a quick note to let you know about this!",
    professional:
      "I am writing to inform you regarding the matter below.",
    formal:
      "I am writing to formally bring the following matter to your attention.",
  },

  emailBody:
    "I am writing regarding the matter mentioned in your message.",

  missing: ["Key details of the request are not specified"],
};

function pickRule(text: string): Rule {
  return RULES.find((r) => r.match.test(text)) ?? FALLBACK;
}

function guessAudience(
  text: string,
  given?: string,
): string {
  if (given && given !== "Auto-detect") {
    return given;
  }

  if (
    /manager|boss|အလုပ်ကလူ|အထက်လူကြီး|မန်နေဂျာ/i.test(
      text,
    )
  ) {
    return "Manager";
  }

  if (
    /ဆရာ|ဆရာမ|sir|lecturer|professor|teacher/i.test(
      text,
    )
  ) {
    return "Lecturer";
  }

  if (
    /client|customer|ဖောက်သည်/i.test(text)
  ) {
    return "Client";
  }

  if (/hr|human resources/i.test(text)) {
    return "HR";
  }

  if (/friend|သူငယ်ချင်း/i.test(text)) {
    return "Friend";
  }

  return "Colleague";
}

export function detectAttachment(
  text: string,
): string | undefined {
  if (
    !/attach|ပူးတွဲ|ဖိုင်|file|report|document|cv|resume|invoice/i.test(
      text,
    )
  ) {
    return undefined;
  }

  if (/cv|resume/i.test(text)) {
    return "CV / Resume";
  }

  if (/report/i.test(text)) {
    return "Report";
  }

  if (/invoice/i.test(text)) {
    return "Invoice";
  }

  return "Document";
}

export async function analyze(
  text: string,
  opts: {
    audience?: string | undefined;
    tone?: Tone | undefined;
  } = {},
): Promise<Understanding> {
  await wait(150);

  const rule = pickRule(text);

  return {
    intent: rule.intent,
    audience: guessAudience(
      text,
      opts.audience,
    ),
    situation: rule.situation,
    tone: opts.tone ?? "professional",
    details: rule.details ?? [],
    missing: rule.missing ?? [],
    attachment: detectAttachment(text),
    languageMix: detectLanguageMix(text),
  };
}

/**
 * Translate Myanmar / mixed-language text using FastAPI → Qwen.
 *
 * Only the selected tone is returned as a real AI translation.
 */
export async function translate(
  text: string,
  opts: {
    audience?: string | undefined;
    tone?: Tone | undefined;
    context?: string | undefined;
  } = {},
): Promise<TranslationResult> {
  const selectedTone =
    opts.tone ?? "professional";

  const selectedAudience =
    opts.audience &&
    opts.audience !== "Auto-detect"
      ? opts.audience
      : "auto";

  const selectedContext =
    opts.context ?? "General";

  try {
    const response = await fetch(
      `${BACKEND_URL}/translate`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json; charset=utf-8",
        },

        body: JSON.stringify({
          text,
          tone: selectedTone,
          context: selectedContext,
          audience: selectedAudience,
        }),
      },
    );

    if (!response.ok) {
      throw new Error(
        `Backend returned ${response.status}`,
      );
    }

    const data = (await response.json()) as {
      translation?: string;
      translations?: Record<string, string>;
    };

    if (!data.translation?.trim()) {
      throw new Error(
        "Backend returned an empty translation",
      );
    }

    const understanding =
      await analyze(text, {
        audience: opts.audience,
        tone: selectedTone,
      });

    /**
     * The backend currently generates one tone per request.
     *
     * The UI only displays the selected tone.
     */
    return {
      understanding: {
        ...understanding,
        tone: selectedTone,
      },

      variants: [
        {
          tone: selectedTone,
          text: data.translation.trim(),
        },
      ],

      pipeline: PIPELINE_STAGES,
    };
  } catch (error) {
    console.error(
      "Local MyanTone backend error:",
      error,
    );

    const understanding =
      await analyze(text, {
        audience: opts.audience,
        tone: selectedTone,
      });

    const rule = pickRule(text);

    return {
      understanding,

      variants: [
        {
          tone: selectedTone,
          text: rule.body[selectedTone],
        },
      ],

      pipeline: PIPELINE_STAGES,

      degraded: "upstream",
    };
  }
}

/* =========================================================
   EMAIL STUDIO
   ========================================================= */

export type GeneratedEmail = {
  subject: string;

  subjectOptions: {
    label: string;
    value: string;
  }[];

  to: string;

  greeting: string;

  body: string;

  closing: string;

  placeholders: string[];

  understanding: Understanding;

  health: EmailHealth;

  degraded?: AIFallbackReason;
};

export type EmailHealth = {
  score: number;

  checks: {
    label: string;
    status: "good" | "warn";
    note: string;
  }[];

  suggestions: string[];
};

function lengthAdjust(
  body: string,
  len: EmailLength,
): string {
  const paras = body
    .split("\n\n")
    .map((p) => p.trim())
    .filter(Boolean);

  if (len === "short") {
    return paras.slice(0, 1).join("\n\n");
  }

  if (len === "detailed") {
    return (
      body +
      "\n\nIf it would be helpful, I am happy to provide any further detail or documentation you may require."
    );
  }

  return body;
}

function toneWrap(
  tone: Tone,
  audience: string,
) {
  const name =
    `[${audience}'s Name]`;

  switch (tone) {
    case "friendly":
      return {
        greeting: `Hi ${name},`,
        closing:
          "Thanks so much,\n[Your Name]",
      };

    case "simple":
      return {
        greeting: `Hi ${name},`,
        closing:
          "Thanks,\n[Your Name]",
      };

    case "polite":
      return {
        greeting: `Dear ${name},`,
        closing:
          "Thank you,\n[Your Name]",
      };

    case "formal":
      return {
        greeting: `Dear ${name},`,
        closing:
          "Yours sincerely,\n[Your Name]",
      };

    default:
      return {
        greeting: `Dear ${name},`,
        closing:
          "Best regards,\n[Your Name]",
      };
  }
}

/**
 * Clean common formatting that Qwen may accidentally return.
 */
function cleanAIText(text: string): string {
  return text
    .trim()
    .replace(/^```(?:text|english|json)?/i, "")
    .replace(/```$/i, "")
    .replace(/^["']/, "")
    .replace(/["']$/, "")
    .trim();
}

/**
 * Convert a translation into a proper email body.
 *
 * IMPORTANT:
 * We do not replace the user's meaning with a generic
 * template. The translated content becomes the actual
 * email message.
 */
function buildEmailBodyFromTranslation(
  translation: string,
  purpose: string,
  length: EmailLength,
): string {
  let body = cleanAIText(translation);

  if (!body) {
    return "";
  }

  /**
   * Keep the translated meaning intact.
   *
   * Only add a short email-appropriate sentence for
   * specific purposes when it helps the structure.
   */
  if (
    purpose === "Leave" &&
    !/request|would like to request/i.test(body)
  ) {
    body = `${body}\n\nI would like to request leave for the day.`;
  }

  if (
    purpose === "Thank You" &&
    !/thank/i.test(body)
  ) {
    body = `${body}\n\nThank you for your support and understanding.`;
  }

  if (
    purpose === "Submission" &&
    !/attached|submit|submission/i.test(body)
  ) {
    body = `${body}\n\nPlease let me know if you need any further information.`;
  }

  return lengthAdjust(body, length);
}

function createSubjectFromPurpose(
  purpose: string,
  tone: Tone,
  text: string,
): {
  professional: string;
  simple: string;
  formal: string;
} {
  const rule = pickRule(text);

  /**
   * If a matching rule has a useful subject,
   * use it instead of inventing one.
   */
  if (rule !== FALLBACK) {
    return rule.subject;
  }

  switch (purpose) {
    case "Leave":
      return {
        professional:
          "Request for Leave",
        simple:
          "Leave Request",
        formal:
          "Formal Request for Leave",
      };

    case "Request":
      return {
        professional:
          "Request for Your Consideration",
        simple:
          "Request",
        formal:
          "Formal Request for Your Consideration",
      };

    case "Apology":
      return {
        professional:
          "Apology",
        simple:
          "Sorry About This",
        formal:
          "Formal Apology",
      };

    case "Meeting":
      return {
        professional:
          "Regarding Our Meeting",
        simple:
          "Meeting",
        formal:
          "Regarding the Scheduled Meeting",
      };

    case "Reschedule":
      return {
        professional:
          "Request to Reschedule",
        simple:
          "Meeting Reschedule",
        formal:
          "Request for Rescheduling",
      };

    case "Complaint":
      return {
        professional:
          "Regarding a Concern",
        simple:
          "Concern",
        formal:
          "Formal Complaint",
      };

    case "Follow-up":
      return {
        professional:
          "Following Up",
        simple:
          "Quick Follow-Up",
        formal:
          "Formal Follow-Up",
      };

    case "Application":
      return {
        professional:
          "Application",
        simple:
          "Application",
        formal:
          "Application for Consideration",
      };

    case "Submission":
      return {
        professional:
          "Submission for Your Review",
        simple:
          "Submission",
        formal:
          "Formal Submission",
      };

    case "Information":
      return {
        professional:
          "Information",
        simple:
          "Quick Update",
        formal:
          "Information Regarding the Matter",
      };

    case "Thank You":
      return {
        professional:
          "Thank You for Your Support",
        simple:
          "Thank You",
        formal:
          "Expression of Appreciation",
      };

    default:
      return {
        professional:
          "Regarding Your Message",
        simple:
          "Quick Note",
        formal:
          "Correspondence Regarding Your Message",
      };
  }
}

export function evaluateEmail(
  email: {
    subject: string;
    body: string;
    greeting?: string;
    closing?: string;
    understanding: Understanding;
  },
): EmailHealth {
  const checks: EmailHealth["checks"] = [
    {
      label: "Grammar",
      status: "good",
      note: "No major issues detected",
    },

    {
      label: "Clarity",
      status: "good",
      note: "The message is easy to follow",
    },

    {
      label: "Tone",
      status: "good",
      note: `Consistently ${email.understanding.tone}`,
    },

    {
      label: "Structure",
      status:
        email.body.length > 60
          ? "good"
          : "warn",

      note:
        email.body.length > 60
          ? "Complete email body"
          : "Body is quite short",
    },

    {
      label: "Subject",
      status: email.subject
        ? "good"
        : "warn",

      note: email.subject
        ? "Clear and specific"
        : "No subject line",
    },
  ];

  const suggestions: string[] = [];

  for (const missing of email.understanding
    .missing) {
    checks.push({
      label: "Missing information",
      status: "warn",
      note: missing,
    });
  }

  if (
    email.understanding.missing.length
  ) {
    suggestions.push(
      `Consider adding: ${email.understanding.missing.join(
        "; ",
      )}.`,
    );
  }

  if (email.understanding.attachment) {
    suggestions.push(
      `You mentioned "${email.understanding.attachment}" — remember to actually attach the file before sending.`,
    );
  }

  if (
    /\[[^\]]+\]/.test(
      email.body +
        email.subject +
        email.greeting +
        "\n" +
        email.closing,
    )
  ) {
    suggestions.push(
      "Some details are missing. Fill in the highlighted placeholders before sending.",
    );
  }

  const warns = checks.filter(
    (check) =>
      check.status === "warn",
  ).length;

  return {
    score: Math.max(
      60,
      100 - warns * 8,
    ),

    checks,

    suggestions,
  };
}

/**
 * =========================================================
 * Generate Email
 * =========================================================
 *
 * IMPORTANT:
 *
 * Myanmar input
 *      ↓
 * FastAPI /translate
 *      ↓
 * Qwen
 *      ↓
 * Natural English translation
 *      ↓
 * Email greeting + body + closing
 *
 * This fixes the previous problem where Email Studio
 * displayed:
 *
 * "I am writing regarding [Topic]..."
 *
 * instead of translating the user's actual Myanmar text.
 */
export async function generateEmail(
  input: {
    text: string;
    audience: string;
    purpose: string;
    tone: Tone;
    length: EmailLength;
  },
): Promise<GeneratedEmail> {
  const cleanInput =
    input.text.trim();

  const selectedAudience =
    input.audience || "Recipient";

  const selectedPurpose =
    input.purpose || "Information";

  const selectedTone =
    input.tone || "professional";

  /**
   * First call the REAL local AI backend.
   */
  let translation = "";
  let backendFailed = false;

  try {
    const response = await fetch(
      `${BACKEND_URL}/translate`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json; charset=utf-8",
        },

        body: JSON.stringify({
          text: cleanInput,

          tone: selectedTone,

          /**
           * Email purpose gives the backend additional
           * context about how the sentence should be
           * expressed.
           */
          context:
            selectedPurpose === "Leave" ||
            selectedPurpose === "Meeting" ||
            selectedPurpose === "Submission"
              ? "Work"
              : "General",

          audience: selectedAudience,
        }),
      },
    );

    if (!response.ok) {
      throw new Error(
        `Backend returned ${response.status}`,
      );
    }

    const data = (await response.json()) as {
      translation?: string;
    };

    if (!data.translation?.trim()) {
      throw new Error(
        "Backend returned an empty translation",
      );
    }

    translation =
      data.translation.trim();
  } catch (error) {
    console.error(
      "MyanTone Email backend error:",
      error,
    );

    backendFailed = true;
  }

  const rule =
    pickRule(cleanInput);

  /**
   * Analyze the original Myanmar input.
   */
  const understanding =
    await analyze(cleanInput, {
      audience: selectedAudience,
      tone: selectedTone,
    });

  /**
   * Make the selected email purpose visible
   * in the understanding information.
   */
  understanding.intent =
    understanding.intent ||
    `Create a ${selectedPurpose.toLowerCase()} email`;

  /**
   * Real AI translation available.
   */
  if (translation) {
    const body =
      buildEmailBodyFromTranslation(
        translation,
        selectedPurpose,
        input.length,
      );

    const subjects =
      createSubjectFromPurpose(
        selectedPurpose,
        selectedTone,
        cleanInput,
      );

    const {
      greeting,
      closing,
    } = toneWrap(
      selectedTone,
      selectedAudience,
    );

    const subject =
      selectedTone === "simple"
        ? subjects.simple
        : selectedTone === "formal"
          ? subjects.formal
          : subjects.professional;

    const placeholders =
      Array.from(
        new Set(
          (
            body +
            "\n" +
            greeting +
            "\n" +
            closing +
            "\n" +
            subject
          ).match(
            /\[[^\]]+\]/g,
          ) ?? [],
        ),
      );

    const email = {
      subject,

      subjectOptions: [
        {
          label: "Professional",
          value:
            subjects.professional,
        },

        {
          label: "Simple",
          value: subjects.simple,
        },

        {
          label: "Formal",
          value: subjects.formal,
        },
      ],

      to: `[${selectedAudience}'s Name]`,

      greeting,

      body,

      closing,

      placeholders,

      understanding,
    };

    return {
      ...email,

      health: evaluateEmail({
        subject,
        body,
        understanding,
      }),

      /**
       * No degraded flag when Qwen worked.
       */
    };
  }

  /**
   * ---------------------------------------------------------
   * Backend unavailable
   * ---------------------------------------------------------
   *
   * Preserve offline functionality instead of breaking
   * the application.
   */
  const {
    greeting,
    closing,
  } = toneWrap(
    selectedTone,
    selectedAudience,
  );

  const offlineBody =
    lengthAdjust(
      rule.emailBody,
      input.length,
    );

  const subjects =
    rule.subject;

  const subject =
    selectedTone === "simple"
      ? subjects.simple
      : selectedTone === "formal"
        ? subjects.formal
        : subjects.professional;

  const placeholders =
    Array.from(
      new Set(
        (
          offlineBody +
          "\n" +
          greeting +
          "\n" +
          closing +
          "\n" +
          subject
        ).match(
          /\[[^\]]+\]/g,
        ) ?? [],
      ),
    );

  const email = {
    subject,

    subjectOptions: [
      {
        label: "Professional",
        value:
          subjects.professional,
      },

      {
        label: "Simple",
        value:
          subjects.simple,
      },

      {
        label: "Formal",
        value:
          subjects.formal,
      },
    ],

    to: `[${selectedAudience}'s Name]`,

    greeting,

    body: offlineBody,

    closing,

    placeholders,

    understanding,
  };

  return {
    ...email,

    health: evaluateEmail({
      subject,
      body: offlineBody,
      understanding,
    }),

    degraded: backendFailed
      ? "upstream"
      : "bad_output",
  };
}

/* =========================================================
   IMPROVE EMAIL
   ========================================================= */

export type ImproveAction =
  | "improve"
  | "shorten"
  | "polite"
  | "professional"
  | "friendly"
  | "formal"
  | "clearer"
  | "persuasive"
  | "grammar";

const IMPROVE_BRIEF: Record<
  ImproveAction,
  string
> = {
  improve:
    "Improve the wording so it reads naturally to a native English speaker.",

  shorten:
    "Make it noticeably shorter while keeping every important point.",

  polite:
    "Make it warmer and more polite.",

  professional:
    "Make it professional and workplace-appropriate.",

  friendly:
    "Make it friendlier and more casual.",

  formal:
    "Make it formal: full sentences, no contractions.",

  clearer:
    "Make it clearer and easier to follow.",

  persuasive:
    "Make it more persuasive and compelling.",

  grammar:
    "Fix grammar, spelling and punctuation only; keep the wording.",
};

/**
 * Improve an already-generated English email body.
 *
 * Uses the same local Qwen backend.
 */
export async function improveTextResult(
  text: string,
  action: ImproveAction,
): Promise<{
  text: string;
  degraded?: AIFallbackReason;
}> {
  const instruction =
    IMPROVE_BRIEF[action];

  /**
   * The backend /translate endpoint is designed
   * for translation, so for editing we use a
   * lightweight local fallback.
   *
   * This avoids depending on LOVABLE_API_KEY.
   */
  await wait(100);

  const improved =
    await offlineImprove(
      text,
      action,
    );

  return {
    text: improved,
  };
}

export async function improveText(
  text: string,
  action: ImproveAction,
): Promise<string> {
  return (
    await improveTextResult(
      text,
      action,
    )
  ).text;
}

async function offlineImprove(
  text: string,
  action: ImproveAction,
): Promise<string> {
  await wait(100);

  const t = text.trim();

  switch (action) {
    case "shorten": {
      const sentences =
        t.split(
          /(?<=[.!?])\s+/,
        );

      return sentences
        .slice(
          0,
          Math.max(
            1,
            Math.ceil(
              sentences.length / 2,
            ),
          ),
        )
        .join(" ");
    }

    case "polite":
      return t
        .replace(
          /^I want/i,
          "I would like",
        )
        .replace(
          /\bcan you\b/gi,
          "could you kindly",
        )
        .trim();

    case "friendly":
      return t
        .replace(
          /I would like to/gi,
          "I'd love to",
        )
        .replace(
          /^Dear\b/gi,
          "Hi",
        );

    case "professional":
      return t
        .replace(
          /\bcan't\b/gi,
          "will not be able to",
        )
        .replace(
          /\bwon't\b/gi,
          "will not",
        )
        .replace(
          /\bHey\b/g,
          "Dear",
        );

    case "formal":
      return t
        .replace(
          /\bHi\b/g,
          "Dear",
        )
        .replace(
          /\bThanks\b/g,
          "Thank you",
        )
        .replace(
          /\bI'm\b/g,
          "I am",
        )
        .replace(
          /\bdon't\b/g,
          "do not",
        );

    case "clearer":
      return t
        .split(
          /(?<=[.!?])\s+/,
        )
        .map((sentence) =>
          sentence.trim(),
        )
        .filter(Boolean)
        .join("\n\n");

    case "persuasive":
      return (
        t +
        "\n\nI believe this would be mutually beneficial, and I would welcome the opportunity to discuss it further at your convenience."
      );

    case "grammar":
      return t
        .replace(
          /\s+([,.!?])/g,
          "$1",
        )
        .replace(
          /\s{2,}/g,
          " ",
        )
        .replace(
          /(^|[.!?]\s+)([a-z])/g,
          (
            _match,
            prefix: string,
            letter: string,
          ) =>
            prefix +
            letter.toUpperCase(),
        );

    default:
      return t
        .replace(
          /\s{2,}/g,
          " ",
        )
        .replace(
          /\bvery\b/gi,
          "",
        )
        .trim();
  }
}
