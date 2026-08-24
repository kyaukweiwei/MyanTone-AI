/**
 * MyanTone AI — mock inference engine.
 *
 * This module is the single boundary between the UI and "the model".
 * Every function is async and returns typed data, so swapping these
 * implementations for a real NMT/LLM API call (server function -> provider)
 * requires no changes in the components.
 */

export type Tone = "simple" | "polite" | "friendly" | "professional" | "formal";
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

export const CONTEXTS = ["General", "Work", "University", "Business", "Career", "Personal"] as const;

export type Understanding = {
  intent: string;
  audience: string;
  situation: string;
  tone: Tone;
  details: string[];
  missing: string[];
  attachment?: string;
  languageMix: string;
};

export type TranslationResult = {
  understanding: Understanding;
  variants: { tone: Tone; text: string }[];
  pipeline: string[];
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

const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));

const MY_RE = /[\u1000-\u109F\uAA60-\uAA7F]/;

export function detectLanguageMix(text: string) {
  const my = (text.match(/[\u1000-\u109F]/g) ?? []).length;
  const en = (text.match(/[A-Za-z]/g) ?? []).length;
  if (my && en) return "Mixed Myanmar + English";
  if (my) return "Myanmar (Unicode)";
  if (en) return "English";
  return "Unknown";
}

export function isMyanmar(text: string) {
  return MY_RE.test(text);
}

type Rule = {
  match: RegExp;
  intent: string;
  situation: string;
  purpose: string;
  subject: { professional: string; simple: string; formal: string };
  body: Record<Tone, string>;
  emailBody: string;
  details?: string[];
  missing?: string[];
};

