import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("=" * 60)
print("Loading MyanTone AI")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32,
)

# Use CPU
model.to("cpu")
model.eval()

print("MyanTone AI model loaded.")
print("Device: CPU")
print("=" * 60)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="MyanTone AI API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# TONES
# ============================================================

TONES = [
    "simple",
    "polite",
    "friendly",
    "professional",
    "formal",
]


# ============================================================
# REQUEST / RESPONSE MODELS
# ============================================================

class TranslateRequest(BaseModel):
    text: str
    tone: str = "professional"
    context: str = "general"
    audience: str = "auto"


class TranslateResponse(BaseModel):
    translation: str
    translations: dict[str, str]


# ============================================================
# TRANSLATION FUNCTION
# ============================================================

def rule_based_translation(
    text: str,
    tone: str,
    context: str,
    audience: str,
):
    """
    Deterministic translation layer for common Myanmar sentences.
    Returns a translation string or None.
    """

    # Normalize whitespace only
    text = text.strip()

    print("=" * 50)
    print("RULE CHECK")
    print("INPUT:", repr(text))
    print("TONE:", tone)

    # ========================================================
    # 1. TRAFFIC + WORK + LATE
    # ========================================================

    if "ကားပိတ်နေလို့" in text and "အလုပ်နောက်ကျမယ်" in text:

        print("MATCH: TRAFFIC + WORK + LATE")

        translations = {
            "simple": "I'll be late for work because of traffic.",
            "polite": "I'm sorry, but I'll be late for work because of traffic.",
            "friendly": "I'll be a little late for work because of traffic.",
            "professional": "I'll be late for work because of traffic.",
            "formal": "I will be late for work due to traffic.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 2. WORK + NOT COME + တော့ဘူး
    # ========================================================

    if "အလုပ်မလာတော့ဘူး" in text:

        print("MATCH: WORK + NOT COME")

        translations = {
            "simple": "I won't come to work today.",
            "polite": "I'm sorry, but I won't be able to come to work today.",
            "friendly": "I won't be coming to work today.",
            "professional": "I won't be able to come to work today.",
            "formal": "I will not be able to come to work today.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 3. MEETING + NOT ATTEND
    # ========================================================

    if "meeting" in text.lower() and "မတက်တော့ဘူး" in text:

        print("MATCH: MEETING + NOT ATTEND")

        translations = {
            "simple": "I won't attend today's meeting.",
            "polite": "I'm sorry, but I won't be able to attend today's meeting.",
            "friendly": "I won't be able to make it to today's meeting.",
            "professional": "I won't be able to attend today's meeting.",
            "formal": "I will be unable to attend today's meeting.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 4. WORK + CANNOT COME
    # ========================================================

    if "အလုပ်မလာနိုင်ဘူး" in text:

        print("MATCH: WORK + CANNOT COME")

        translations = {
            "simple": "I can't come to work today.",
            "polite": "I'm sorry, but I can't come to work today.",
            "friendly": "I can't make it to work today.",
            "professional": "I won't be able to come to work today.",
            "formal": "I will be unable to come to work today.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 5. MEETING + CANNOT ATTEND
    # ========================================================

    if "meeting" in text.lower() and "မတက်နိုင်ဘူး" in text:

        print("MATCH: MEETING + CANNOT ATTEND")

        translations = {
            "simple": "I can't attend today's meeting.",
            "polite": "I'm sorry, but I won't be able to attend today's meeting.",
            "friendly": "I can't make it to today's meeting.",
            "professional": "I won't be able to attend today's meeting.",
            "formal": "I will be unable to attend today's meeting.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 6. SICK + SCHOOL
    # ========================================================

    if "နေမကောင်းလို့" in text and "ကျောင်းမတက်နိုင်ဘူး" in text:

        print("MATCH: SICK + SCHOOL")

        translations = {
            "simple": "I'm not feeling well, so I can't attend school today.",
            "polite": "I'm sorry, but I'm not feeling well, so I won't be able to attend school today.",
            "friendly": "I'm not feeling well, so I can't make it to school today.",
            "professional": "I'm not feeling well, so I won't be able to attend school today.",
            "formal": "As I am unwell, I will be unable to attend school today.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 7. WORK + A LITTLE LATE
    # ========================================================

    if "အလုပ်နည်းနည်းနောက်ကျမယ်" in text:

        print("MATCH: WORK + LITTLE LATE")

        translations = {
            "simple": "I'll be a little late for work today.",
            "polite": "I'm sorry, but I'll be a little late for work today.",
            "friendly": "I'll be a little late to work today.",
            "professional": "I'll be slightly late for work today.",
            "formal": "I will be slightly delayed in arriving at work today.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 8. PROJECT SUBMISSION
    # ========================================================

    if (
        "မနက်ဖြန်" in text
        and "project" in text.lower()
        and "submit လုပ်မယ်" in text
    ):

        print("MATCH: PROJECT SUBMISSION")

        translations = {
            "simple": "I'll submit the project tomorrow.",
            "polite": "I'll submit the project tomorrow.",
            "friendly": "I'll submit the project tomorrow.",
            "professional": "I'll submit the project tomorrow.",
            "formal": "I will submit the project tomorrow.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 9. ASSIGNMENT + DEADLINE
    # ========================================================

    if (
        "assignment မပြီးသေးလို့" in text
        and "deadline" in text.lower()
    ):

        print("MATCH: ASSIGNMENT + DEADLINE")

        translations = {
            "simple": "I haven't finished the assignment yet, so could you please extend the deadline?",
            "polite": "I haven't finished the assignment yet. Could you please extend the deadline?",
            "friendly": "I haven't finished the assignment yet. Could you give me a little more time?",
            "professional": "I haven't finished the assignment yet, so could you please extend the deadline?",
            "formal": "As I have not yet completed the assignment, I would appreciate an extension of the deadline.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 10. ON MY WAY
    # ========================================================

    if "အခုလာနေပြီ" in text:

        print("MATCH: ON MY WAY")

        translations = {
            "simple": "I'm on my way.",
            "polite": "I'm on my way.",
            "friendly": "I'm on my way!",
            "professional": "I'm on my way.",
            "formal": "I am currently on my way.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 11. NOT SURE
    # ========================================================

    if "မသေချာသေးဘူး" in text:

        print("MATCH: NOT SURE")

        translations = {
            "simple": "I'm not sure yet.",
            "polite": "I'm not sure yet.",
            "friendly": "I'm not sure yet.",
            "professional": "I'm not certain yet.",
            "formal": "I am not certain at this time.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # 12. TRY
    # ========================================================

    if "ကြိုးစားကြည့်မယ်" in text:

        print("MATCH: TRY")

        translations = {
            "simple": "I'll try.",
            "polite": "I'll do my best.",
            "friendly": "I'll give it a try.",
            "professional": "I'll do my best.",
            "formal": "I will make every effort to do so.",
        }

        return translations.get(
            tone,
            translations["professional"]
        )

    # ========================================================
    # NO MATCH
    # ========================================================

    print("NO RULE MATCH")
    return None

def generate_translation(
    text: str,
    tone: str,
    context: str,
    audience: str,
):

    system_prompt = """You are MyanTone AI.

Your task is ONLY to translate Myanmar or Myanmar-English mixed text into natural English.

IMPORTANT:

1. Preserve the exact meaning.
2. Do not invent information.
3. Do not answer the user.
4. Do not explain.
5. Do not summarize.
6. Return ONLY the English translation.
7. Preserve the subject, action, time, reason, and intention.
8. Myanmar-English mixed words such as meeting, work, project, email, assignment, deadline, etc. must be understood in the Myanmar sentence.
9. The requested tone changes STYLE only. It must NOT change the meaning.

TONE:

Simple:
Clear and direct everyday English.

Polite:
Respectful and courteous English.

Friendly:
Warm and conversational English.

Professional:
Clear and respectful workplace English.

Formal:
Polished and formal English.

IMPORTANT MEANING PATTERNS:

ဒီနေ့ meeting မတက်တော့ဘူး။
→ I won't attend today's meeting.

ဒီနေ့ အလုပ်မလာတော့ဘူး။
→ I won't come to work today.

ဒီနေ့ meeting မတက်နိုင်ဘူး။
→ I can't attend today's meeting.

ဒီနေ့ အလုပ်မလာနိုင်ဘူး။
→ I can't come to work today.

ဒီနေ့ အလုပ်မလာနိုင်ဘူးလို့ manager ကို ပြောချင်တယ်။
→ I want to tell my manager that I can't come to work today.

ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်။
→ I want to tell my colleague that I can't attend today's meeting.

ဒီနေ့ အလုပ်နည်းနည်းနောက်ကျမယ်။
→ I'll be a little late for work today.

ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။
→ I'll be late for work because of traffic.

မနက်ဖြန် အလုပ်သွားမယ်။
→ I'll go to work tomorrow.

မနေ့က အလုပ်မသွားဘူး။
→ I didn't go to work yesterday.

အခု အလုပ်လုပ်နေတယ်။
→ I'm working right now.

အခုထိ အလုပ်မပြီးသေးဘူး။
→ I haven't finished the work yet.

အလုပ်ပြီးသွားပြီ။
→ I've finished the work.

မနက်ဖြန် project ကို submit လုပ်မယ်။
→ I'll submit the project tomorrow.

assignment မပြီးသေးလို့ deadline နည်းနည်းတိုးပေးပါ။
→ I haven't finished the assignment yet, so could you please extend the deadline?

နေမကောင်းလို့ ဒီနေ့ ကျောင်းမတက်နိုင်ဘူး။
→ I'm not feeling well, so I can't attend school today.

ဒီနေ့ lecture နောက်ကျမယ်။
→ I'll be late for today's lecture.

မိုးရွာနေလို့ အပြင်မထွက်တော့ဘူး။
→ It's raining, so I'm not going out.

အခုလာနေပြီ။
→ I'm on my way.

မသေချာသေးဘူး။
→ I'm not sure yet.

ကြိုးစားကြည့်မယ်။
→ I'll try.

CRITICAL:

"မတက်" means "not attend/go to" an event such as a meeting, class, or lecture.

"မလာ" means "not come" to a place such as work, school, or home.

Do not confuse these actions.

"တော့ဘူး" commonly indicates that something will no longer happen / the speaker will not do it.

"နိုင်ဘူး" commonly indicates inability / cannot.

"ချင်တယ်" commonly indicates wanting to do something.

"မယ်" commonly indicates future intention/action.

"လို့" can introduce a reason or reported/intended statement depending on context.

Translate the user's actual message, not one of the examples.
"""


    user_prompt = f"""Translate this message into natural English.

Context: {context}
Audience: {audience}
Tone: {tone}

USER MESSAGE:
{text}

Return ONLY the translation.
"""


    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]


    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )


    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )


    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=False,
            repetition_penalty=1.05,
        )


    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]


    result = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()


    result = result.strip('"').strip("'").strip()

    return result

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "name": "MyanTone AI",
        "status": "running",
        "model": MODEL_NAME,
        "device": "CPU",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True,
        "device": "cpu",
    }


# ============================================================
# TRANSLATE ENDPOINT
# ============================================================

@app.post(
    "/translate",
    response_model=TranslateResponse,
)

def translate(request: TranslateRequest):

    if not request.text.strip():
        return TranslateResponse(
            translation="",
            translations={
                tone: ""
                for tone in TONES
            },
        )

    # ---------------------------------------------------------
    # 1. Try deterministic translation first
    # ---------------------------------------------------------
    rule_translation = rule_based_translation(
        text=request.text,
        tone=request.tone,
        context=request.context,
        audience=request.audience,
    )

    if rule_translation is not None:
        print("RULE MATCH:", request.text)
        print("RULE RESULT:", rule_translation)

    return TranslateResponse(
        translation=rule_translation,
        translations={
            request.tone: rule_translation,
        },
    )

    # ---------------------------------------------------------
    # 2. Fall back to Qwen for unknown sentences
    # ---------------------------------------------------------
    selected_translation = generate_translation(
        text=request.text,
        tone=request.tone,
        context=request.context,
        audience=request.audience,
    )

    if not selected_translation:
        selected_translation = "Sorry, I couldn't generate a translation for this message."

    return TranslateResponse(
    translation=selected_translation,
    translations={
        request.tone: selected_translation,
    },
)

