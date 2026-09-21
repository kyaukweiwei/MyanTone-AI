# import torch
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from transformers import AutoTokenizer, AutoModelForCausalLM


# # ============================================================
# # MODEL CONFIGURATION
# # ============================================================

# MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# print("=" * 60)
# print("Loading MyanTone AI")
# print("=" * 60)

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     dtype=torch.float32,
# )

# # Use CPU
# model.to("cpu")
# model.eval()

# print("MyanTone AI model loaded.")
# print("Device: CPU")
# print("=" * 60)


# # ============================================================
# # FASTAPI APP
# # ============================================================

# app = FastAPI(
#     title="MyanTone AI API",
#     version="1.0.0",
# )


# # ============================================================
# # CORS
# # ============================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#         "http://localhost:8080",
#         "http://127.0.0.1:8080",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ============================================================
# # TONES
# # ============================================================

# TONES = [
#     "simple",
#     "polite",
#     "friendly",
#     "professional",
#     "formal",
# ]


# # ============================================================
# # REQUEST / RESPONSE MODELS
# # ============================================================

# class TranslateRequest(BaseModel):
#     text: str
#     tone: str = "professional"
#     context: str = "general"
#     audience: str = "auto"


# class TranslateResponse(BaseModel):
#     translation: str
#     translations: dict[str, str]


# # ============================================================
# # TRANSLATION FUNCTION
# # ============================================================

# def rule_based_translation(
#     text: str,
#     tone: str,
#     context: str,
#     audience: str,
# ):
#     """
#     Deterministic translation layer for common Myanmar sentences.
#     Returns a translation string or None.
#     """

#     # Normalize whitespace only
#     text = text.strip()

#     print("=" * 50)
#     print("RULE CHECK")
#     print("INPUT:", repr(text))
#     print("TONE:", tone)

#     # ========================================================
#     # 1. TRAFFIC + WORK + LATE
#     # ========================================================

#     if "ကားပိတ်နေလို့" in text and "အလုပ်နောက်ကျမယ်" in text:

#         print("MATCH: TRAFFIC + WORK + LATE")

#         translations = {
#             "simple": "I'll be late for work because of traffic.",
#             "polite": "I'm sorry, but I'll be late for work because of traffic.",
#             "friendly": "I'll be a little late for work because of traffic.",
#             "professional": "I'll be late for work because of traffic.",
#             "formal": "I will be late for work due to traffic.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 2. WORK + NOT COME + တော့ဘူး
#     # ========================================================

#     if "အလုပ်မလာတော့ဘူး" in text:

#         print("MATCH: WORK + NOT COME")

#         translations = {
#             "simple": "I won't come to work today.",
#             "polite": "I'm sorry, but I won't be able to come to work today.",
#             "friendly": "I won't be coming to work today.",
#             "professional": "I won't be able to come to work today.",
#             "formal": "I will not be able to come to work today.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 3. MEETING + NOT ATTEND
#     # ========================================================

#     if "meeting" in text.lower() and "မတက်တော့ဘူး" in text:

#         print("MATCH: MEETING + NOT ATTEND")

#         translations = {
#             "simple": "I won't attend today's meeting.",
#             "polite": "I'm sorry, but I won't be able to attend today's meeting.",
#             "friendly": "I won't be able to make it to today's meeting.",
#             "professional": "I won't be able to attend today's meeting.",
#             "formal": "I will be unable to attend today's meeting.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 4. WORK + CANNOT COME
#     # ========================================================

#     if "အလုပ်မလာနိုင်ဘူး" in text:

#         print("MATCH: WORK + CANNOT COME")

#         translations = {
#             "simple": "I can't come to work today.",
#             "polite": "I'm sorry, but I can't come to work today.",
#             "friendly": "I can't make it to work today.",
#             "professional": "I won't be able to come to work today.",
#             "formal": "I will be unable to come to work today.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 5. MEETING + CANNOT ATTEND
#     # ========================================================

#     if "meeting" in text.lower() and "မတက်နိုင်ဘူး" in text:

#         print("MATCH: MEETING + CANNOT ATTEND")

#         translations = {
#             "simple": "I can't attend today's meeting.",
#             "polite": "I'm sorry, but I won't be able to attend today's meeting.",
#             "friendly": "I can't make it to today's meeting.",
#             "professional": "I won't be able to attend today's meeting.",
#             "formal": "I will be unable to attend today's meeting.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 6. SICK + SCHOOL
#     # ========================================================

#     if "နေမကောင်းလို့" in text and "ကျောင်းမတက်နိုင်ဘူး" in text:

#         print("MATCH: SICK + SCHOOL")

#         translations = {
#             "simple": "I'm not feeling well, so I can't attend school today.",
#             "polite": "I'm sorry, but I'm not feeling well, so I won't be able to attend school today.",
#             "friendly": "I'm not feeling well, so I can't make it to school today.",
#             "professional": "I'm not feeling well, so I won't be able to attend school today.",
#             "formal": "As I am unwell, I will be unable to attend school today.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 7. WORK + A LITTLE LATE
#     # ========================================================

#     if "အလုပ်နည်းနည်းနောက်ကျမယ်" in text:

#         print("MATCH: WORK + LITTLE LATE")

#         translations = {
#             "simple": "I'll be a little late for work today.",
#             "polite": "I'm sorry, but I'll be a little late for work today.",
#             "friendly": "I'll be a little late to work today.",
#             "professional": "I'll be slightly late for work today.",
#             "formal": "I will be slightly delayed in arriving at work today.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 8. PROJECT SUBMISSION
#     # ========================================================

#     if (
#         "မနက်ဖြန်" in text
#         and "project" in text.lower()
#         and "submit လုပ်မယ်" in text
#     ):

#         print("MATCH: PROJECT SUBMISSION")

#         translations = {
#             "simple": "I'll submit the project tomorrow.",
#             "polite": "I'll submit the project tomorrow.",
#             "friendly": "I'll submit the project tomorrow.",
#             "professional": "I'll submit the project tomorrow.",
#             "formal": "I will submit the project tomorrow.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 9. ASSIGNMENT + DEADLINE
#     # ========================================================

#     if (
#         "assignment မပြီးသေးလို့" in text
#         and "deadline" in text.lower()
#     ):

#         print("MATCH: ASSIGNMENT + DEADLINE")

#         translations = {
#             "simple": "I haven't finished the assignment yet, so could you please extend the deadline?",
#             "polite": "I haven't finished the assignment yet. Could you please extend the deadline?",
#             "friendly": "I haven't finished the assignment yet. Could you give me a little more time?",
#             "professional": "I haven't finished the assignment yet, so could you please extend the deadline?",
#             "formal": "As I have not yet completed the assignment, I would appreciate an extension of the deadline.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 10. ON MY WAY
#     # ========================================================

#     if "အခုလာနေပြီ" in text:

#         print("MATCH: ON MY WAY")

#         translations = {
#             "simple": "I'm on my way.",
#             "polite": "I'm on my way.",
#             "friendly": "I'm on my way!",
#             "professional": "I'm on my way.",
#             "formal": "I am currently on my way.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 11. NOT SURE
#     # ========================================================

#     if "မသေချာသေးဘူး" in text:

#         print("MATCH: NOT SURE")