const RULES: Rule[] = [
  {
    match: /meeting|မီးတင်း|အစည်းအဝေး/i,
    intent: "Unable to attend / reschedule a meeting",
    situation: "A scheduled meeting cannot be attended at the planned time",
    purpose: "Reschedule",
    subject: {
      professional: "Request to Reschedule Our Meeting",
      simple: "Meeting Reschedule",
      formal: "Request for Rescheduling of Scheduled Meeting",
    },
    body: {
      simple: "I can't attend today's meeting.",
      polite: "I'm sorry, but I won't be able to attend today's meeting.",
      friendly: "Hey, I won't be able to make it to today's meeting. Sorry about that!",
      professional: "I apologize, but I will be unable to attend today's meeting.",
      formal: "I regret to inform you that I will be unable to attend today's meeting.",
    },
    emailBody:
      "I am writing regarding our meeting scheduled for [Meeting Date]. Unfortunately, I will not be able to attend at the arranged time.\n\nWould it be possible to reschedule to [Proposed Date and Time]? I am happy to adjust to a slot that suits you best.\n\nI apologize for any inconvenience this may cause and appreciate your understanding.",
    missing: ["A specific alternative date and time is not suggested"],
  },
  {
    match: /assignment|deadline|extend|တာဝန်|စာမေးပွဲ/i,
    intent: "Request for an assignment deadline extension",
    situation: "Coursework cannot be submitted by the original deadline",
    purpose: "Request",
    subject: {
      professional: "Request for Assignment Deadline Extension",
      simple: "Assignment Extension Request",
      formal: "Formal Request for Extension of Assignment Submission Deadline",
    },
    body: {
      simple: "Can I submit my assignment tomorrow?",
      polite: "Could I please submit my assignment tomorrow instead?",
      friendly: "Would it be okay if I hand in the assignment tomorrow?",
      professional: "I would like to request an extension and submit my assignment tomorrow.",
      formal:
        "I would like to respectfully request an extension of the assignment submission deadline to tomorrow.",
    },
    emailBody:
      "I would like to kindly request an extension for the [Assignment Name] submission deadline. Due to [Reason], I have not been able to complete the work to the standard I would like.\n\nI would be very grateful if I could submit the assignment by [New Date].\n\nThank you for your consideration and understanding.",
    missing: ["The reason for the extension is not stated"],
  },
  {
    match: /ဖျား|အဖျား|sick|leave|ခွင့်/i,
    intent: "Request leave from work due to illness",
    situation: "The sender is unwell and cannot come to work",
    purpose: "Leave",
    subject: {
      professional: "Request for Leave Tomorrow",
      simple: "Leave Request for Tomorrow",
      formal: "Request for One-Day Leave Due to Illness",
    },
    body: {
      simple: "I'm sick, so I can't come to work tomorrow.",
      polite: "I'm not feeling well, so I won't be able to come to work tomorrow.",
      friendly: "I'm feeling under the weather, so I'll have to skip work tomorrow.",
      professional:
        "I am unwell and will be unable to come to work tomorrow. I would like to request leave for the day.",
      formal:
        "I regret to inform you that due to illness I will be unable to attend work tomorrow, and I would like to request leave for the day.",
    },
    emailBody:
      "I am writing to inform you that I will be unable to come to work tomorrow due to illness. I would like to kindly request leave for the day.\n\nI will ensure that any urgent matters are handed over to the team, and I will remain reachable by email if anything requires my attention.\n\nI apologize for any inconvenience and appreciate your understanding.",
    missing: ["Date of return to work is not specified"],
  },
  {
    match: /report|attach|ပူးတွဲ|တင်ပြ/i,
    intent: "Submit a document for review",
    situation: "A file or report needs to be sent to the recipient",
    purpose: "Submission",
    subject: {
      professional: "Submission of the Requested Report",
      simple: "Report Attached",
      formal: "Submission of Report for Your Review",
    },
    body: {
      simple: "Here is the report.",
      polite: "I've attached the report for you — please take a look when you can.",
      friendly: "Sending over the report — let me know what you think!",
      professional: "Please find the attached report for your review.",
      formal: "Please find enclosed the report submitted for your kind review and consideration.",
    },
    emailBody:
      "Please find the attached [Document Name] for your review.\n\nThe document covers [Brief Summary]. Please let me know if you would like any changes or additional detail.\n\nThank you for your time.",
    details: ["Attachment referenced in the message"],
  },
  {
    match: /thank|ကျေးဇူး/i,
    intent: "Express thanks",
    situation: "The sender wishes to acknowledge help or an opportunity",
    purpose: "Thank You",
    subject: {
      professional: "Thank You for Your Time",
      simple: "Thank You",
      formal: "Note of Appreciation",
    },
    body: {
      simple: "Thanks a lot for your help.",
      polite: "Thank you very much for your help — I really appreciate it.",
      friendly: "Thanks so much, you really saved me there!",
      professional: "Thank you for your support; it is greatly appreciated.",
      formal: "I would like to express my sincere appreciation for your kind assistance.",
    },
    emailBody:
      "I wanted to take a moment to thank you for [Reason]. Your support made a real difference and it is genuinely appreciated.\n\nPlease do not hesitate to reach out if there is ever anything I can help with in return.",
  },
];

const FALLBACK: Rule = {
  match: /.*/,
  intent: "Communicate a message clearly",
  situation: "General communication",
  purpose: "Information",
  subject: {
    professional: "Following Up on Your Request",
    simple: "Quick Note",
    formal: "Correspondence Regarding Your Request",
  },
  body: {
    simple: "I wanted to let you know about this.",
    polite: "I just wanted to kindly let you know about this.",
    friendly: "Just a quick note to let you know about this!",
    professional: "I am writing to inform you regarding the matter below.",
    formal: "I am writing to formally bring the following matter to your attention.",
  },
  emailBody:
    "I am writing regarding [Topic].\n\n[Add the key details you would like to share here.]\n\nPlease let me know if you need any further information.",
  missing: ["Key details of the request are not specified"],
};

function pickRule(text: string) {
  return RULES.find((r) => r.match.test(text)) ?? FALLBACK;
}

