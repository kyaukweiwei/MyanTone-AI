import type { EmailLength, Tone } from "./myantone-engine";

export type Template = {
  id: string;
  category: "Work" | "University" | "Career" | "Business" | "Personal";
  title: string;
  blurb: string;
  seed: string;
  audience: string;
  purpose: string;
  tone: Tone;
  length: EmailLength;
};

export const TEMPLATE_CATEGORIES = [
  "Work",
  "University",
  "Career",
  "Business",
  "Personal",
] as const;

const t = (
  id: string,
  category: Template["category"],
  title: string,
  blurb: string,
  seed: string,
  audience: string,
  purpose: string,
  tone: Tone = "professional",
  length: EmailLength = "standard",
): Template => ({ id, category, title, blurb, seed, audience, purpose, tone, length });

export const TEMPLATES: Template[] = [
  t("sick-leave", "Work", "Sick Leave", "Ask your manager for a day off due to illness.", "မနက်ဖြန် အဖျားရှိလို့ အလုပ်မလာနိုင်ဘူး။ Manager ကို ခွင့်တောင်းတဲ့ email ရေးချင်တယ်။", "Manager", "Leave"),
  t("meeting-request", "Work", "Meeting Request", "Propose a meeting with a clear agenda.", "အလုပ်ကိစ္စအတွက် meeting တစ်ခု ချိန်းချင်တယ်လို့ ပြောချင်တယ်", "Manager", "Meeting"),
  t("meeting-reschedule", "Work", "Meeting Reschedule", "Move a meeting to another time politely.", "မနက်ဖြန် meeting မလုပ်နိုင်လို့ next week ရွှေ့ချင်တယ်", "Client", "Reschedule"),
  t("late-arrival", "Work", "Late Arrival", "Let your team know you'll be late.", "မနက် traffic ကြောင့် အလုပ်နောက်ကျမယ်လို့ ပြောချင်တယ်", "Manager", "Apology", "polite"),
  t("wfh", "Work", "Work From Home", "Request to work remotely for a day.", "မနက်ဖြန် အိမ်ကနေ အလုပ်လုပ်ချင်လို့ ခွင့်တောင်းချင်တယ်", "Manager", "Request"),
  t("deadline-extension", "Work", "Deadline Extension", "Ask for more time on a work task.", "project deadline ကို extend လုပ်ပေးဖို့ တောင်းချင်တယ်", "Manager", "Request"),
  t("report-submission", "Work", "Report Submission", "Send a report for review.", "ဒီ report ကို attach လုပ်ပြီး manager ကို ပို့ချင်တယ်", "Manager", "Submission"),

  t("assignment-extension", "University", "Assignment Extension", "Request extra time from your lecturer.", "Sir ကို assignment deadline extend လုပ်ပေးဖို့ request email ရေးချင်တယ်", "Lecturer", "Request"),
  t("absence", "University", "Class Absence", "Explain why you missed a class.", "မနေ့က အတန်းမတက်နိုင်ခဲ့လို့ ဆရာ့ကို ရှင်းပြချင်တယ်", "Lecturer", "Apology", "polite"),
  t("lecturer-request", "University", "Lecturer Request", "Ask your lecturer for guidance.", "ဆရာ့ကို thesis အကြံဉာဏ်တောင်းချင်တယ်", "Lecturer", "Request"),
  t("internship-request", "University", "Internship Request", "Apply for an internship placement.", "company တစ်ခုမှာ internship လျှောက်ချင်တယ်", "HR", "Application"),
  t("recommendation", "University", "Recommendation Request", "Request a recommendation letter.", "Professor ကို recommendation letter တောင်းချင်တယ်", "Professor", "Request", "formal"),

  t("job-application", "Career", "Job Application", "Apply for an advertised role.", "ဒီ position အတွက် job application email ရေးချင်တယ်။ CV attach လုပ်မယ်", "Recruiter", "Application"),
  t("interview-confirm", "Career", "Interview Confirmation", "Confirm your interview slot.", "interview ချိန်းထားတာကို confirm လုပ်ချင်တယ်", "Recruiter", "Information"),
  t("interview-followup", "Career", "Interview Follow-up", "Follow up after an interview.", "interview ပြီးနောက် follow-up email ပို့ချင်တယ်", "Recruiter", "Follow-up"),
  t("recruiter-message", "Career", "Recruiter Message", "Reach out to a recruiter.", "recruiter ကို ကိုယ့်အကြောင်း မိတ်ဆက်ပြီး စာပို့ချင်တယ်", "Recruiter", "Information"),
  t("thank-you-career", "Career", "Thank You Email", "Thank someone after a meeting.", "အချိန်ပေးတဲ့အတွက် ကျေးဇူးတင်ကြောင်း email ပို့ချင်တယ်", "Colleague", "Thank You", "polite"),

  t("complaint", "Business", "Customer Complaint", "Raise an issue with a supplier.", "ဝန်ဆောင်မှု အဆင်မပြေလို့ complaint email ရေးချင်တယ်", "Customer", "Complaint", "formal"),
  t("quotation", "Business", "Quotation Request", "Ask a supplier for pricing.", "ဒီ product အတွက် quotation တောင်းချင်တယ်", "Client", "Request"),
  t("payment-reminder", "Business", "Payment Reminder", "Politely chase an unpaid invoice.", "invoice ငွေမရသေးလို့ သတိပေး email ပို့ချင်တယ်", "Client", "Follow-up"),
  t("invoice", "Business", "Invoice", "Send an invoice with details.", "invoice ကို attach လုပ်ပြီး client ကို ပို့ချင်တယ်", "Client", "Submission"),
  t("order-confirmation", "Business", "Order Confirmation", "Confirm an order with a customer.", "customer ရဲ့ order ကို confirm လုပ်ကြောင်း အကြောင်းကြားချင်တယ်", "Customer", "Information"),
  t("partnership", "Business", "Partnership Proposal", "Propose working together.", "partnership အတွက် အဆိုပြုချက် email ရေးချင်တယ်", "Client", "Request", "formal", "detailed"),

  t("apology", "Personal", "Apology", "Say sorry sincerely.", "အမှားတစ်ခုအတွက် တောင်းပန်ချင်တယ်", "Friend", "Apology", "polite"),
  t("invitation", "Personal", "Invitation", "Invite someone to an event.", "ပွဲတစ်ခုကို ဖိတ်ချင်တယ်", "Friend", "Information", "friendly"),
  t("thank-you", "Personal", "Thank You", "Thank a friend or colleague.", "ကူညီပေးတဲ့အတွက် ကျေးဇူးတင်ကြောင်း ပြောချင်တယ်", "Friend", "Thank You", "friendly"),
  t("personal-request", "Personal", "Request", "Ask someone for a favour.", "အကူအညီတစ်ခု တောင်းချင်တယ်", "Friend", "Request", "polite"),
];