#         translations = {
#             "simple": "I'm not sure yet.",
#             "polite": "I'm not sure yet.",
#             "friendly": "I'm not sure yet.",
#             "professional": "I'm not certain yet.",
#             "formal": "I am not certain at this time.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # 12. TRY
#     # ========================================================

#     if "ကြိုးစားကြည့်မယ်" in text:

#         print("MATCH: TRY")

#         translations = {
#             "simple": "I'll try.",
#             "polite": "I'll do my best.",
#             "friendly": "I'll give it a try.",
#             "professional": "I'll do my best.",
#             "formal": "I will make every effort to do so.",
#         }

#         return translations.get(
#             tone,
#             translations["professional"]
#         )

#     # ========================================================
#     # NO MATCH
#     # ========================================================

#     print("NO RULE MATCH")
#     return None

# def generate_translation(
#     text: str,
#     tone: str,
#     context: str,
#     audience: str,
# ):

#     system_prompt = """You are MyanTone AI.

# Your task is ONLY to translate Myanmar or Myanmar-English mixed text into natural English.

# IMPORTANT:

# 1. Preserve the exact meaning.
# 2. Do not invent information.
# 3. Do not answer the user.
# 4. Do not explain.
# 5. Do not summarize.
# 6. Return ONLY the English translation.
# 7. Preserve the subject, action, time, reason, and intention.
# 8. Myanmar-English mixed words such as meeting, work, project, email, assignment, deadline, etc. must be understood in the Myanmar sentence.
# 9. The requested tone changes STYLE only. It must NOT change the meaning.

# TONE:

# Simple:
# Clear and direct everyday English.

# Polite:
# Respectful and courteous English.

# Friendly:
# Warm and conversational English.

# Professional:
# Clear and respectful workplace English.

# Formal:
# Polished and formal English.

# IMPORTANT MEANING PATTERNS:

# ဒီနေ့ meeting မတက်တော့ဘူး။
# → I won't attend today's meeting.

# ဒီနေ့ အလုပ်မလာတော့ဘူး။
# → I won't come to work today.

# ဒီနေ့ meeting မတက်နိုင်ဘူး။
# → I can't attend today's meeting.

# ဒီနေ့ အလုပ်မလာနိုင်ဘူး။
# → I can't come to work today.

# ဒီနေ့ အလုပ်မလာနိုင်ဘူးလို့ manager ကို ပြောချင်တယ်။
# → I want to tell my manager that I can't come to work today.

# ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်။
# → I want to tell my colleague that I can't attend today's meeting.

# ဒီနေ့ အလုပ်နည်းနည်းနောက်ကျမယ်။
# → I'll be a little late for work today.

# ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။
# → I'll be late for work because of traffic.

# မနက်ဖြန် အလုပ်သွားမယ်။
# → I'll go to work tomorrow.

# မနေ့က အလုပ်မသွားဘူး။
# → I didn't go to work yesterday.

# အခု အလုပ်လုပ်နေတယ်။
# → I'm working right now.

# အခုထိ အလုပ်မပြီးသေးဘူး။
# → I haven't finished the work yet.

# အလုပ်ပြီးသွားပြီ။
# → I've finished the work.

# မနက်ဖြန် project ကို submit လုပ်မယ်။
# → I'll submit the project tomorrow.

# assignment မပြီးသေးလို့ deadline နည်းနည်းတိုးပေးပါ။
# → I haven't finished the assignment yet, so could you please extend the deadline?

# နေမကောင်းလို့ ဒီနေ့ ကျောင်းမတက်နိုင်ဘူး။
# → I'm not feeling well, so I can't attend school today.

# ဒီနေ့ lecture နောက်ကျမယ်။
# → I'll be late for today's lecture.

# မိုးရွာနေလို့ အပြင်မထွက်တော့ဘူး။
# → It's raining, so I'm not going out.

# အခုလာနေပြီ။
# → I'm on my way.

# မသေချာသေးဘူး။
# → I'm not sure yet.

# ကြိုးစားကြည့်မယ်။
# → I'll try.

# CRITICAL:

# "မတက်" means "not attend/go to" an event such as a meeting, class, or lecture.

# "မလာ" means "not come" to a place such as work, school, or home.

# Do not confuse these actions.

# "တော့ဘူး" commonly indicates that something will no longer happen / the speaker will not do it.

# "နိုင်ဘူး" commonly indicates inability / cannot.

# "ချင်တယ်" commonly indicates wanting to do something.

# "မယ်" commonly indicates future intention/action.

# "လို့" can introduce a reason or reported/intended statement depending on context.

# Translate the user's actual message, not one of the examples.
# """


#     user_prompt = f"""Translate this message into natural English.

# Context: {context}
# Audience: {audience}
# Tone: {tone}

# USER MESSAGE:
# {text}

# Return ONLY the translation.
# """


#     messages = [
#         {
#             "role": "system",
#             "content": system_prompt,
#         },
#         {
#             "role": "user",
#             "content": user_prompt,
#         },
#     ]


#     prompt = tokenizer.apply_chat_template(
#         messages,
#         tokenize=False,
#         add_generation_prompt=True,
#     )


#     inputs = tokenizer(
#         prompt,
#         return_tensors="pt",
#     )


#     with torch.no_grad():

#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=40,
#             do_sample=False,
#             repetition_penalty=1.05,
#         )


#     generated_tokens = outputs[0][
#         inputs["input_ids"].shape[1]:
#     ]


#     result = tokenizer.decode(
#         generated_tokens,
#         skip_special_tokens=True,
#     ).strip()


#     result = result.strip('"').strip("'").strip()

#     return result

# # ============================================================
# # ROOT ENDPOINT
# # ============================================================

# @app.get("/")
# def root():

#     return {
#         "name": "MyanTone AI",
#         "status": "running",
#         "model": MODEL_NAME,
#         "device": "CPU",
#     }


# # ============================================================
# # HEALTH CHECK
# # ============================================================

# @app.get("/health")
# def health():

#     return {
#         "status": "healthy",
#         "model_loaded": True,
#         "device": "cpu",
#     }


# # ============================================================
# # TRANSLATE ENDPOINT
# # ============================================================

# @app.post(
#     "/translate",
#     response_model=TranslateResponse,
# )

# def translate(request: TranslateRequest):

#     if not request.text.strip():
#         return TranslateResponse(
#             translation="",
#             translations={
#                 tone: ""
#                 for tone in TONES
#             },
#         )

#     # ---------------------------------------------------------
#     # 1. Try deterministic translation first
#     # ---------------------------------------------------------
#     rule_translation = rule_based_translation(
#         text=request.text,
#         tone=request.tone,
#         context=request.context,
#         audience=request.audience,
#     )

#     if rule_translation is not None:
#         print("RULE MATCH:", request.text)
#         print("RULE RESULT:", rule_translation)

#     return TranslateResponse(
#         translation=rule_translation,
#         translations={
#             request.tone: rule_translation,
#         },
#     )

#     # ---------------------------------------------------------
#     # 2. Fall back to Qwen for unknown sentences
#     # ---------------------------------------------------------
#     selected_translation = generate_translation(
#         text=request.text,
#         tone=request.tone,
#         context=request.context,
#         audience=request.audience,
#     )

#     if not selected_translation:
#         selected_translation = "Sorry, I couldn't generate a translation for this message."