function guessAudience(text: string, given?: string) {
  if (given && given !== "Auto-detect") return given;
  if (/manager|boss|အလုပ်ကလူ|အထက်လူကြီး/i.test(text)) return "Manager";
  if (/ဆရာ|sir|lecturer|professor|teacher/i.test(text)) return "Lecturer";
  if (/client|customer|ဖောက်သည်/i.test(text)) return "Client";
  if (/hr/i.test(text)) return "HR";
  if (/friend|သူငယ်ချင်း/i.test(text)) return "Friend";
  return "Colleague";
}

export function detectAttachment(text: string) {
  if (!/attach|ပူးတွဲ|ဖိုင်|file|report|document|cv|resume/i.test(text)) return undefined;
  if (/cv|resume/i.test(text)) return "CV / Resume";
  if (/report/i.test(text)) return "Report";
  if (/invoice/i.test(text)) return "Invoice";
  return "Document";
}

export async function analyze(
  text: string,
  opts: { audience?: string; tone?: Tone } = {},
): Promise<Understanding> {
  await wait(500);
  const rule = pickRule(text);
  return {
    intent: rule.intent,
    audience: guessAudience(text, opts.audience),
    situation: rule.situation,
    tone: opts.tone ?? "professional",
    details: rule.details ?? [],
    missing: rule.missing ?? [],
    attachment: detectAttachment(text),
    languageMix: detectLanguageMix(text),
  };
}

export async function translate(
  text: string,
  opts: { audience?: string; tone?: Tone; context?: string } = {},
): Promise<TranslationResult> {
  const understanding = await analyze(text, opts);
  const rule = pickRule(text);
  await wait(400);
  return {
    understanding,
    variants: TONES.map((t) => ({ tone: t.id, text: rule.body[t.id] })),
    pipeline: PIPELINE_STAGES,
  };
}

export type GeneratedEmail = {
  subject: string;
  subjectOptions: { label: string; value: string }[];
  to: string;
  greeting: string;
  body: string;
  closing: string;
  placeholders: string[];
  understanding: Understanding;
  health: EmailHealth;
};

export type EmailHealth = {
  score: number;
  checks: { label: string; status: "good" | "warn"; note: string }[];
  suggestions: string[];
};

function lengthAdjust(body: string, len: EmailLength) {
  const paras = body.split("\n\n");
  if (len === "short") return paras.slice(0, 1).join("\n\n");
  if (len === "detailed")
    return (
      body +
      "\n\nIf it would be helpful, I am happy to provide any further detail or documentation you may require."
    );
  return body;
}

function toneWrap(tone: Tone, audience: string) {
  const name = `[${audience}'s Name]`;
  switch (tone) {
    case "friendly":
      return { greeting: `Hi ${name},`, closing: "Thanks so much,\n[Your Name]" };
    case "simple":
      return { greeting: `Hi ${name},`, closing: "Thanks,\n[Your Name]" };
    case "polite":
      return { greeting: `Dear ${name},`, closing: "Thank you,\n[Your Name]" };
    case "formal":
      return { greeting: `Dear ${name},`, closing: "Yours sincerely,\n[Your Name]" };
    default:
      return { greeting: `Dear ${name},`, closing: "Best regards,\n[Your Name]" };
  }
}

