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
  t(
        "meeting-not-attending",
        "Work",
        "Can't Attend Meeting",
        "Tell your colleague that you cannot attend today's meeting.",
        "ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်။",
        "Colleague",
        "Meeting",
        "professional",
    ),

    t(
        "meeting-not-attend",
        "Work",
        "Won't Attend Meeting",
        "Let your team know that you will not attend today's meeting.",
        "ဒီနေ့ meeting မတက်တော့ဘူး။",
        "Colleague",
        "Meeting",
        "professional",
    ),

    t(
        "work-absence",
        "Work",
        "Can't Come to Work",
        "Tell your manager that you cannot come to work today.",
        "ဒီနေ့ အလုပ်မလာနိုင်ဘူးလို့ manager ကို ပြောချင်တယ်။",
        "Manager",
        "Leave",
        "professional",
    ),

    t(
        "work-not-coming",
        "Work",
        "Not Coming to Work",
        "Tell your manager that you will not come to work today.",
        "ဒီနေ့ အလုပ်မလာတော့ဘူး။",
        "Manager",
        "Leave",
        "professional",
    ),

    t(
        "late-because-traffic",
        "Work",
        "Late Because of Traffic",
        "Let your manager know that traffic will make you late.",
        "ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။",
        "Manager",
        "Late Arrival",
        "professional",
    ),

    t(
        "slightly-late",
        "Work",
        "Running a Little Late",
        "Tell your team that you will be slightly late for work.",
        "ဒီနေ့ အလုပ်နည်းနည်းနောက်ကျမယ်။",
        "Manager",
        "Late Arrival",
        "polite",
    ),

    t(
        "work-tomorrow",
        "Work",
        "Going to Work Tomorrow",
        "Tell someone that you will go to work tomorrow.",
        "မနက်ဖြန် အလုပ်သွားမယ်။",
        "Manager",
        "Information",
        "professional",
    ),

    t(
        "did-not-go-work",
        "Work",
        "Didn't Go to Work",
        "Explain that you did not go to work yesterday.",
        "မနေ့က အလုပ်မသွားဘူး။",
        "Manager",
        "Explanation",
        "polite",
    ),

    t(
        "currently-working",
        "Work",
        "Currently Working",
        "Let someone know that you are working right now.",
        "အခု အလုပ်လုပ်နေတယ်။",
        "Colleague",
        "Information",
        "professional",
    ),

    t(
        "work-not-finished",
        "Work",
        "Work Not Finished",
        "Explain that you have not finished the work yet.",
        "အခုထိ အလုပ်မပြီးသေးဘူး။",
        "Manager",
        "Status Update",
        "professional",
    ),

    t(
        "work-finished",
        "Work",
        "Work Completed",
        "Tell your manager that you have finished the work.",
        "အလုပ်ပြီးသွားပြီ။",
        "Manager",
        "Status Update",
        "professional",
    ),

    t(
        "project-submission",
        "University",
        "Project Submission",
        "Tell your lecturer or teammate that you will submit the project tomorrow.",
        "မနက်ဖြန် project ကို submit လုပ်မယ်။",
        "Lecturer",
        "Submission",
        "professional",
    ),

    t(
        "assignment-extension",
        "University",
        "Assignment Extension",
        "Ask for more time because your assignment is not finished.",
        "assignment မပြီးသေးလို့ deadline နည်းနည်းတိုးပေးပါ။",
        "Lecturer",
        "Request",
        "polite",
        "detailed",
    ),

    t(
        "school-absence",
        "University",
        "Unable to Attend School",
        "Explain that you cannot attend school because you are unwell.",
        "နေမကောင်းလို့ ဒီနေ့ ကျောင်းမတက်နိုင်ဘူး။",
        "Lecturer",
        "Absence",
        "polite",
    ),

    t(
        "late-for-lecture",
        "University",
        "Late for Lecture",
        "Tell your lecturer that you will be late for today's lecture.",
        "ဒီနေ့ lecture နောက်ကျမယ်။",
        "Lecturer",
        "Late Arrival",
        "polite",
    ),

    t(
        "on-my-way",
        "Career",
        "On My Way",
        "Let someone know that you are currently on your way.",
        "အခုလာနေပြီ။",
        "Recruiter",
        "Information",
        "professional",
    ),

    t(
        "not-sure",
        "Career",
        "Not Sure Yet",
        "Tell someone that you are not certain yet.",
        "မသေချာသေးဘူး။",
        "Recruiter",
        "Information",
        "professional",
    ),

    t(
        "will-try",
        "Career",
        "I'll Try",
        "Let someone know that you will make an effort.",
        "ကြိုးစားကြည့်မယ်။",
        "Manager",
        "Commitment",
        "professional",
    ),

    t(
        "business-meeting",
        "Business",
        "Meeting Attendance",
        "Communicate whether you can attend a business meeting.",
        "ဒီနေ့ meeting မတက်နိုင်ဘူး။",
        "Client",
        "Meeting",
        "formal",
    ),

    t(
        "business-late",
        "Business",
        "Business Meeting Delay",
        "Inform a client that you may be late because of traffic.",
        "ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။",
        "Client",
        "Delay",
        "formal",
    ),

    t(
        "project-update",
        "Business",
        "Project Update",
        "Give a short update about your project submission.",
        "မနက်ဖြန် project ကို submit လုပ်မယ်။",
        "Client",
        "Project Update",
        "professional",
    ),

    t(
        "deadline-extension-business",
        "Business",
        "Deadline Extension",
        "Request an extension because the assignment or task is unfinished.",
        "assignment မပြီးသေးလို့ deadline နည်းနည်းတိုးပေးပါ။",
        "Client",
        "Request",
        "formal",
        "detailed",
    ),

    t(
        "personal-apology",
        "Personal",
        "Can't Make It",
        "Politely tell someone that you cannot attend.",
        "ဒီနေ့ meeting မတက်နိုင်ဘူး။",
        "Friend",
        "Apology",
        "friendly",
    ),

    t(
        "on-my-way-personal",
        "Personal",
        "I'm On My Way",
        "Let a friend know that you are already coming.",
        "အခုလာနေပြီ။",
        "Friend",
        "Information",
        "friendly",
    ),

    t(
        "not-sure-personal",
        "Personal",
        "Not Sure Yet",
        "Tell a friend that you are still unsure.",
        "မသေချာသေးဘူး။",
        "Friend",
        "Information",
        "friendly",
    ),

    t(
        "personal-try",
        "Personal",
        "I'll Give It a Try",
        "Tell someone that you will try your best.",
        "ကြိုးစားကြည့်မယ်။",
        "Friend",
        "Commitment",
        "friendly",
    ),

    t(
        "personal-late",
        "Personal",
        "Running Late",
        "Tell someone that you will arrive a little late.",
        "ဒီနေ့ အလုပ်နည်းနည်းနောက်ကျမယ်။",
        "Friend",
        "Late Arrival",
        "friendly",
    ),
];