#     return TranslateResponse(
#     translation=selected_translation,
#     translations={
#         request.tone: selected_translation,
#     },
# )



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re


# ============================================================
# MyanTone AI
# Myanmar → Natural English
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


# ============================================================
# Load Qwen model
# ============================================================

print("Loading MyanTone AI model...")
print(f"Model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32,
)

model.to("cpu")
model.eval()

print("Model loaded successfully.")
print("Device: CPU")


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="MyanTone AI API",
    description="Myanmar to natural English translation with tone control.",
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
# Tones
# ============================================================

TONES = [
    "simple",
    "polite",
    "friendly",
    "professional",
    "formal",
]


# ============================================================
# Request / Response Models
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
# 100 TRAINING / REFERENCE SENTENCES
#
# These examples are used as a deterministic reference layer.
# They also provide training-style examples for the project.
# ============================================================

TRAINING_EXAMPLES = [

    # ========================================================
    # WORK / OFFICE - 1 to 25
    # ========================================================

    {
        "input": "ဒီနေ့ အလုပ်နောက်ကျမယ်။",
        "simple": "I'll be late for work today.",
        "polite": "I'm sorry, but I'll be late for work today.",
        "friendly": "I'll be a little late for work today.",
        "professional": "I'll be slightly late for work today.",
        "formal": "I will be slightly delayed in arriving at work today.",
    },

    {
        "input": "ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။",
        "simple": "I'll be late for work because of traffic.",
        "polite": "I'm sorry, but I'll be late for work because of the traffic.",
        "friendly": "The traffic is bad, so I'll be a little late for work.",
        "professional": "I'll be slightly late for work due to traffic.",
        "formal": "I will be delayed in arriving at work due to traffic congestion.",
    },

    {
        "input": "ဒီနေ့ အလုပ်မလာနိုင်ဘူး။",
        "simple": "I can't come to work today.",
        "polite": "I'm sorry, but I can't come to work today.",
        "friendly": "I won't be able to make it to work today.",
        "professional": "I will be unable to come to work today.",
        "formal": "I regret to inform you that I will be unable to report to work today.",
    },

    {
        "input": "ဒီနေ့ အလုပ်မလာတော့ဘူး။",
        "simple": "I won't come to work today.",
        "polite": "I'm sorry, but I won't be coming to work today.",
        "friendly": "I won't be coming to work today.",
        "professional": "I will not be coming to work today.",
        "formal": "I would like to inform you that I will not be reporting to work today.",
    },

    {
        "input": "မနက်ဖြန် အလုပ်သွားမယ်။",
        "simple": "I'll go to work tomorrow.",
        "polite": "I'll be going to work tomorrow.",
        "friendly": "I'll be at work tomorrow.",
        "professional": "I will be at work tomorrow.",
        "formal": "I will report to work tomorrow.",
    },

    {
        "input": "အခု အလုပ်လုပ်နေတယ်။",
        "simple": "I'm working right now.",
        "polite": "I'm currently working on it.",
        "friendly": "I'm working on it right now.",
        "professional": "I'm currently working on the task.",
        "formal": "I am currently engaged in the assigned work.",
    },

    {
        "input": "အခုထိ အလုပ်မပြီးသေးဘူး။",
        "simple": "I haven't finished the work yet.",
        "polite": "I'm sorry, but I haven't finished the work yet.",
        "friendly": "I haven't finished it yet.",
        "professional": "The work is not completed yet.",
        "formal": "The assigned work has not yet been completed.",
    },

    {
        "input": "အလုပ်ပြီးသွားပြီ။",
        "simple": "The work is finished.",
        "polite": "I've finished the work.",
        "friendly": "It's all done.",
        "professional": "The work has been completed.",
        "formal": "The assigned work has been successfully completed.",
    },

    {
        "input": "အလုပ်နည်းနည်းနောက်ကျမယ်။",
        "simple": "I'll be a little late for work.",
        "polite": "I'm sorry, but I'll be a little late for work.",
        "friendly": "I'll be a bit late for work.",
        "professional": "I'll be slightly late for work.",
        "formal": "I will be slightly delayed in arriving at work.",
    },

    {
        "input": "ဒီနေ့ leave ယူချင်တယ်။",
        "simple": "I want to take leave today.",
        "polite": "I'd like to take leave today, if possible.",
        "friendly": "I'd like to take the day off today.",
        "professional": "I would like to request leave for today.",
        "formal": "I would like to formally request leave for today.",
    },

    {
        "input": "မနက်ဖြန် leave ယူမယ်။",
        "simple": "I'll take leave tomorrow.",
        "polite": "I'd like to take leave tomorrow.",
        "friendly": "I'll be taking the day off tomorrow.",
        "professional": "I will be taking leave tomorrow.",
        "formal": "I would like to inform you that I will be taking leave tomorrow.",
    },

    {
        "input": "ဒီ task ကို လုပ်နေတယ်။",
        "simple": "I'm working on this task.",
        "polite": "I'm currently working on this task.",
        "friendly": "I'm working on this task now.",
        "professional": "I'm currently working on this task.",
        "formal": "I am currently working on the assigned task.",
    },

    {
        "input": "ဒီ task ပြီးရင် ပို့ပေးမယ်။",
        "simple": "I'll send it when I finish this task.",
        "polite": "I'll send it once I finish this task.",
        "friendly": "I'll send it over when I'm done with this task.",
        "professional": "I will send it once this task is completed.",
        "formal": "I will forward it upon completion of this task.",
    },

    {
        "input": "အလုပ်ကိစ္စနည်းနည်းများနေတယ်။",
        "simple": "I have a lot of work right now.",
        "polite": "I have quite a bit of work to handle right now.",
        "friendly": "I've got a lot on my plate right now.",
        "professional": "I am currently handling a heavy workload.",
        "formal": "I am currently managing a substantial workload.",
    },

    {
        "input": "ဒီအလုပ်ကို အရင်လုပ်လိုက်မယ်။",
        "simple": "I'll do this work first.",
        "polite": "I'll take care of this first.",
        "friendly": "I'll get this done first.",
        "professional": "I'll prioritize this task first.",
        "formal": "I will prioritize this task before proceeding with the others.",
    },

    {
        "input": "အလုပ်အခြေအနေကို update ပေးမယ်။",
        "simple": "I'll give you an update on the work.",
        "polite": "I'll give you an update on the work shortly.",
        "friendly": "I'll keep you updated on the work.",
        "professional": "I will provide an update on the work.",
        "formal": "I will provide you with an update regarding the progress of the work.",
    },

    {
        "input": "ဒီအလုပ်ကို ဘယ်အချိန်ပြီးရမလဲ။",
        "simple": "When do I need to finish this work?",
        "polite": "When would you like me to finish this work?",
        "friendly": "When do you need this done?",
        "professional": "What is the deadline for this task?",
        "formal": "Could you please confirm the deadline for this task?",
    },

    {
        "input": "ဒီနေ့အတွင်းပြီးအောင်လုပ်မယ်။",
        "simple": "I'll finish it today.",
        "polite": "I'll make sure to finish it today.",
        "friendly": "I'll get it done today.",
        "professional": "I will complete it by the end of today.",
        "formal": "I will ensure that the task is completed by the end of today.",
    },

    {
        "input": "ဒီကိစ္စကို manager နဲ့ ပြောပြီးပြီ။",
        "simple": "I already talked to the manager about this.",
        "polite": "I've already discussed this with the manager.",
        "friendly": "I already talked to the manager about it.",
        "professional": "I have already discussed this matter with the manager.",
        "formal": "I have already discussed this matter with the manager.",
    },

    {
        "input": "manager ကို ပြောပေးပါ။",
        "simple": "Please tell the manager.",
        "polite": "Could you please let the manager know?",
        "friendly": "Can you let the manager know?",
        "professional": "Please inform the manager.",
        "formal": "I would appreciate it if you could inform the manager.",
    },

    {
        "input": "ဒီ file ကို ပြန်ပို့ပေးပါ။",
        "simple": "Please send this file again.",
        "polite": "Could you please resend this file?",
        "friendly": "Can you send this file again?",
        "professional": "Please resend the file.",
        "formal": "Could you kindly resend the requested file?",
    },

    {
        "input": "file ကို attach လုပ်ထားတယ်။",
        "simple": "I attached the file.",
        "polite": "I've attached the file for you.",
        "friendly": "I've attached the file here.",
        "professional": "The file has been attached for your review.",
        "formal": "Please find the requested file attached.",
    },

    {
        "input": "ဒီကိစ္စကို နောက်မှပြောမယ်။",
        "simple": "I'll talk about this later.",
        "polite": "I'll discuss this with you later.",
        "friendly": "Let's talk about this later.",
        "professional": "I'll discuss this matter with you later.",
        "formal": "I would like to discuss this matter at a later time.",
    },

    {
        "input": "အလုပ်မှာ ပြဿနာတစ်ခုရှိတယ်။",
        "simple": "There's a problem at work.",
        "polite": "There's an issue at work that I'd like to discuss.",
        "friendly": "There's a small problem at work.",
        "professional": "There is an issue that needs to be addressed at work.",
        "formal": "There is an issue at work that requires attention.",
    },

    {
        "input": "ဒီကိစ္စကို ကူညီပေးပါ။",
        "simple": "Please help me with this.",
        "polite": "Could you please help me with this?",
        "friendly": "Can you help me with this?",
        "professional": "Could you please assist me with this matter?",
        "formal": "I would appreciate your assistance with this matter.",
    },


    # ========================================================
    # UNIVERSITY / SCHOOL - 26 to 45
    # ========================================================

    {
        "input": "နေမကောင်းလို့ ဒီနေ့ ကျောင်းမတက်နိုင်ဘူး။",
        "simple": "I'm sick, so I can't attend school today.",
        "polite": "I'm sorry, but I'm not feeling well and can't attend school today.",
        "friendly": "I'm not feeling well, so I can't make it to school today.",
        "professional": "I am unwell and will be unable to attend school today.",
        "formal": "I regret to inform you that I am unwell and unable to attend school today.",
    },

    {
        "input": "ဒီနေ့ lecture နောက်ကျမယ်။",
        "simple": "I'll be late for the lecture today.",
        "polite": "I'm sorry, but I'll be late for today's lecture.",
        "friendly": "I'll be a little late for the lecture today.",
        "professional": "I will be slightly late for today's lecture.",
        "formal": "I will be delayed in attending today's lecture.",
    },

    {
        "input": "ဒီနေ့ class မတက်နိုင်ဘူး။",
        "simple": "I can't attend class today.",
        "polite": "I'm sorry, but I can't attend class today.",
        "friendly": "I won't be able to make it to class today.",
        "professional": "I will be unable to attend today's class.",
        "formal": "I regret to inform you that I will be unable to attend today's class.",
    },

    {
        "input": "assignment မပြီးသေးဘူး။",
        "simple": "I haven't finished the assignment yet.",
        "polite": "I'm sorry, but I haven't finished the assignment yet.",
        "friendly": "I haven't finished the assignment yet.",
        "professional": "The assignment is not completed yet.",
        "formal": "The assignment has not yet been completed.",
    },

    {
        "input": "assignment မပြီးသေးလို့ deadline တိုးပေးပါ။",
        "simple": "Please extend the deadline because I haven't finished the assignment.",
        "polite": "Could you please extend the deadline because I haven't finished the assignment yet?",
        "friendly": "Could you give me a little more time to finish the assignment?",
        "professional": "Could you please extend the deadline as I have not yet completed the assignment?",
        "formal": "I would respectfully request an extension of the assignment deadline.",
    },

    {
        "input": "မနက်ဖြန် assignment submit လုပ်မယ်။",
        "simple": "I'll submit the assignment tomorrow.",
        "polite": "I will submit the assignment tomorrow.",
        "friendly": "I'll submit the assignment tomorrow.",
        "professional": "I will submit the assignment by tomorrow.",
        "formal": "I will submit the completed assignment tomorrow.",
    },

    {
        "input": "ဒီနေ့ exam ရှိတယ်။",
        "simple": "I have an exam today.",
        "polite": "I have an exam today.",
        "friendly": "I've got an exam today.",
        "professional": "I have an examination scheduled for today.",
        "formal": "I am scheduled to take an examination today.",
    },

    {
        "input": "exam အတွက် စာလေ့လာနေတယ်။",
        "simple": "I'm studying for the exam.",
        "polite": "I'm currently studying for the exam.",
        "friendly": "I'm studying for my exam right now.",
        "professional": "I am currently preparing for the examination.",
        "formal": "I am currently preparing for the upcoming examination.",
    },

    {
        "input": "project အတွက် team member တွေနဲ့ ဆွေးနွေးနေတယ်။",
        "simple": "I'm discussing the project with my team members.",
        "polite": "I'm currently discussing the project with my team members.",
        "friendly": "I'm talking about the project with my team.",
        "professional": "I am discussing the project with the team.",
        "formal": "I am currently coordinating with my team members regarding the project.",
    },

    {
        "input": "presentation မနက်ဖြန်လုပ်ရမယ်။",
        "simple": "I have to give a presentation tomorrow.",
        "polite": "I have to give a presentation tomorrow.",
        "friendly": "I've got a presentation tomorrow.",
        "professional": "I am scheduled to give a presentation tomorrow.",
        "formal": "I am scheduled to deliver a presentation tomorrow.",
    },

    {
        "input": "presentation အတွက် ပြင်ဆင်နေတယ်။",
        "simple": "I'm preparing for the presentation.",
        "polite": "I'm currently preparing for the presentation.",
        "friendly": "I'm getting ready for the presentation.",
        "professional": "I am currently preparing the presentation.",
        "formal": "I am currently making preparations for the presentation.",
    },

    {
        "input": "ဆရာကို မေးချင်တာရှိတယ်။",
        "simple": "I want to ask the teacher something.",
        "polite": "I'd like to ask the teacher something.",
        "friendly": "I want to ask the teacher something.",
        "professional": "I would like to ask the instructor a question.",
        "formal": "I would like to ask the instructor for clarification regarding a matter.",
    },

    {
        "input": "ဒီ lesson ကို နားမလည်ဘူး။",
        "simple": "I don't understand this lesson.",
        "polite": "I'm having trouble understanding this lesson.",
        "friendly": "I don't really understand this lesson.",
        "professional": "I am having difficulty understanding this lesson.",
        "formal": "I am having difficulty understanding the material covered in this lesson.",
    },

    {
        "input": "နောက်တစ်ခါ ပြန်ရှင်းပြပေးပါ။",
        "simple": "Please explain it again.",
        "polite": "Could you please explain it again?",
        "friendly": "Can you explain it one more time?",
        "professional": "Could you please explain the concept again?",
        "formal": "I would appreciate it if you could explain the concept once again.",
    },

    {
        "input": "ဒီနေ့ university မသွားနိုင်ဘူး။",
        "simple": "I can't go to university today.",
        "polite": "I'm sorry, but I can't go to university today.",
        "friendly": "I won't be able to make it to university today.",
        "professional": "I will be unable to attend university today.",
        "formal": "I regret to inform you that I will be unable to attend university today.",
    },

    {
        "input": "group project အတွက် meeting လုပ်မယ်။",
        "simple": "We'll have a meeting for the group project.",
        "polite": "We'll have a meeting to discuss the group project.",
        "friendly": "We're going to have a meeting for the group project.",
        "professional": "We will hold a meeting to discuss the group project.",
        "formal": "We will conduct a meeting regarding the group project.",
    },

    {
        "input": "project ကို မနက်ဖြန် submit လုပ်မယ်။",
        "simple": "I'll submit the project tomorrow.",
        "polite": "I'll submit the project tomorrow.",
        "friendly": "I'll get the project submitted tomorrow.",
        "professional": "I will submit the project by tomorrow.",
        "formal": "I will submit the completed project tomorrow.",
    },

    {
        "input": "စာမေးပွဲ result ဘယ်တော့ထွက်မလဲ။",
        "simple": "When will the exam results come out?",
        "polite": "Could you please let me know when the exam results will be released?",
        "friendly": "Do you know when the exam results will be out?",
        "professional": "Could you please confirm when the examination results will be released?",
        "formal": "I would appreciate information regarding the release date of the examination results.",
    },

    {
        "input": "ဒီနေ့ class ရှိမရှိ မသေချာဘူး။",
        "simple": "I'm not sure if there's class today.",
        "polite": "I'm not sure whether we have class today.",
        "friendly": "I'm not sure if we have class today.",
        "professional": "I'm unsure whether today's class is scheduled.",
        "formal": "I would like to confirm whether a class is scheduled for today.",
    },

    {
        "input": "notes တွေ ပို့ပေးပါ။",
        "simple": "Please send me the notes.",
        "polite": "Could you please send me the notes?",
        "friendly": "Can you send me the notes?",
        "professional": "Could you please share the lecture notes with me?",
        "formal": "I would appreciate it if you could provide me with the lecture notes.",
    },


    # ========================================================
    # MEETINGS - 46 to 55
    # ========================================================

    {
        "input": "ဒီနေ့ meeting မတက်နိုင်ဘူး။",
        "simple": "I can't attend today's meeting.",
        "polite": "I'm sorry, but I won't be able to attend today's meeting.",
        "friendly": "I won't be able to make it to today's meeting.",
        "professional": "I will be unable to attend today's meeting.",
        "formal": "I regret to inform you that I will be unable to attend today's meeting.",
    },

    {
        "input": "ဒီနေ့ meeting မတက်တော့ဘူး။",
        "simple": "I won't attend today's meeting.",
        "polite": "I'm sorry, but I won't be attending today's meeting.",
        "friendly": "I won't be joining today's meeting.",
        "professional": "I will not be attending today's meeting.",
        "formal": "I would like to inform you that I will not be attending today's meeting.",
    },

    {
        "input": "meeting ကို နောက်တစ်ချိန်ရွှေ့လို့ရမလား။",
        "simple": "Can we move the meeting to another time?",
        "polite": "Could we please move the meeting to another time?",
        "friendly": "Can we reschedule the meeting?",
        "professional": "Could we reschedule the meeting to a different time?",
        "formal": "Would it be possible to reschedule the meeting for another time?",
    },

    {
        "input": "meeting ဘယ်အချိန်စမလဲ။",
        "simple": "What time does the meeting start?",
        "polite": "Could you please let me know what time the meeting starts?",
        "friendly": "What time does the meeting start?",
        "professional": "Could you please confirm the meeting start time?",
        "formal": "I would appreciate confirmation of the scheduled meeting time.",
    },

    {
        "input": "meeting link ပို့ပေးပါ။",
        "simple": "Please send me the meeting link.",
        "polite": "Could you please send me the meeting link?",
        "friendly": "Can you send me the meeting link?",
        "professional": "Please share the meeting link with me.",
        "formal": "I would appreciate it if you could provide the meeting link.",
    },

    {
        "input": "meeting အတွက် ပြင်ဆင်နေတယ်။",
        "simple": "I'm preparing for the meeting.",
        "polite": "I'm currently preparing for the meeting.",
        "friendly": "I'm getting ready for the meeting.",
        "professional": "I am currently preparing for the meeting.",
        "formal": "I am currently making preparations for the scheduled meeting.",
    },

    {
        "input": "meeting ပြီးသွားပြီ။",
        "simple": "The meeting is over.",
        "polite": "The meeting has finished.",
        "friendly": "The meeting is done.",
        "professional": "The meeting has concluded.",
        "formal": "The meeting has officially concluded.",
    },

    {
        "input": "meeting notes ပို့ပေးမယ်။",
        "simple": "I'll send the meeting notes.",
        "polite": "I'll send the meeting notes shortly.",
        "friendly": "I'll send over the meeting notes.",
        "professional": "I will send the meeting notes shortly.",
        "formal": "I will distribute the meeting notes shortly.",
    },

    {
        "input": "meeting မှာ ဒီအကြောင်းပြောမယ်။",
        "simple": "I'll talk about this in the meeting.",
        "polite": "I'll discuss this in the meeting.",
        "friendly": "I'll bring this up in the meeting.",
        "professional": "I will discuss this matter during the meeting.",
        "formal": "I will raise this matter for discussion during the meeting.",
    },

    {
        "input": "meeting အတွက် agenda ပြင်ပြီးပြီ။",
        "simple": "I've prepared the meeting agenda.",
        "polite": "I've prepared the agenda for the meeting.",
        "friendly": "The meeting agenda is ready.",
        "professional": "The meeting agenda has been prepared.",
        "formal": "The agenda for the scheduled meeting has been prepared.",
    },


    # ========================================================
    # PROJECTS / ASSIGNMENTS - 56 to 70
    # ========================================================

    {
        "input": "မနက်ဖြန် project ကို submit လုပ်မယ်။",
        "simple": "I'll submit the project tomorrow.",
        "polite": "I will submit the project tomorrow.",
        "friendly": "I'll submit the project tomorrow.",
        "professional": "I will submit the project by tomorrow.",
        "formal": "I will submit the completed project tomorrow.",
    },

    {
        "input": "project မပြီးသေးဘူး။",
        "simple": "The project isn't finished yet.",
        "polite": "I'm sorry, but the project isn't finished yet.",
        "friendly": "The project isn't done yet.",
        "professional": "The project is still in progress.",
        "formal": "The project has not yet been completed.",
    },

    {
        "input": "project ကို ပြန်စစ်နေတယ်။",
        "simple": "I'm checking the project again.",
        "polite": "I'm reviewing the project again.",
        "friendly": "I'm going over the project again.",
        "professional": "I am currently reviewing the project.",
        "formal": "I am conducting a further review of the project.",
    },

    {
        "input": "project မှာ error တစ်ခုရှိတယ်။",
        "simple": "There's an error in the project.",
        "polite": "There's an error in the project that I need to fix.",
        "friendly": "There's a small error in the project.",
        "professional": "There is an error in the project that needs to be resolved.",
        "formal": "An error has been identified in the project and requires correction.",
    },

    {
        "input": "ဒီ error ကို fix လုပ်မယ်။",
        "simple": "I'll fix this error.",
        "polite": "I'll fix this error as soon as possible.",
        "friendly": "I'll fix this error.",
        "professional": "I will resolve this error.",
        "formal": "I will take the necessary steps to resolve this error.",
    },

    {
        "input": "project deadline နီးလာပြီ။",
        "simple": "The project deadline is getting close.",
        "polite": "The project deadline is approaching.",
        "friendly": "The project deadline is coming up soon.",
        "professional": "The project deadline is approaching.",
        "formal": "The project deadline is drawing near.",
    },

    {
        "input": "deadline တိုးပေးလို့ရမလား။",
        "simple": "Can you extend the deadline?",
        "polite": "Could you please extend the deadline?",
        "friendly": "Could we get a little more time?",
        "professional": "Would it be possible to extend the deadline?",
        "formal": "I would respectfully request an extension of the deadline.",
    },

    {
        "input": "ဒီ task ကို assign လုပ်ပေးထားတယ်။",
        "simple": "I've been assigned this task.",
        "polite": "I've been assigned this task.",
        "friendly": "I was assigned this task.",
        "professional": "This task has been assigned to me.",
        "formal": "I have been assigned responsibility for this task.",
    },

    {
        "input": "ဒီ task ကို ဒီနေ့ပြီးအောင်လုပ်မယ်။",
        "simple": "I'll finish this task today.",
        "polite": "I'll make sure to finish this task today.",
        "friendly": "I'll get this task done today.",
        "professional": "I will complete this task by the end of today.",
        "formal": "I will ensure that this task is completed by the end of today.",
    },

    {
        "input": "team နဲ့အတူ project လုပ်နေတယ်။",
        "simple": "I'm working on the project with my team.",
        "polite": "I'm currently working on the project with my team.",
        "friendly": "I'm working on the project with my team.",
        "professional": "I am collaborating with my team on the project.",
        "formal": "I am currently collaborating with my team members on the project.",
    },

    {
        "input": "project အကြောင်း update ပေးမယ်။",
        "simple": "I'll give you an update on the project.",
        "polite": "I'll provide you with an update on the project.",
        "friendly": "I'll keep you updated on the project.",
        "professional": "I will provide an update on the project's progress.",
        "formal": "I will provide a formal update regarding the project's progress.",
    },

    {
        "input": "project ကို အောင်မြင်အောင်လုပ်မယ်။",
        "simple": "I'll make the project successful.",
        "polite": "I'll do my best to make the project successful.",
        "friendly": "We'll do our best to make the project work.",
        "professional": "I will work to ensure the project's success.",
        "formal": "I will make every effort to ensure the successful completion of the project.",
    },

    {
        "input": "ဒီအပိုင်းကို ငါလုပ်မယ်။",
        "simple": "I'll do this part.",
        "polite": "I'll take care of this part.",
        "friendly": "I'll handle this part.",
        "professional": "I will take responsibility for this part.",
        "formal": "I will assume responsibility for this portion of the work.",
    },

    {
        "input": "အလုပ်ကို အပိုင်းခွဲပြီးလုပ်ကြမယ်။",
        "simple": "Let's divide the work.",
        "polite": "Let's divide the work among the team.",
        "friendly": "Let's split up the work.",
        "professional": "Let's divide the tasks among the team members.",
        "formal": "I suggest that we distribute the responsibilities among the team members.",
    },

    {
        "input": "ဒီ project အတွက် idea တစ်ခုရှိတယ်။",
        "simple": "I have an idea for this project.",
        "polite": "I have an idea that we could consider for this project.",
        "friendly": "I've got an idea for this project.",
        "professional": "I have a proposal for this project.",
        "formal": "I would like to propose an idea for consideration in this project.",
    },


    # ========================================================
    # CAREER / INTERVIEW - 71 to 80
    # ========================================================

    {
        "input": "ဒီ job ကို apply လုပ်ချင်တယ်။",
        "simple": "I want to apply for this job.",
        "polite": "I'd like to apply for this position.",
        "friendly": "I'd like to apply for this job.",
        "professional": "I would like to apply for this position.",
        "formal": "I would like to formally submit my application for this position.",
    },

    {
        "input": "CV ပြင်နေတယ်။",
        "simple": "I'm updating my CV.",
        "polite": "I'm currently updating my CV.",
        "friendly": "I'm working on my CV.",
        "professional": "I am currently updating my CV.",
        "formal": "I am currently revising my curriculum vitae.",
    },

    {
        "input": "interview အတွက် ပြင်ဆင်နေတယ်။",
        "simple": "I'm preparing for the interview.",
        "polite": "I'm currently preparing for the interview.",
        "friendly": "I'm getting ready for my interview.",
        "professional": "I am currently preparing for the interview.",
        "formal": "I am currently making preparations for the upcoming interview.",
    },

    {
        "input": "interview ဘယ်အချိန်ရှိလဲ။",
        "simple": "What time is the interview?",
        "polite": "Could you please let me know what time the interview is?",
        "friendly": "What time is the interview?",
        "professional": "Could you please confirm the interview time?",
        "formal": "I would appreciate confirmation of the scheduled interview time.",
    },

    {
        "input": "interview invitation ရလို့ ဝမ်းသာတယ်။",
        "simple": "I'm happy to receive the interview invitation.",
        "polite": "I'm very pleased to receive the interview invitation.",
        "friendly": "I'm really happy to get the interview invitation.",
        "professional": "I am pleased to receive the interview invitation.",
        "formal": "I sincerely appreciate the opportunity to be invited for an interview.",
    },

    {
        "input": "ဒီ internship ကို လျှောက်ချင်တယ်။",
        "simple": "I want to apply for this internship.",
        "polite": "I'd like to apply for this internship opportunity.",
        "friendly": "I'd love to apply for this internship.",
        "professional": "I would like to apply for this internship position.",
        "formal": "I would like to formally apply for this internship opportunity.",
    },

    {
        "input": "application result ဘယ်တော့သိရမလဲ။",
        "simple": "When will I know the application result?",
        "polite": "Could you please let me know when I can expect the application result?",
        "friendly": "Do you know when I'll hear back about my application?",
        "professional": "Could you please confirm when I can expect to receive the application result?",
        "formal": "I would appreciate information regarding the expected timeline for the application decision.",
    },

    {
        "input": "interview result ကို follow up လုပ်ချင်တယ်။",
        "simple": "I want to follow up on the interview result.",
        "polite": "I'd like to politely follow up regarding my interview result.",
        "friendly": "I just wanted to follow up about my interview.",
        "professional": "I would like to follow up regarding the outcome of my interview.",
        "formal": "I am writing to respectfully inquire about the outcome of my interview.",
    },

    {
        "input": "ဒီ position အတွက် ကျွန်တော်စိတ်ဝင်စားတယ်။",
        "simple": "I'm interested in this position.",
        "polite": "I'm very interested in this position.",
        "friendly": "I'm really interested in this role.",
        "professional": "I am highly interested in this position.",
        "formal": "I am particularly interested in the opportunity associated with this position.",
    },

    {
        "input": "အလုပ်အခွင့်အရေးအတွက် ကျေးဇူးတင်ပါတယ်။",
        "simple": "Thank you for the job opportunity.",
        "polite": "Thank you very much for the opportunity.",
        "friendly": "Thanks so much for the opportunity.",
        "professional": "Thank you for providing me with this opportunity.",
        "formal": "I sincerely appreciate the opportunity you have provided.",
    },


    # ========================================================
    # BUSINESS / CLIENT - 81 to 90
    # ========================================================

    {
        "input": "client ကို update ပေးမယ်။",
        "simple": "I'll give the client an update.",
        "polite": "I'll provide the client with an update.",
        "friendly": "I'll keep the client updated.",
        "professional": "I will provide the client with an update.",
        "formal": "I will provide the client with a formal update regarding the matter.",
    },

    {
        "input": "client က reply မပြန်သေးဘူး။",
        "simple": "The client hasn't replied yet.",
        "polite": "The client hasn't responded yet.",
        "friendly": "The client hasn't gotten back to us yet.",
        "professional": "The client has not responded yet.",
        "formal": "We have not yet received a response from the client.",
    },

    {
        "input": "client ကို email ပို့ပြီးပြီ။",
        "simple": "I've sent the email to the client.",
        "polite": "I've already sent the email to the client.",
        "friendly": "I already sent the client the email.",
        "professional": "The email has already been sent to the client.",
        "formal": "The requested email has been sent to the client.",
    },

    {
        "input": "document ကို client ဆီ ပို့ပေးမယ်။",
        "simple": "I'll send the document to the client.",
        "polite": "I'll send the document to the client shortly.",
        "friendly": "I'll send the document over to the client.",
        "professional": "I will send the document to the client.",
        "formal": "I will forward the requested document to the client.",
    },

    {
        "input": "ဒီ document ကို စစ်ပေးပါ။",
        "simple": "Please check this document.",
        "polite": "Could you please check this document?",
        "friendly": "Can you take a look at this document?",
        "professional": "Could you please review this document?",
        "formal": "I would appreciate it if you could review this document.",
    },

    {
        "input": "ဒီ proposal ကို ပြင်ပြီးပြီ။",
        "simple": "I've revised the proposal.",
        "polite": "I've revised the proposal as requested.",
        "friendly": "I've updated the proposal.",
        "professional": "I have revised the proposal accordingly.",
        "formal": "The proposal has been revised in accordance with the requested changes.",
    },

    {
        "input": "ဒီနေ့ client နဲ့ call ရှိတယ်။",
        "simple": "I have a call with the client today.",
        "polite": "I have a call scheduled with the client today.",
        "friendly": "I've got a call with the client today.",
        "professional": "I have a client call scheduled for today.",
        "formal": "I am scheduled to participate in a call with the client today.",
    },

    {
        "input": "ဒီကိစ္စကို client နဲ့ ဆွေးနွေးမယ်။",
        "simple": "I'll discuss this with the client.",
        "polite": "I'll discuss this matter with the client.",
        "friendly": "I'll talk this over with the client.",
        "professional": "I will discuss this matter with the client.",
        "formal": "I will discuss this matter with the client and seek further clarification.",
    },

    {
        "input": "ဒီနေ့အတွင်း quotation ပို့မယ်။",
        "simple": "I'll send the quotation today.",
        "polite": "I'll send the quotation by the end of today.",
        "friendly": "I'll send over the quotation today.",
        "professional": "I will send the quotation by the end of today.",
        "formal": "I will provide the quotation by the end of today.",
    },

    {
        "input": "အချက်အလက်တွေ ထပ်လိုသေးတယ်။",
        "simple": "I still need more information.",
        "polite": "I would need some additional information, please.",
        "friendly": "I just need a little more information.",
        "professional": "I require some additional information to proceed.",
        "formal": "I would appreciate receiving the additional information required to proceed.",
    },


    # ========================================================
    # DAILY COMMUNICATION - 91 to 100
    # ========================================================

    {
        "input": "အခုလာနေပြီ။",
        "simple": "I'm on my way.",
        "polite": "I'm on my way now.",
        "friendly": "I'm on my way!",
        "professional": "I am currently on my way.",
        "formal": "I am currently en route.",
    },

    {
        "input": "မသေချာသေးဘူး။",
        "simple": "I'm not sure yet.",
        "polite": "I'm not sure yet, I'm afraid.",
        "friendly": "I'm not sure yet.",
        "professional": "I don't have confirmation yet.",
        "formal": "I am unable to confirm this at the moment.",
    },

    {
        "input": "ကြိုးစားကြည့်မယ်။",
        "simple": "I'll try.",
        "polite": "I'll do my best.",
        "friendly": "I'll give it a try.",
        "professional": "I will do my best to accomplish it.",
        "formal": "I will make every effort to accomplish this.",
    },

    {
        "input": "မိုးရွာနေလို့ အပြင်မထွက်တော့ဘူး။",
        "simple": "It's raining, so I won't go outside.",
        "polite": "Since it's raining, I think I'll stay inside.",
        "friendly": "It's raining, so I'm going to stay in.",
        "professional": "Due to the rain, I will not be going outside.",
        "formal": "Due to the current weather conditions, I will remain indoors.",
    },

    {
        "input": "နောက်မှပြန်ခေါ်မယ်။",
        "simple": "I'll call you back later.",
        "polite": "I'll call you back later, if that's okay.",
        "friendly": "I'll call you back later.",
        "professional": "I will return your call later.",
        "formal": "I will return your call at a later time.",
    },

    {
        "input": "အခုမအားသေးဘူး။",
        "simple": "I'm not free right now.",
        "polite": "I'm sorry, but I'm not available right now.",
        "friendly": "I'm a little busy right now.",
        "professional": "I'm currently unavailable.",
        "formal": "I am currently unavailable and will respond when I am free.",
    },

    {
        "input": "နည်းနည်းစောင့်ပေးပါ။",
        "simple": "Please wait a little.",
        "polite": "Could you please wait for a moment?",
        "friendly": "Just give me a minute, please.",
        "professional": "Could you please give me a moment?",
        "formal": "I would appreciate your patience for a brief moment.",
    },

    {
        "input": "ကျေးဇူးပြုပြီး ပြန်ရှင်းပြပေးပါ။",
        "simple": "Please explain it again.",
        "polite": "Could you please explain it again?",
        "friendly": "Can you explain it again for me?",
        "professional": "Could you please clarify this again?",
        "formal": "I would appreciate it if you could provide further clarification.",
    },

    {
        "input": "ကူညီပေးလို့ ကျေးဇူးတင်ပါတယ်။",
        "simple": "Thank you for helping me.",
        "polite": "Thank you very much for your help.",
        "friendly": "Thanks a lot for helping me!",
        "professional": "Thank you for your assistance.",
        "formal": "I sincerely appreciate your assistance and support.",
    },

    {
        "input": "တောင်းပန်ပါတယ်၊ မေ့သွားတယ်။",
        "simple": "Sorry, I forgot.",
        "polite": "I'm sorry, I completely forgot.",
        "friendly": "Sorry, it slipped my mind.",
        "professional": "I apologize; I overlooked it.",
        "formal": "Please accept my apologies for having overlooked this matter.",
    },
]