export function evaluateEmail(email: {
  subject: string;
  body: string;
  understanding: Understanding;
}): EmailHealth {
  const checks: EmailHealth["checks"] = [
    { label: "Grammar", status: "good", note: "No issues detected" },
    { label: "Clarity", status: "good", note: "The request is easy to follow" },
    {
      label: "Tone",
      status: "good",
      note: `Consistently ${email.understanding.tone}`,
    },
    {
      label: "Structure",
      status: email.body.length > 80 ? "good" : "warn",
      note: email.body.length > 80 ? "Complete opening, body and closing" : "Body is quite short",
    },
    {
      label: "Subject",
      status: email.subject ? "good" : "warn",
      note: email.subject ? "Clear and specific" : "No subject line",
    },
  ];
  const suggestions: string[] = [];
  for (const m of email.understanding.missing) {
    checks.push({ label: "Missing information", status: "warn", note: m });
  }
  if (email.understanding.missing.length)
    suggestions.push(`Consider adding: ${email.understanding.missing.join("; ")}.`);
  if (email.understanding.attachment)
    suggestions.push(
      `You mentioned "${email.understanding.attachment}" — remember to actually attach the file before sending.`,
    );
  if (/\[[^\]]+\]/.test(email.body))
    suggestions.push("Some details are missing. Fill in the highlighted placeholders before sending.");

  const warns = checks.filter((c) => c.status === "warn").length;
  return { score: Math.max(60, 100 - warns * 8), checks, suggestions };
}

export async function generateEmail(input: {
  text: string;
  audience: string;
  purpose: string;
  tone: Tone;
  length: EmailLength;
}): Promise<GeneratedEmail> {
  const understanding = await analyze(input.text, {
    audience: input.audience,
    tone: input.tone,
  });
  const rule = pickRule(input.text);
  await wait(500);
  const { greeting, closing } = toneWrap(input.tone, input.audience || "Recipient");
  const body = lengthAdjust(rule.emailBody, input.length);
  const subject = rule.subject.professional;
  const placeholders = Array.from(
    new Set((body + greeting + closing).match(/\[[^\]]+\]/g) ?? []),
  );
  const email = {
    subject,
    subjectOptions: [
      { label: "Professional", value: rule.subject.professional },
      { label: "Simple", value: rule.subject.simple },
      { label: "Formal", value: rule.subject.formal },
    ],
    to: `[${input.audience || "Recipient"}'s Name]`,
    greeting,
    body,
    closing,
    placeholders,
    understanding,
  };
  return { ...email, health: evaluateEmail({ subject, body, understanding }) };
}

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

export async function improveText(text: string, action: ImproveAction): Promise<string> {
  await wait(450);
  const t = text.trim();
  switch (action) {
    case "shorten": {
      const sentences = t.split(/(?<=[.!?])\s+/);
      return sentences.slice(0, Math.max(1, Math.ceil(sentences.length / 2))).join(" ");
    }
    case "polite":
      return t
        .replace(/^I want/i, "I would like")
        .replace(/\bcan you\b/gi, "could you kindly")
        .replace(/\bplease\b/gi, "please")
        .replace(/^(?!Thank)/, "") + "\n\nThank you for your kind understanding.";
    case "friendly":
      return t.replace(/I would like to/gi, "I'd love to").replace(/Dear/g, "Hi") + " 🙂";
    case "professional":
      return t
        .replace(/\bcan't\b/gi, "will not be able to")
        .replace(/\bwon't\b/gi, "will not")
        .replace(/\bHey\b/g, "Dear");
    case "formal":
      return t
        .replace(/\bHi\b/g, "Dear")
        .replace(/\bThanks\b/g, "Thank you")
        .replace(/\bI'm\b/g, "I am")
        .replace(/\bdon't\b/g, "do not");
    case "clearer":
      return t
        .split(/(?<=[.!?])\s+/)
        .map((s) => s.trim())
        .filter(Boolean)
        .join("\n\n");
    case "persuasive":
      return (
        t +
        "\n\nI believe this would be mutually beneficial, and I would welcome the opportunity to discuss it further at your convenience."
      );
    case "grammar":
      return t
        .replace(/\s+([,.!?])/g, "$1")
        .replace(/\s{2,}/g, " ")
        .replace(/(^|[.!?]\s+)([a-z])/g, (_m, p1: string, p2: string) => p1 + p2.toUpperCase());
    default:
      return t
        .replace(/\s{2,}/g, " ")
        .replace(/\bvery\b/gi, "")
        .trim();
  }
}