# ============================================================
# Normalize text
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize Myanmar/English mixed input for matching.
    """
    text = text.strip().lower()

    # Normalize different punctuation
    text = re.sub(r"[၊,]", " ", text)
    text = re.sub(r"[။.!?]", "", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# Find training/reference example
# ============================================================

def find_training_example(text: str):
    """
    Find an exact normalized match from the 100 examples.
    """

    normalized_input = normalize_text(text)

    for example in TRAINING_EXAMPLES:
        example_input = normalize_text(example["input"])

        if normalized_input == example_input:
            return example

    return None


# ============================================================
# Rule-based translation
# ============================================================

def rule_based_translation(text: str, tone: str):
    """
    Return a known translation from the 100-example dataset.
    """

    example = find_training_example(text)

    if example is None:
        return None

    return example.get(tone, example.get("professional"))


# ============================================================
# Qwen Translation
# ============================================================

def generate_translation(
    text: str,
    tone: str,
    context: str = "general",
    audience: str = "auto",
):
    """
    Generate natural English using Qwen.
    """

    if not text.strip():
        return ""

    system_prompt = """
You are MyanTone AI, a Myanmar-to-natural-English translation assistant.

Your job is ONLY to translate the user's Myanmar or Myanmar-English mixed
message into natural English.

Do NOT:
- answer the user's question
- explain the meaning
- summarize
- add information
- change the intended meaning
- invent details

Translate the intended meaning naturally.

The user may write:
- pure Myanmar
- English
- Myanmar + English mixed language

Mixed words such as:
meeting, manager, project, assignment, submit, deadline, CV,
interview, client, task, email, call, presentation, leave
are valid.

Important Myanmar meaning distinctions:

"မလာ" means not come / not go to a place.
"မတက်" means not attend / not join an event such as a meeting or class.
"တော့ဘူး" often means will no longer / won't.
"နိုင်ဘူး" means cannot / unable to.
"ချင်တယ်" means want to.
"မယ်" normally expresses future intention/action.
"လို့" may express a reason or an intended/reported statement depending
on context.

Examples:

ဒီနေ့ meeting မတက်တော့ဘူး။
= I won't attend today's meeting.

ဒီနေ့ အလုပ်မလာတော့ဘူး။
= I won't come to work today.

ဒီနေ့ meeting မတက်နိုင်ဘူး။
= I can't attend today's meeting.

ဒီနေ့ အလုပ်မလာနိုင်ဘူး။
= I can't come to work today.

ဒီနေ့ အလုပ်မလာနိုင်ဘူးလို့ manager ကို ပြောချင်တယ်။
= I want to tell my manager that I can't come to work today.

ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်။
= I want to tell my colleague that I can't attend today's meeting.

Tone must change ONLY the style.

Simple:
Short and direct everyday English.

Polite:
Respectful and courteous.

Friendly:
Natural, warm, casual English.

Professional:
Clear workplace-appropriate English.

Formal:
More formal and respectful English.

Always return ONLY the English translation.
"""


    user_prompt = f"""
Translate this message into natural English.

Context: {context}
Audience: {audience}
Tone: {tone}

Myanmar / mixed input:
{text}

English translation:
"""


    try:
        messages = [
            {
                "role": "system",
                "content": system_prompt.strip(),
            },
            {
                "role": "user",
                "content": user_prompt.strip(),
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
            truncation=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                do_sample=False,
                temperature=0.1,
                top_p=0.9,
                repetition_penalty=1.05,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        result = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        ).strip()

        # Remove accidental prefixes
        prefixes = [
            "English translation:",
            "Translation:",
            "Answer:",
        ]

        for prefix in prefixes:
            if result.lower().startswith(prefix.lower()):
                result = result[len(prefix):].strip()

        # Keep only first non-empty answer if Qwen produces multiple lines
        lines = [
            line.strip()
            for line in result.splitlines()
            if line.strip()
        ]

        if lines:
            result = lines[0]

        return result

    except Exception as e:
        print("QWEN ERROR:", repr(e))
        return ""


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MyanTone AI API is running.",
        "model": MODEL_NAME,
        "device": "cpu",
        "training_examples": len(TRAINING_EXAMPLES),
        "tones": TONES,
    }


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "device": "cpu",
        "training_examples": len(TRAINING_EXAMPLES),
    }


# ============================================================
# Dataset endpoint
# ============================================================

@app.get("/dataset")
def dataset():
    """
    Return the 100 reference/training examples.
    """

    return {
        "count": len(TRAINING_EXAMPLES),
        "examples": TRAINING_EXAMPLES,
    }


# ============================================================
# Translate endpoint
# ============================================================

@app.post("/translate", response_model=TranslateResponse)
def translate(request: TranslateRequest):

    text = request.text.strip()

    if not text:
        return TranslateResponse(
            translation="",
            translations={},
        )

    # --------------------------------------------------------
    # Validate tone
    # --------------------------------------------------------

    tone = request.tone.lower().strip()

    if tone not in TONES:
        tone = "professional"

    # --------------------------------------------------------
    # 1. Try the 100-example reference dataset first
    # --------------------------------------------------------

    rule_translation = rule_based_translation(
        text=text,
        tone=tone,
    )

    if rule_translation is not None:

        print("=" * 60)
        print("REFERENCE DATASET MATCH")
        print("INPUT:", text)
        print("TONE:", tone)
        print("RESULT:", rule_translation)
        print("=" * 60)

        return TranslateResponse(
            translation=rule_translation,
            translations={
                tone: rule_translation,
            },
        )

    # --------------------------------------------------------
    # 2. Unknown sentence → Qwen
    # --------------------------------------------------------

    print("=" * 60)
    print("QWEN TRANSLATION")
    print("INPUT:", text)
    print("TONE:", tone)
    print("=" * 60)

    selected_translation = generate_translation(
        text=text,
        tone=tone,
        context=request.context,
        audience=request.audience,
    )

    # --------------------------------------------------------
    # 3. Safety fallback
    # --------------------------------------------------------

    if not selected_translation:
        selected_translation = (
            "Sorry, I couldn't generate a translation "
            "for this message."
        )

    return TranslateResponse(
        translation=selected_translation,
        translations={
            tone: selected_translation,
        },
    )


# ============================================================
# Generate all 5 tones
# ============================================================

@app.post("/translate-all")
def translate_all(request: TranslateRequest):

    text = request.text.strip()

    if not text:
        return {
            "translation": "",
            "translations": {},
        }

    results = {}

    # First check the 100 examples
    example = find_training_example(text)

    if example:

        for tone in TONES:
            results[tone] = example[tone]

        return {
            "translation": results.get(
                request.tone,
                results["professional"],
            ),
            "translations": results,
        }

    # Otherwise generate each tone using Qwen
    for tone in TONES:

        result = generate_translation(
            text=text,
            tone=tone,
            context=request.context,
            audience=request.audience,
        )

        if not result:
            result = "Unable to generate translation."

        results[tone] = result

    selected_tone = request.tone.lower().strip()

    if selected_tone not in TONES:
        selected_tone = "professional"

    return {
        "translation": results[selected_tone],
        "translations": results,
    }


# ============================================================
# Run with:
#
# uvicorn api:app --reload --port 8000
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )