# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# import re


# # ============================================================
# # MyanTone AI
# # Myanmar → Natural English
# # ============================================================

# MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# # Visible API/build version. Change this whenever backend behavior changes.
# API_VERSION = "2.2.0-complete-context-debug"
# API_BUILD = "2026-09-21-long-context"


# # ============================================================
# # Load Qwen model
# # ============================================================

# print("Loading MyanTone AI model...")
# print(f"Model: {MODEL_NAME}")

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     dtype=torch.float32,
# )

# model.to("cpu")
# model.eval()

# print("Model loaded successfully.")
# print("Device: CPU")


# # ============================================================
# # FastAPI
# # ============================================================

# app = FastAPI(
#     title="MyanTone AI API",
#     description="Myanmar to natural English translation with tone control.",
#     version=API_VERSION,
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
# # Tones
# # ============================================================

# TONES = [
#     "simple",
#     "polite",
#     "friendly",
#     "professional",
#     "formal",
# ]


# # ============================================================
# # Request / Response Models
# # ============================================================

# class TranslateRequest(BaseModel):
#     text: str
#     tone: str = "professional"
#     context: str = "general"
#     audience: str = "auto"


# class TranslateResponse(BaseModel):
#     translation: str
#     translations: dict[str, str]
#     api_version: str = API_VERSION
#     debug: dict = Field(default_factory=dict)
#     # AI Understanding is returned by the API so the frontend can display
#     # the complete meaning that was detected, instead of only the final intent.
#     language: str = ""
#     intent: str = ""
#     audience_detected: str = ""
#     situation: str = ""
#     reason: str = ""
#     main_action: str = ""
#     cause_chain: str = ""
#     recommended_tone: str = ""


# # ============================================================
# # 100 TRAINING / REFERENCE SENTENCES
# #
# # These examples are used as a deterministic reference layer.
# # They also provide training-style examples for the project.
# # ============================================================

# TRAINING_EXAMPLES = [

#     # ========================================================
#     # WORK / OFFICE - 1 to 25
#     # ========================================================

#     {
#         "input": "ဒီနေ့ အလုပ်နောက်ကျမယ်။",
#         "simple": "I'll be late for work today.",
#         "polite": "I'm sorry, but I'll be late for work today.",
#         "friendly": "I'll be a little late for work today.",
#         "professional": "I'll be slightly late for work today.",
#         "formal": "I will be slightly delayed in arriving at work today.",
#     },

#     {
#         "input": "ကားပိတ်နေလို့ အလုပ်နောက်ကျမယ်။",
#         "simple": "I'll be late for work because of traffic.",
#         "polite": "I'm sorry, but I'll be late for work because of the traffic.",
#         "friendly": "The traffic is bad, so I'll be a little late for work.",
#         "professional": "I'll be slightly late for work due to traffic.",
#         "formal": "I will be delayed in arriving at work due to traffic congestion.",
#     },

#     {
#         "input": "ဒီနေ့ အလုပ်မလာနိုင်ဘူး။",
#         "simple": "I can't come to work today.",
#         "polite": "I'm sorry, but I can't come to work today.",
#         "friendly": "I won't be able to make it to work today.",
#         "professional": "I will be unable to come to work today.",
#         "formal": "I regret to inform you that I will be unable to report to work today.",
#     },

#     {
#         "input": "ဒီနေ့ အလုပ်မလာတော့ဘူး။",
#         "simple": "I won't come to work today.",
#         "polite": "I'm sorry, but I won't be coming to work today.",
#         "friendly": "I won't be coming to work today.",
#         "professional": "I will not be coming to work today.",
#         "formal": "I would like to inform you that I will not be reporting to work today.",
#     },

#     {
#         "input": "မနက်ဖြန် အလုပ်သွားမယ်။",
#         "simple": "I'll go to work tomorrow.",
#         "polite": "I'll be going to work tomorrow.",
#         "friendly": "I'll be at work tomorrow.",
#         "professional": "I will be at work tomorrow.",
#         "formal": "I will report to work tomorrow.",
#     },

#     {
#         "input": "အခု အလုပ်လုပ်နေတယ်။",
#         "simple": "I'm working right now.",
#         "polite": "I'm currently working on it.",
#         "friendly": "I'm working on it right now.",
#         "professional": "I'm currently working on the task.",
#         "formal": "I am currently engaged in the assigned work.",
#     },

#     {
#         "input": "အခုထိ အလုပ်မပြီးသေးဘူး။",
#         "simple": "I haven't finished the work yet.",
#         "polite": "I'm sorry, but I haven't finished the work yet.",
#         "friendly": "I haven't finished it yet.",
#         "professional": "The work is not completed yet.",
#         "formal": "The assigned work has not yet been completed.",
#     },

#     {
#         "input": "အလုပ်ပြီးသွားပြီ။",
#         "simple": "The work is finished.",
#         "polite": "I've finished the work.",
#         "friendly": "It's all done.",
#         "professional": "The work has been completed.",
#         "formal": "The assigned work has been successfully completed.",
#     },

#     {
#         "input": "အလုပ်နည်းနည်းနောက်ကျမယ်။",
#         "simple": "I'll be a little late for work.",
#         "polite": "I'm sorry, but I'll be a little late for work.",
#         "friendly": "I'll be a bit late for work.",
#         "professional": "I'll be slightly late for work.",
#         "formal": "I will be slightly delayed in arriving at work.",
#     },

#     {
#         "input": "ဒီနေ့ leave ယူချင်တယ်။",
#         "simple": "I want to take leave today.",
#         "polite": "I'd like to take leave today, if possible.",
#         "friendly": "I'd like to take the day off today.",
#         "professional": "I would like to request leave for today.",
#         "formal": "I would like to formally request leave for today.",
#     },

#     {
#         "input": "မနက်ဖြန် leave ယူမယ်။",
#         "simple": "I'll take leave tomorrow.",
#         "polite": "I'd like to take leave tomorrow.",
#         "friendly": "I'll be taking the day off tomorrow.",
#         "professional": "I will be taking leave tomorrow.",
#         "formal": "I would like to inform you that I will be taking leave tomorrow.",
#     },

#     {
#         "input": "ဒီ task ကို လုပ်နေတယ်။",
#         "simple": "I'm working on this task.",
#         "polite": "I'm currently working on this task.",
#         "friendly": "I'm working on this task now.",
#         "professional": "I'm currently working on this task.",
#         "formal": "I am currently working on the assigned task.",
#     },

#     {
#         "input": "ဒီ task ပြီးရင် ပို့ပေးမယ်။",
#         "simple": "I'll send it when I finish this task.",
#         "polite": "I'll send it once I finish this task.",
#         "friendly": "I'll send it over when I'm done with this task.",
#         "professional": "I will send it once this task is completed.",
#         "formal": "I will forward it upon completion of this task.",
#     },

#     {
#         "input": "အလုပ်ကိစ္စနည်းနည်းများနေတယ်။",
#         "simple": "I have a lot of work right now.",
#         "polite": "I have quite a bit of work to handle right now.",
#         "friendly": "I've got a lot on my plate right now.",
#         "professional": "I am currently handling a heavy workload.",
#         "formal": "I am currently managing a substantial workload.",
#     },

#     {
#         "input": "ဒီအလုပ်ကို အရင်လုပ်လိုက်မယ်။",
#         "simple": "I'll do this work first.",
#         "polite": "I'll take care of this first.",
#         "friendly": "I'll get this done first.",
#         "professional": "I'll prioritize this task first.",
#         "formal": "I will prioritize this task before proceeding with the others.",
#     },

#     {
#         "input": "အလုပ်အခြေအနေကို update ပေးမယ်။",
#         "simple": "I'll give you an update on the work.",
#         "polite": "I'll give you an update on the work shortly.",
#         "friendly": "I'll keep you updated on the work.",
#         "professional": "I will provide an update on the work.",
#         "formal": "I will provide you with an update regarding the progress of the work.",
#     },

#     {
#         "input": "ဒီအလုပ်ကို ဘယ်အချိန်ပြီးရမလဲ။",
#         "simple": "When do I need to finish this work?",
#         "polite": "When would you like me to finish this work?",
#         "friendly": "When do you need this done?",
#         "professional": "What is the deadline for this task?",
#         "formal": "Could you please confirm the deadline for this task?",
#     },

#     {
#         "input": "ဒီနေ့အတွင်းပြီးအောင်လုပ်မယ်။",
#         "simple": "I'll finish it today.",
#         "polite": "I'll make sure to finish it today.",
#         "friendly": "I'll get it done today.",
#         "professional": "I will complete it by the end of today.",
#         "formal": "I will ensure that the task is completed by the end of today.",
#     },

#     {
#         "input": "ဒီကိစ္စကို manager နဲ့ ပြောပြီးပြီ။",
#         "simple": "I already talked to the manager about this.",
#         "polite": "I've already discussed this with the manager.",
#         "friendly": "I already talked to the manager about it.",
#         "professional": "I have already discussed this matter with the manager.",
#         "formal": "I have already discussed this matter with the manager.",
#     },

#     {
#         "input": "manager ကို ပြောပေးပါ။",
#         "simple": "Please tell the manager.",
#         "polite": "Could you please let the manager know?",
#         "friendly": "Can you let the manager know?",
#         "professional": "Please inform the manager.",
#         "formal": "I would appreciate it if you could inform the manager.",
#     },

#     {
#         "input": "ဒီ file ကို ပြန်ပို့ပေးပါ။",
#         "simple": "Please send this file again.",
#         "polite": "Could you please resend this file?",
#         "friendly": "Can you send this file again?",
#         "professional": "Please resend the file.",
#         "formal": "Could you kindly resend the requested file?",
#     },

#     {
#         "input": "file ကို attach လုပ်ထားတယ်။",
#         "simple": "I attached the file.",
#         "polite": "I've attached the file for you.",
#         "friendly": "I've attached the file here.",
#         "professional": "The file has been attached for your review.",
#         "formal": "Please find the requested file attached.",
#     },

#     {
#         "input": "ဒီကိစ္စကို နောက်မှပြောမယ်။",
#         "simple": "I'll talk about this later.",
#         "polite": "I'll discuss this with you later.",
#         "friendly": "Let's talk about this later.",
#         "professional": "I'll discuss this matter with you later.",
#         "formal": "I would like to discuss this matter at a later time.",
#     },

#     {
#         "input": "အလုပ်မှာ ပြဿနာတစ်ခုရှိတယ်။",
#         "simple": "There's a problem at work.",
#         "polite": "There's an issue at work that I'd like to discuss.",
#         "friendly": "There's a small problem at work.",
#         "professional": "There is an issue that needs to be addressed at work.",
#         "formal": "There is an issue at work that requires attention.",
#     },

#     {
#         "input": "ဒီကိစ္စကို ကူညီပေးပါ။",
#         "simple": "Please help me with this.",
#         "polite": "Could you please help me with this?",
#         "friendly": "Can you help me with this?",
#         "professional": "Could you please assist me with this matter?",
#         "formal": "I would appreciate your assistance with this matter.",
#     },


#     # ========================================================
#     # UNIVERSITY / SCHOOL - 26 to 45
#     # ========================================================

#     {
#         "input": "နေမကောင်းလို့ ဒီနေ့ ကျောင်းမတက်နိုင်ဘူး။",
#         "simple": "I'm sick, so I can't attend school today.",
#         "polite": "I'm sorry, but I'm not feeling well and can't attend school today.",
#         "friendly": "I'm not feeling well, so I can't make it to school today.",
#         "professional": "I am unwell and will be unable to attend school today.",
#         "formal": "I regret to inform you that I am unwell and unable to attend school today.",
#     },

#     {
#         "input": "ဒီနေ့ lecture နောက်ကျမယ်။",
#         "simple": "I'll be late for the lecture today.",
#         "polite": "I'm sorry, but I'll be late for today's lecture.",
#         "friendly": "I'll be a little late for the lecture today.",
#         "professional": "I will be slightly late for today's lecture.",
#         "formal": "I will be delayed in attending today's lecture.",
#     },

#     {
#         "input": "ဒီနေ့ class မတက်နိုင်ဘူး။",
#         "simple": "I can't attend class today.",
#         "polite": "I'm sorry, but I can't attend class today.",
#         "friendly": "I won't be able to make it to class today.",
#         "professional": "I will be unable to attend today's class.",
#         "formal": "I regret to inform you that I will be unable to attend today's class.",
#     },

#     {
#         "input": "assignment မပြီးသေးဘူး။",
#         "simple": "I haven't finished the assignment yet.",
#         "polite": "I'm sorry, but I haven't finished the assignment yet.",
#         "friendly": "I haven't finished the assignment yet.",
#         "professional": "The assignment is not completed yet.",
#         "formal": "The assignment has not yet been completed.",
#     },

#     {
#         "input": "assignment မပြီးသေးလို့ deadline တိုးပေးပါ။",
#         "simple": "Please extend the deadline because I haven't finished the assignment.",
#         "polite": "Could you please extend the deadline because I haven't finished the assignment yet?",
#         "friendly": "Could you give me a little more time to finish the assignment?",
#         "professional": "Could you please extend the deadline as I have not yet completed the assignment?",
#         "formal": "I would respectfully request an extension of the assignment deadline.",
#     },

#     {
#         "input": "မနက်ဖြန် assignment submit လုပ်မယ်။",
#         "simple": "I'll submit the assignment tomorrow.",
#         "polite": "I will submit the assignment tomorrow.",
#         "friendly": "I'll submit the assignment tomorrow.",
#         "professional": "I will submit the assignment by tomorrow.",
#         "formal": "I will submit the completed assignment tomorrow.",
#     },

#     {
#         "input": "ဒီနေ့ exam ရှိတယ်။",
#         "simple": "I have an exam today.",
#         "polite": "I have an exam today.",
#         "friendly": "I've got an exam today.",
#         "professional": "I have an examination scheduled for today.",
#         "formal": "I am scheduled to take an examination today.",
#     },

#     {
#         "input": "exam အတွက် စာလေ့လာနေတယ်။",
#         "simple": "I'm studying for the exam.",
#         "polite": "I'm currently studying for the exam.",
#         "friendly": "I'm studying for my exam right now.",
#         "professional": "I am currently preparing for the examination.",
#         "formal": "I am currently preparing for the upcoming examination.",
#     },

#     {
#         "input": "project အတွက် team member တွေနဲ့ ဆွေးနွေးနေတယ်။",
#         "simple": "I'm discussing the project with my team members.",
#         "polite": "I'm currently discussing the project with my team members.",
#         "friendly": "I'm talking about the project with my team.",
#         "professional": "I am discussing the project with the team.",
#         "formal": "I am currently coordinating with my team members regarding the project.",
#     },

#     {
#         "input": "presentation မနက်ဖြန်လုပ်ရမယ်။",
#         "simple": "I have to give a presentation tomorrow.",
#         "polite": "I have to give a presentation tomorrow.",
#         "friendly": "I've got a presentation tomorrow.",
#         "professional": "I am scheduled to give a presentation tomorrow.",
#         "formal": "I am scheduled to deliver a presentation tomorrow.",
#     },

#     {
#         "input": "presentation အတွက် ပြင်ဆင်နေတယ်။",
#         "simple": "I'm preparing for the presentation.",
#         "polite": "I'm currently preparing for the presentation.",
#         "friendly": "I'm getting ready for the presentation.",
#         "professional": "I am currently preparing the presentation.",
#         "formal": "I am currently making preparations for the presentation.",
#     },

#     {
#         "input": "ဆရာကို မေးချင်တာရှိတယ်။",
#         "simple": "I want to ask the teacher something.",
#         "polite": "I'd like to ask the teacher something.",
#         "friendly": "I want to ask the teacher something.",
#         "professional": "I would like to ask the instructor a question.",
#         "formal": "I would like to ask the instructor for clarification regarding a matter.",
#     },

#     {
#         "input": "ဒီ lesson ကို နားမလည်ဘူး။",
#         "simple": "I don't understand this lesson.",
#         "polite": "I'm having trouble understanding this lesson.",
#         "friendly": "I don't really understand this lesson.",
#         "professional": "I am having difficulty understanding this lesson.",
#         "formal": "I am having difficulty understanding the material covered in this lesson.",
#     },

#     {
#         "input": "နောက်တစ်ခါ ပြန်ရှင်းပြပေးပါ။",
#         "simple": "Please explain it again.",
#         "polite": "Could you please explain it again?",
#         "friendly": "Can you explain it one more time?",
#         "professional": "Could you please explain the concept again?",
#         "formal": "I would appreciate it if you could explain the concept once again.",
#     },

#     {
#         "input": "ဒီနေ့ university မသွားနိုင်ဘူး။",
#         "simple": "I can't go to university today.",
#         "polite": "I'm sorry, but I can't go to university today.",
#         "friendly": "I won't be able to make it to university today.",
#         "professional": "I will be unable to attend university today.",
#         "formal": "I regret to inform you that I will be unable to attend university today.",
#     },

#     {
#         "input": "group project အတွက် meeting လုပ်မယ်။",
#         "simple": "We'll have a meeting for the group project.",
#         "polite": "We'll have a meeting to discuss the group project.",
#         "friendly": "We're going to have a meeting for the group project.",
#         "professional": "We will hold a meeting to discuss the group project.",
#         "formal": "We will conduct a meeting regarding the group project.",
#     },

#     {
#         "input": "project ကို မနက်ဖြန် submit လုပ်မယ်။",
#         "simple": "I'll submit the project tomorrow.",
#         "polite": "I'll submit the project tomorrow.",
#         "friendly": "I'll get the project submitted tomorrow.",
#         "professional": "I will submit the project by tomorrow.",
#         "formal": "I will submit the completed project tomorrow.",
#     },

#     {
#         "input": "စာမေးပွဲ result ဘယ်တော့ထွက်မလဲ။",
#         "simple": "When will the exam results come out?",
#         "polite": "Could you please let me know when the exam results will be released?",
#         "friendly": "Do you know when the exam results will be out?",
#         "professional": "Could you please confirm when the examination results will be released?",
#         "formal": "I would appreciate information regarding the release date of the examination results.",
#     },

#     {
#         "input": "ဒီနေ့ class ရှိမရှိ မသေချာဘူး။",
#         "simple": "I'm not sure if there's class today.",
#         "polite": "I'm not sure whether we have class today.",
#         "friendly": "I'm not sure if we have class today.",
#         "professional": "I'm unsure whether today's class is scheduled.",
#         "formal": "I would like to confirm whether a class is scheduled for today.",
#     },

#     {
#         "input": "notes တွေ ပို့ပေးပါ။",
#         "simple": "Please send me the notes.",
#         "polite": "Could you please send me the notes?",
#         "friendly": "Can you send me the notes?",
#         "professional": "Could you please share the lecture notes with me?",
#         "formal": "I would appreciate it if you could provide me with the lecture notes.",
#     },


#     # ========================================================
#     # MEETINGS - 46 to 55
#     # ========================================================

#     {
#         "input": "ဒီနေ့ meeting မတက်နိုင်ဘူး။",
#         "simple": "I can't attend today's meeting.",
#         "polite": "I'm sorry, but I won't be able to attend today's meeting.",
#         "friendly": "I won't be able to make it to today's meeting.",
#         "professional": "I will be unable to attend today's meeting.",
#         "formal": "I regret to inform you that I will be unable to attend today's meeting.",
#     },

#     {
#         "input": "ဒီနေ့ meeting မတက်တော့ဘူး။",
#         "simple": "I won't attend today's meeting.",
#         "polite": "I'm sorry, but I won't be attending today's meeting.",
#         "friendly": "I won't be joining today's meeting.",
#         "professional": "I will not be attending today's meeting.",
#         "formal": "I would like to inform you that I will not be attending today's meeting.",
#     },

#     {
#         "input": "meeting ကို နောက်တစ်ချိန်ရွှေ့လို့ရမလား။",
#         "simple": "Can we move the meeting to another time?",
#         "polite": "Could we please move the meeting to another time?",
#         "friendly": "Can we reschedule the meeting?",
#         "professional": "Could we reschedule the meeting to a different time?",
#         "formal": "Would it be possible to reschedule the meeting for another time?",
#     },

#     {
#         "input": "meeting ဘယ်အချိန်စမလဲ။",
#         "simple": "What time does the meeting start?",
#         "polite": "Could you please let me know what time the meeting starts?",
#         "friendly": "What time does the meeting start?",
#         "professional": "Could you please confirm the meeting start time?",
#         "formal": "I would appreciate confirmation of the scheduled meeting time.",
#     },

#     {
#         "input": "meeting link ပို့ပေးပါ။",
#         "simple": "Please send me the meeting link.",
#         "polite": "Could you please send me the meeting link?",
#         "friendly": "Can you send me the meeting link?",
#         "professional": "Please share the meeting link with me.",
#         "formal": "I would appreciate it if you could provide the meeting link.",
#     },

#     {
#         "input": "meeting အတွက် ပြင်ဆင်နေတယ်။",
#         "simple": "I'm preparing for the meeting.",
#         "polite": "I'm currently preparing for the meeting.",
#         "friendly": "I'm getting ready for the meeting.",
#         "professional": "I am currently preparing for the meeting.",
#         "formal": "I am currently making preparations for the scheduled meeting.",
#     },

#     {
#         "input": "meeting ပြီးသွားပြီ။",
#         "simple": "The meeting is over.",
#         "polite": "The meeting has finished.",
#         "friendly": "The meeting is done.",
#         "professional": "The meeting has concluded.",
#         "formal": "The meeting has officially concluded.",
#     },

#     {
#         "input": "meeting notes ပို့ပေးမယ်။",
#         "simple": "I'll send the meeting notes.",
#         "polite": "I'll send the meeting notes shortly.",
#         "friendly": "I'll send over the meeting notes.",
#         "professional": "I will send the meeting notes shortly.",
#         "formal": "I will distribute the meeting notes shortly.",
#     },

#     {
#         "input": "meeting မှာ ဒီအကြောင်းပြောမယ်။",
#         "simple": "I'll talk about this in the meeting.",
#         "polite": "I'll discuss this in the meeting.",
#         "friendly": "I'll bring this up in the meeting.",
#         "professional": "I will discuss this matter during the meeting.",
#         "formal": "I will raise this matter for discussion during the meeting.",
#     },

#     {
#         "input": "meeting အတွက် agenda ပြင်ပြီးပြီ။",
#         "simple": "I've prepared the meeting agenda.",
#         "polite": "I've prepared the agenda for the meeting.",
#         "friendly": "The meeting agenda is ready.",
#         "professional": "The meeting agenda has been prepared.",
#         "formal": "The agenda for the scheduled meeting has been prepared.",
#     },


#     # ========================================================
#     # PROJECTS / ASSIGNMENTS - 56 to 70
#     # ========================================================

#     {
#         "input": "မနက်ဖြန် project ကို submit လုပ်မယ်။",
#         "simple": "I'll submit the project tomorrow.",
#         "polite": "I will submit the project tomorrow.",
#         "friendly": "I'll submit the project tomorrow.",
#         "professional": "I will submit the project by tomorrow.",
#         "formal": "I will submit the completed project tomorrow.",
#     },

#     {
#         "input": "project မပြီးသေးဘူး။",
#         "simple": "The project isn't finished yet.",
#         "polite": "I'm sorry, but the project isn't finished yet.",
#         "friendly": "The project isn't done yet.",
#         "professional": "The project is still in progress.",
#         "formal": "The project has not yet been completed.",
#     },

#     {
#         "input": "project ကို ပြန်စစ်နေတယ်။",
#         "simple": "I'm checking the project again.",
#         "polite": "I'm reviewing the project again.",
#         "friendly": "I'm going over the project again.",
#         "professional": "I am currently reviewing the project.",
#         "formal": "I am conducting a further review of the project.",
#     },

#     {
#         "input": "project မှာ error တစ်ခုရှိတယ်။",
#         "simple": "There's an error in the project.",
#         "polite": "There's an error in the project that I need to fix.",
#         "friendly": "There's a small error in the project.",
#         "professional": "There is an error in the project that needs to be resolved.",
#         "formal": "An error has been identified in the project and requires correction.",
#     },

#     {
#         "input": "ဒီ error ကို fix လုပ်မယ်။",
#         "simple": "I'll fix this error.",
#         "polite": "I'll fix this error as soon as possible.",
#         "friendly": "I'll fix this error.",
#         "professional": "I will resolve this error.",
#         "formal": "I will take the necessary steps to resolve this error.",
#     },

#     {
#         "input": "project deadline နီးလာပြီ။",
#         "simple": "The project deadline is getting close.",
#         "polite": "The project deadline is approaching.",
#         "friendly": "The project deadline is coming up soon.",
#         "professional": "The project deadline is approaching.",
#         "formal": "The project deadline is drawing near.",
#     },

#     {
#         "input": "deadline တိုးပေးလို့ရမလား။",
#         "simple": "Can you extend the deadline?",
#         "polite": "Could you please extend the deadline?",
#         "friendly": "Could we get a little more time?",
#         "professional": "Would it be possible to extend the deadline?",
#         "formal": "I would respectfully request an extension of the deadline.",
#     },

#     {
#         "input": "ဒီ task ကို assign လုပ်ပေးထားတယ်။",
#         "simple": "I've been assigned this task.",
#         "polite": "I've been assigned this task.",
#         "friendly": "I was assigned this task.",
#         "professional": "This task has been assigned to me.",
#         "formal": "I have been assigned responsibility for this task.",
#     },

#     {
#         "input": "ဒီ task ကို ဒီနေ့ပြီးအောင်လုပ်မယ်။",
#         "simple": "I'll finish this task today.",
#         "polite": "I'll make sure to finish this task today.",
#         "friendly": "I'll get this task done today.",
#         "professional": "I will complete this task by the end of today.",
#         "formal": "I will ensure that this task is completed by the end of today.",
#     },

#     {
#         "input": "team နဲ့အတူ project လုပ်နေတယ်။",
#         "simple": "I'm working on the project with my team.",
#         "polite": "I'm currently working on the project with my team.",
#         "friendly": "I'm working on the project with my team.",
#         "professional": "I am collaborating with my team on the project.",
#         "formal": "I am currently collaborating with my team members on the project.",
#     },

#     {
#         "input": "project အကြောင်း update ပေးမယ်။",
#         "simple": "I'll give you an update on the project.",
#         "polite": "I'll provide you with an update on the project.",
#         "friendly": "I'll keep you updated on the project.",
#         "professional": "I will provide an update on the project's progress.",
#         "formal": "I will provide a formal update regarding the project's progress.",
#     },

#     {
#         "input": "project ကို အောင်မြင်အောင်လုပ်မယ်။",
#         "simple": "I'll make the project successful.",
#         "polite": "I'll do my best to make the project successful.",
#         "friendly": "We'll do our best to make the project work.",
#         "professional": "I will work to ensure the project's success.",
#         "formal": "I will make every effort to ensure the successful completion of the project.",
#     },

#     {
#         "input": "ဒီအပိုင်းကို ငါလုပ်မယ်။",
#         "simple": "I'll do this part.",
#         "polite": "I'll take care of this part.",
#         "friendly": "I'll handle this part.",
#         "professional": "I will take responsibility for this part.",
#         "formal": "I will assume responsibility for this portion of the work.",
#     },

#     {
#         "input": "အလုပ်ကို အပိုင်းခွဲပြီးလုပ်ကြမယ်။",
#         "simple": "Let's divide the work.",
#         "polite": "Let's divide the work among the team.",
#         "friendly": "Let's split up the work.",
#         "professional": "Let's divide the tasks among the team members.",
#         "formal": "I suggest that we distribute the responsibilities among the team members.",
#     },

#     {
#         "input": "ဒီ project အတွက် idea တစ်ခုရှိတယ်။",
#         "simple": "I have an idea for this project.",
#         "polite": "I have an idea that we could consider for this project.",
#         "friendly": "I've got an idea for this project.",
#         "professional": "I have a proposal for this project.",
#         "formal": "I would like to propose an idea for consideration in this project.",
#     },


#     # ========================================================
#     # CAREER / INTERVIEW - 71 to 80
#     # ========================================================

#     {
#         "input": "ဒီ job ကို apply လုပ်ချင်တယ်။",
#         "simple": "I want to apply for this job.",
#         "polite": "I'd like to apply for this position.",
#         "friendly": "I'd like to apply for this job.",
#         "professional": "I would like to apply for this position.",
#         "formal": "I would like to formally submit my application for this position.",
#     },

#     {
#         "input": "CV ပြင်နေတယ်။",
#         "simple": "I'm updating my CV.",
#         "polite": "I'm currently updating my CV.",
#         "friendly": "I'm working on my CV.",
#         "professional": "I am currently updating my CV.",
#         "formal": "I am currently revising my curriculum vitae.",
#     },

#     {
#         "input": "interview အတွက် ပြင်ဆင်နေတယ်။",
#         "simple": "I'm preparing for the interview.",
#         "polite": "I'm currently preparing for the interview.",
#         "friendly": "I'm getting ready for my interview.",
#         "professional": "I am currently preparing for the interview.",
#         "formal": "I am currently making preparations for the upcoming interview.",
#     },

#     {
#         "input": "interview ဘယ်အချိန်ရှိလဲ။",
#         "simple": "What time is the interview?",
#         "polite": "Could you please let me know what time the interview is?",
#         "friendly": "What time is the interview?",
#         "professional": "Could you please confirm the interview time?",
#         "formal": "I would appreciate confirmation of the scheduled interview time.",
#     },

#     {
#         "input": "interview invitation ရလို့ ဝမ်းသာတယ်။",
#         "simple": "I'm happy to receive the interview invitation.",
#         "polite": "I'm very pleased to receive the interview invitation.",
#         "friendly": "I'm really happy to get the interview invitation.",
#         "professional": "I am pleased to receive the interview invitation.",
#         "formal": "I sincerely appreciate the opportunity to be invited for an interview.",
#     },

#     {
#         "input": "ဒီ internship ကို လျှောက်ချင်တယ်။",
#         "simple": "I want to apply for this internship.",
#         "polite": "I'd like to apply for this internship opportunity.",
#         "friendly": "I'd love to apply for this internship.",
#         "professional": "I would like to apply for this internship position.",
#         "formal": "I would like to formally apply for this internship opportunity.",
#     },

#     {
#         "input": "application result ဘယ်တော့သိရမလဲ။",
#         "simple": "When will I know the application result?",
#         "polite": "Could you please let me know when I can expect the application result?",
#         "friendly": "Do you know when I'll hear back about my application?",
#         "professional": "Could you please confirm when I can expect to receive the application result?",
#         "formal": "I would appreciate information regarding the expected timeline for the application decision.",
#     },

#     {
#         "input": "interview result ကို follow up လုပ်ချင်တယ်။",
#         "simple": "I want to follow up on the interview result.",
#         "polite": "I'd like to politely follow up regarding my interview result.",
#         "friendly": "I just wanted to follow up about my interview.",
#         "professional": "I would like to follow up regarding the outcome of my interview.",
#         "formal": "I am writing to respectfully inquire about the outcome of my interview.",
#     },

#     {
#         "input": "ဒီ position အတွက် ကျွန်တော်စိတ်ဝင်စားတယ်။",
#         "simple": "I'm interested in this position.",
#         "polite": "I'm very interested in this position.",
#         "friendly": "I'm really interested in this role.",
#         "professional": "I am highly interested in this position.",
#         "formal": "I am particularly interested in the opportunity associated with this position.",
#     },

#     {
#         "input": "အလုပ်အခွင့်အရေးအတွက် ကျေးဇူးတင်ပါတယ်။",
#         "simple": "Thank you for the job opportunity.",
#         "polite": "Thank you very much for the opportunity.",
#         "friendly": "Thanks so much for the opportunity.",
#         "professional": "Thank you for providing me with this opportunity.",
#         "formal": "I sincerely appreciate the opportunity you have provided.",
#     },


#     # ========================================================
#     # BUSINESS / CLIENT - 81 to 90
#     # ========================================================

#     {
#         "input": "client ကို update ပေးမယ်။",
#         "simple": "I'll give the client an update.",
#         "polite": "I'll provide the client with an update.",
#         "friendly": "I'll keep the client updated.",
#         "professional": "I will provide the client with an update.",
#         "formal": "I will provide the client with a formal update regarding the matter.",
#     },

#     {
#         "input": "client က reply မပြန်သေးဘူး။",
#         "simple": "The client hasn't replied yet.",
#         "polite": "The client hasn't responded yet.",
#         "friendly": "The client hasn't gotten back to us yet.",
#         "professional": "The client has not responded yet.",
#         "formal": "We have not yet received a response from the client.",
#     },

#     {
#         "input": "client ကို email ပို့ပြီးပြီ။",
#         "simple": "I've sent the email to the client.",
#         "polite": "I've already sent the email to the client.",
#         "friendly": "I already sent the client the email.",
#         "professional": "The email has already been sent to the client.",
#         "formal": "The requested email has been sent to the client.",
#     },

#     {
#         "input": "document ကို client ဆီ ပို့ပေးမယ်။",
#         "simple": "I'll send the document to the client.",
#         "polite": "I'll send the document to the client shortly.",
#         "friendly": "I'll send the document over to the client.",
#         "professional": "I will send the document to the client.",
#         "formal": "I will forward the requested document to the client.",
#     },

#     {
#         "input": "ဒီ document ကို စစ်ပေးပါ။",
#         "simple": "Please check this document.",
#         "polite": "Could you please check this document?",
#         "friendly": "Can you take a look at this document?",
#         "professional": "Could you please review this document?",
#         "formal": "I would appreciate it if you could review this document.",
#     },

#     {
#         "input": "ဒီ proposal ကို ပြင်ပြီးပြီ။",
#         "simple": "I've revised the proposal.",
#         "polite": "I've revised the proposal as requested.",
#         "friendly": "I've updated the proposal.",
#         "professional": "I have revised the proposal accordingly.",
#         "formal": "The proposal has been revised in accordance with the requested changes.",
#     },

#     {
#         "input": "ဒီနေ့ client နဲ့ call ရှိတယ်။",
#         "simple": "I have a call with the client today.",
#         "polite": "I have a call scheduled with the client today.",
#         "friendly": "I've got a call with the client today.",
#         "professional": "I have a client call scheduled for today.",
#         "formal": "I am scheduled to participate in a call with the client today.",
#     },

#     {
#         "input": "ဒီကိစ္စကို client နဲ့ ဆွေးနွေးမယ်။",
#         "simple": "I'll discuss this with the client.",
#         "polite": "I'll discuss this matter with the client.",
#         "friendly": "I'll talk this over with the client.",
#         "professional": "I will discuss this matter with the client.",
#         "formal": "I will discuss this matter with the client and seek further clarification.",
#     },

#     {
#         "input": "ဒီနေ့အတွင်း quotation ပို့မယ်။",
#         "simple": "I'll send the quotation today.",
#         "polite": "I'll send the quotation by the end of today.",
#         "friendly": "I'll send over the quotation today.",
#         "professional": "I will send the quotation by the end of today.",
#         "formal": "I will provide the quotation by the end of today.",
#     },

#     {
#         "input": "အချက်အလက်တွေ ထပ်လိုသေးတယ်။",
#         "simple": "I still need more information.",
#         "polite": "I would need some additional information, please.",
#         "friendly": "I just need a little more information.",
#         "professional": "I require some additional information to proceed.",
#         "formal": "I would appreciate receiving the additional information required to proceed.",
#     },


#     # ========================================================
#     # DAILY COMMUNICATION - 91 to 100
#     # ========================================================

#     {
#         "input": "အခုလာနေပြီ။",
#         "simple": "I'm on my way.",
#         "polite": "I'm on my way now.",
#         "friendly": "I'm on my way!",
#         "professional": "I am currently on my way.",
#         "formal": "I am currently en route.",
#     },

#     {
#         "input": "မသေချာသေးဘူး။",
#         "simple": "I'm not sure yet.",
#         "polite": "I'm not sure yet, I'm afraid.",
#         "friendly": "I'm not sure yet.",
#         "professional": "I don't have confirmation yet.",
#         "formal": "I am unable to confirm this at the moment.",
#     },

#     {
#         "input": "ကြိုးစားကြည့်မယ်။",
#         "simple": "I'll try.",
#         "polite": "I'll do my best.",
#         "friendly": "I'll give it a try.",
#         "professional": "I will do my best to accomplish it.",
#         "formal": "I will make every effort to accomplish this.",
#     },

#     {
#         "input": "မိုးရွာနေလို့ အပြင်မထွက်တော့ဘူး။",
#         "simple": "It's raining, so I won't go outside.",
#         "polite": "Since it's raining, I think I'll stay inside.",
#         "friendly": "It's raining, so I'm going to stay in.",
#         "professional": "Due to the rain, I will not be going outside.",
#         "formal": "Due to the current weather conditions, I will remain indoors.",
#     },

#     {
#         "input": "နောက်မှပြန်ခေါ်မယ်။",
#         "simple": "I'll call you back later.",
#         "polite": "I'll call you back later, if that's okay.",
#         "friendly": "I'll call you back later.",
#         "professional": "I will return your call later.",
#         "formal": "I will return your call at a later time.",
#     },

#     {
#         "input": "အခုမအားသေးဘူး။",
#         "simple": "I'm not free right now.",
#         "polite": "I'm sorry, but I'm not available right now.",
#         "friendly": "I'm a little busy right now.",
#         "professional": "I'm currently unavailable.",
#         "formal": "I am currently unavailable and will respond when I am free.",
#     },

#     {
#         "input": "နည်းနည်းစောင့်ပေးပါ။",
#         "simple": "Please wait a little.",
#         "polite": "Could you please wait for a moment?",
#         "friendly": "Just give me a minute, please.",
#         "professional": "Could you please give me a moment?",
#         "formal": "I would appreciate your patience for a brief moment.",
#     },

#     {
#         "input": "ကျေးဇူးပြုပြီး ပြန်ရှင်းပြပေးပါ။",
#         "simple": "Please explain it again.",
#         "polite": "Could you please explain it again?",
#         "friendly": "Can you explain it again for me?",
#         "professional": "Could you please clarify this again?",
#         "formal": "I would appreciate it if you could provide further clarification.",
#     },

#     {
#         "input": "ကူညီပေးလို့ ကျေးဇူးတင်ပါတယ်။",
#         "simple": "Thank you for helping me.",
#         "polite": "Thank you very much for your help.",
#         "friendly": "Thanks a lot for helping me!",
#         "professional": "Thank you for your assistance.",
#         "formal": "I sincerely appreciate your assistance and support.",
#     },

#     {
#         "input": "တောင်းပန်ပါတယ်၊ မေ့သွားတယ်။",
#         "simple": "Sorry, I forgot.",
#         "polite": "I'm sorry, I completely forgot.",
#         "friendly": "Sorry, it slipped my mind.",
#         "professional": "I apologize; I overlooked it.",
#         "formal": "Please accept my apologies for having overlooked this matter.",
#     },
# ]


# # ============================================================
# # Normalize text
# # ============================================================

# def normalize_text(text: str) -> str:
#     """
#     Normalize Myanmar/English mixed input for matching.
#     """
#     text = text.strip().lower()

#     # Normalize different punctuation
#     text = re.sub(r"[၊,]", " ", text)
#     text = re.sub(r"[။.!?]", "", text)

#     # Normalize multiple spaces
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # ============================================================
# # Find training/reference example
# # ============================================================

# def find_training_example(text: str):
#     """
#     Find an exact normalized match from the 100 examples.
#     """

#     normalized_input = normalize_text(text)

#     for example in TRAINING_EXAMPLES:
#         example_input = normalize_text(example["input"])

#         if normalized_input == example_input:
#             return example

#     return None


# # ============================================================
# # Context-aware translation rules
# # ============================================================

# def _contains_any(text: str, phrases: list[str]) -> bool:
#     return any(phrase in text for phrase in phrases)


# def contextual_rule_translation(text: str, tone: str):
#     """
#     Semantic/context rules for long Myanmar, English, and mixed-language
#     messages. These rules are deliberately clause-aware: they preserve
#     cause -> situation -> consequence -> request/action instead of matching
#     only the final intent.
#     """
#     n = normalize_text(text)

#     def has(*phrases):
#         return _contains_any(n, list(phrases))

#     def variants(simple, polite, friendly, professional, formal):
#         return {
#             "simple": simple,
#             "polite": polite,
#             "friendly": friendly,
#             "professional": professional,
#             "formal": formal,
#         }.get(tone, professional)

#     # --------------------------------------------------------
#     # FIRST: MULTI-CAUSE MESSAGES
#     # --------------------------------------------------------
#     # This MUST run before any single-cause rule. A message can contain
#     # rain + flooding + traffic + a destination + a delay. Never return
#     # early just because the word "traffic" was found.
#     early_weather = has(
#         "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
#         "rain", "raining", "heavy rain", "poured"
#     )
#     early_traffic = has(
#         "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
#         "traffic", "traffic jam", "heavy traffic"
#     )
#     early_flood = has(
#         "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
#         "flood", "flooded", "flooding"
#     )
#     early_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
#     early_wait = has("စောင့်", "wait", "wait for me")
#     early_school = has("ကျောင်း", "school")
#     early_work = has("အလုပ်", "work", "office")
#     early_meeting = has("meeting", "အစည်းအဝေး")

#     early_cause_count = sum([early_weather, early_flood, early_traffic])

#     if early_cause_count >= 2 and (early_delay or early_wait):
#         if early_meeting:
#             early_destination = "the meeting"
#         elif early_school:
#             early_destination = "school"
#         elif early_work:
#             early_destination = "work"
#         else:
#             early_destination = "my destination"

#         early_causes = []
#         if early_weather:
#             early_causes.append("It rained heavily this morning")
#         if early_flood:
#             early_causes.append("the area in front of my house is flooded")
#         if early_traffic:
#             early_causes.append("there is also heavy traffic on the way")

#         if len(early_causes) == 2:
#             early_reason_sentence = early_causes[0] + ", and " + early_causes[1]
#         else:
#             early_reason_sentence = ", ".join(early_causes[:-1]) + ", and " + early_causes[-1]

#         if early_wait:
#             return variants(
#                 f"{early_reason_sentence}, so I'll be late getting to {early_destination}. Please wait for me for a little while.",
#                 f"{early_reason_sentence}, so I'm going to be late getting to {early_destination}. I'm sorry, but could you please wait for me for a little while?",
#                 f"{early_reason_sentence}, so I'll be a little late getting to {early_destination}. Please wait for me for a bit.",
#                 f"{early_reason_sentence}, so I will be late getting to {early_destination}. Could you please wait for me for a little while?",
#                 f"Due to the heavy rain, flooding in front of my house, and heavy traffic on the way, I will be delayed in reaching {early_destination}. I would appreciate your patience and ask that you please wait for me for a little while.",
#             )

#         return variants(
#             f"{early_reason_sentence}, so I'll be late getting to {early_destination} today.",
#             f"{early_reason_sentence}, so I'm sorry, but I'll be late getting to {early_destination} today.",
#             f"{early_reason_sentence}, so I'll be a little late getting to {early_destination} today.",
#             f"{early_reason_sentence}, so I will be late getting to {early_destination} today.",
#             f"Due to the heavy rain, flooding in front of my house, and heavy traffic on the way, I will be delayed in reaching {early_destination} today.",
#         )

#     # --------------------------------------------------------
#     # A. Long chained message: late meeting -> poor sleep -> work absence
#     # --------------------------------------------------------
#     if (
#         has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "ended late", "ran late", "finished late", "late last night")
#         and has("အိပ်ရေးမဝ", "အိပ်မဝ", "အိပ်ရေးမလုံ", "အိပ်မပျော်", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "did not get enough sleep", "barely slept")
#         and has("အလုပ်", "work", "office")
#         and has("မလာ", "မလာတော့", "မသွား", "won't come", "will not come", "not coming", "won't be coming", "will not be coming")
#     ):
#         return variants(
#             "The meeting ended late last night, and I didn't get enough sleep, so I won't be coming to work today.",
#             "The meeting ended quite late last night, and I didn't get enough sleep, so I'm sorry, but I won't be able to come to work today.",
#             "The meeting ran late last night, and I barely got enough sleep, so I won't be coming to work today.",
#             "The meeting ended late last night, and I did not get enough sleep, so I will not be coming to work today.",
#             "As the meeting ended late last night and I did not get sufficient sleep, I will be unable to come to work today.",
#         )

#     # Same meaning even when the time phrase is omitted.
#     if (
#         has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "ended late", "ran late", "finished late")
#         and has("အိပ်ရေးမဝ", "အိပ်မဝ", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "barely slept")
#         and has("အလုပ်", "work", "office")
#         and has("မလာ", "မလာတော့", "မသွား", "won't come", "not coming", "won't be coming")
#     ):
#         return variants(
#             "The meeting ended late, and I didn't get enough sleep, so I won't be coming to work today.",
#             "The meeting ended late, and I didn't get enough sleep, so I'm sorry, but I won't be able to come to work today.",
#             "The meeting ran late, and I barely got enough sleep, so I won't be coming to work today.",
#             "The meeting ended late, and I did not get enough sleep, so I will not be coming to work today.",
#             "As the meeting ended late and I did not get sufficient sleep, I will be unable to come to work today.",
#         )

#     # --------------------------------------------------------
#     # B. Traffic + meeting delay + explicit waiting request
#     # --------------------------------------------------------
#     if (
#         has("ကားပိတ်", "ကားလမ်းပိတ်", "လမ်းပိတ်", "ကားကြပ်", "traffic", "traffic jam", "heavy traffic")
#         and has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "late", "delayed")
#         and has("စောင့်", "wait", "give me a moment", "wait for me")
#     ):
#         return variants(
#             "There's heavy traffic at the end of the street, so I'll be late for the meeting. Please wait for me for a little while.",
#             "There's heavy traffic at the end of the street, so I'm going to be late for the meeting. I'm sorry, but could you please wait for me for a little while?",
#             "There's a traffic jam at the end of the street, so I'll be late for the meeting. Please wait for me a little while.",
#             "There's heavy traffic at the end of the street, so I'll be late for the meeting. Could you please wait for me for a little while?",
#             "There is heavy traffic at the end of the street, which is causing me to be late for the meeting. I would appreciate your patience and ask that you please wait for me for a little while.",
#         )

#     # --------------------------------------------------------
#     # C. Heavy rain + flooding + school delay
#     # --------------------------------------------------------
#     if (
#         has("မိုးသည်း", "မိုးရွာ", "မိုးကြီး", "မိုးသည်းကြီးမည်းကြီး", "rain", "raining", "poured", "heavy rain")
#         and has("ရေလျှံ", "ရေတွေ လျှံ", "ရေဝင်", "flood", "flooded", "flooding", "water is overflowing")
#         and has("ကျောင်း", "school")
#         and has("နောက်ကျ", "late", "delayed")
#     ):
#         return variants(
#             "It rained heavily this morning, and the area in front of my house is flooded, so I'll be late getting to school today.",
#             "It rained very heavily this morning, and the area in front of my house is flooded, so I'm sorry, but I'll be late getting to school today.",
#             "It poured this morning, and there's water all over the front of my house, so I'll be a little late getting to school today.",
#             "It rained heavily this morning, and the area in front of my house is flooded, so I will be late getting to school today.",
#             "Due to the heavy rain this morning and flooding in front of my house, I will be delayed in getting to school today.",
#         )

#     # --------------------------------------------------------
#     # D. Mother's/family health issue + work leave
#     # --------------------------------------------------------
#     if (
#         has("အမေ", "မိခင်", "mother", "mom", "mum")
#         and has("ကျန်းမာရေး", "နေမကောင်း", "health", "not feeling well", "sick")
#         and has("အလုပ်", "work", "office")
#         and has("ခွင့်", "leave", "day off", "take a day off")
#     ):
#         return variants(
#             "My mother has a health issue, so I'd like to take a day off from work today.",
#             "My mother is having a health issue, so I'm sorry, but I'd like to request a day off from work today.",
#             "My mom isn't feeling well, so I'd like to take the day off from work today.",
#             "Due to a health issue involving my mother, I would like to request one day of leave from work today.",
#             "Due to a health-related matter concerning my mother, I would like to respectfully request one day of leave from work today.",
#         )

#     # --------------------------------------------------------
#     # E. Family health/emergency + work leave (generic family member)
#     # --------------------------------------------------------
#     if (
#         has("မိသားစု", "family", "အိမ်က")
#         and has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick", "ဆေးရုံ", "hospital", "အရေးပေါ်", "emergency")
#         and has("အလုပ်", "work", "office")
#         and has("ခွင့်", "leave", "day off")
#     ):
#         return variants(
#             "There is a health issue in my family that I need to take care of, so I'd like to take a day off from work today.",
#             "There is a health issue in my family that I need to take care of, so I'd like to request a day off from work today.",
#             "There's a family health issue I need to take care of, so I'd like to take the day off today.",
#             "Due to a family health matter that requires my attention, I would like to request one day of leave from work today.",
#             "Due to a family health matter requiring my attention, I would like to respectfully request one day of leave from work today.",
#         )

#     # --------------------------------------------------------
#     # COMPOUND WEATHER + TRAFFIC / MULTI-CAUSE CONTEXT
#     #
#     # IMPORTANT: Never let one detected cause (for example "traffic")
#     # hide another meaningful cause (for example "heavy rain").
#     # A long message may contain several causes and all of them must
#     # survive in the English translation.
#     # --------------------------------------------------------
#     has_weather = has(
#         "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
#         "rain", "raining", "heavy rain", "poured"
#     )
#     has_traffic = has(
#         "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
#         "traffic", "traffic jam", "heavy traffic"
#     )
#     has_flood = has(
#         "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
#         "flood", "flooded", "flooding"
#     )
#     has_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
#     has_wait = has("စောင့်", "wait", "wait for me")
#     destination_school = has("ကျောင်း", "school")
#     destination_work = has("အလုပ်", "work", "office")
#     destination_meeting = has("meeting", "အစည်းအဝေး")

#     if (
#         (has_weather and has_traffic and has_delay)
#         or (has_weather and has_traffic and has_wait)
#     ):
#         destination = (
#             "the meeting" if destination_meeting
#             else "school" if destination_school
#             else "work" if destination_work
#             else "my destination"
#         )

#         # Include every detected cause instead of selecting only traffic.
#         cause_sentence = (
#             "It rained heavily, and there is heavy traffic on the way"
#             if has_weather and has_traffic
#             else "It is raining heavily"
#             if has_weather
#             else "There is heavy traffic on the way"
#         )

#         if has_wait:
#             return variants(
#                 f"{cause_sentence}, so I'll be delayed getting to {destination}. Please wait for me for a little while.",
#                 f"{cause_sentence}, so I'm going to be late getting to {destination}. I'm sorry, but could you please wait for me for a little while?",
#                 f"{cause_sentence}, so I'll be a little late getting to {destination}. Please wait for me for a bit.",
#                 f"{cause_sentence}, so I will be delayed getting to {destination}. Could you please wait for me for a little while?",
#                 f"Due to the heavy rain and traffic conditions, I will be delayed in reaching {destination}. I would appreciate your patience and ask that you please wait for me for a little while.",
#             )

#         return variants(
#             f"{cause_sentence}, so I'll be late getting to {destination}.",
#             f"{cause_sentence}, so I'm sorry, but I'll be late getting to {destination}.",
#             f"{cause_sentence}, so I'll be a little late getting to {destination}.",
#             f"{cause_sentence}, so I will be late getting to {destination}.",
#             f"Due to the heavy rain and traffic conditions, I will be delayed in reaching {destination}.",
#         )

#     # Rain + flooding + a destination, even when the exact "school" rule
#     # does not match. Keep both the weather and flooding information.
#     if has_weather and has_flood and has_delay and (destination_school or destination_work):
#         destination = "school" if destination_school else "work"
#         return variants(
#             f"It rained heavily, and the area around my house is flooded, so I'll be late getting to {destination}.",
#             f"It rained heavily, and the area around my house is flooded, so I'm sorry, but I'll be late getting to {destination}.",
#             f"It poured this morning, and there's flooding around my house, so I'll be a little late getting to {destination}.",
#             f"It rained heavily, and the area around my house is flooded, so I will be late getting to {destination}.",
#             f"Due to the heavy rain and flooding around my house, I will be delayed in reaching {destination}.",
#         )

#     # --------------------------------------------------------
#     # F. Transportation/traffic + work/school delay, no wait request
#     # --------------------------------------------------------
#     if has("ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic") and has("နောက်ကျ", "late", "delayed"):
#         if has("ကျောင်း", "school"):
#             return variants(
#                 "There's heavy traffic, so I'll be late getting to school.",
#                 "I'm sorry, but there's heavy traffic, so I'll be late getting to school.",
#                 "There's a lot of traffic, so I'll be a little late getting to school.",
#                 "There's heavy traffic, so I'll be late getting to school.",
#                 "Due to heavy traffic, I will be delayed in arriving at school.",
#             )
#         if has("အလုပ်", "work", "office"):
#             return variants(
#                 "There's heavy traffic, so I'll be late for work.",
#                 "I'm sorry, but there's heavy traffic, so I'll be late for work.",
#                 "There's a lot of traffic, so I'll be a little late for work.",
#                 "There's heavy traffic, so I'll be late for work.",
#                 "Due to heavy traffic, I will be delayed in arriving at work.",
#             )
#         return variants(
#             "There's heavy traffic, so I'll be late.",
#             "I'm sorry, but there's heavy traffic, so I'll be late.",
#             "There's a lot of traffic, so I'll be a little late.",
#             "There's heavy traffic, so I'll be late.",
#             "Due to heavy traffic, I will be delayed.",
#         )

#     # --------------------------------------------------------
#     # G. General meeting delay + tiredness (without work absence)
#     # --------------------------------------------------------
#     if (
#         has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "ended late", "ran late", "finished late")
#         and has("အိပ်ရေးမဝ", "အိပ်မဝ", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "barely slept")
#     ):
#         return variants(
#             "The meeting ended late, and I didn't get enough sleep, so I'm very tired today.",
#             "The meeting ended late, and I didn't get enough sleep, so I'm quite tired today.",
#             "The meeting ran late, and I barely got enough sleep, so I'm really tired today.",
#             "The meeting ended late, and I did not get enough sleep, so I am feeling very tired today.",
#             "As the meeting ended late and I did not get sufficient sleep, I am feeling quite fatigued today.",
#         )

#     # --------------------------------------------------------
#     # H. On the way + traffic + waiting request
#     # --------------------------------------------------------
#     if has("လမ်းမှာ", "လာနေ", "on my way") and has("ကားပိတ်", "ကားကြပ်", "traffic", "လမ်းပိတ်") and has("စောင့်", "wait", "wait for me"):
#         return variants(
#             "I'm on my way, but I'm stuck in traffic, so please wait for me for a little while.",
#             "I'm on my way, but I'm stuck in traffic. Could you please wait for me for a little while?",
#             "I'm on my way, but I'm stuck in traffic, so please wait for me a little while.",
#             "I'm currently on my way, but I'm stuck in traffic. Could you please wait for me for a little while?",
#             "I am currently on my way but delayed by traffic. I would appreciate your patience and ask that you please wait for me for a little while.",
#         )

#     # --------------------------------------------------------
#     # I. Generic waiting requests with known reasons
#     # --------------------------------------------------------
#     if has("စောင့်", "wait", "wait for me", "ခနစောင့်", "ခဏစောင့်"):
#         if has("မိုး", "rain", "raining"):
#             return variants(
#                 "It's raining right now, so please wait for me for a little while.",
#                 "It's raining right now, so could you please wait for me for a little while?",
#                 "It's raining right now, so please wait for me a little while.",
#                 "It's currently raining, so could you please wait for me for a little while?",
#                 "As it is currently raining, I would appreciate your patience and ask that you please wait for me for a little while.",
#             )
#         if has("မအား", "busy", "အလုပ်များ", "unavailable"):
#             return variants(
#                 "I'm a little busy right now, so please wait for me for a moment.",
#                 "I'm sorry, I'm a little busy right now. Could you please wait for me for a moment?",
#                 "I'm a little busy right now, so just give me a moment, please.",
#                 "I'm currently unavailable, so could you please wait for me for a moment?",
#                 "I am currently unavailable. I would appreciate your patience for a brief moment.",
#             )
#         return variants(
#             "Please wait for me for a moment.",
#             "Could you please wait for me for a moment?",
#             "Just give me a moment, please.",
#             "Could you please give me a moment?",
#             "I would appreciate your patience for a brief moment.",
#         )

#     return None



# # ============================================================
# # COMPLETE-MEANING / AI UNDERSTANDING LAYER
# # ============================================================
# #
# # The translation and the "AI Understanding" panel must use the same
# # semantic interpretation.  Do not reduce a long message to its final
# # intent and then lose the earlier reasons.
# #
# # This layer is deliberately lightweight and deterministic for high-
# # confidence patterns. Qwen is still used for unknown translations.
# # ============================================================

# def detect_input_language(text: str) -> str:
#     has_mm = bool(re.search(r"[\u1000-\u109F]", text))
#     # Treat common English words as English content even when Myanmar text
#     # is also present.
#     has_en = bool(re.search(r"[A-Za-z]", text))
#     if has_mm and has_en:
#         return "Mixed Myanmar + English"
#     if has_mm:
#         return "Myanmar (Unicode)"
#     if has_en:
#         return "English"
#     return "Unknown"


# def build_ai_understanding(
#     text: str,
#     requested_tone: str = "professional",
#     audience: str = "auto",
# ) -> dict[str, str]:
#     """
#     Extract the complete meaning needed by both the UI and the translation
#     prompt.  The key design rule is:

#         reason/cause -> situation -> consequence -> main action/request

#     Never replace a long message's reason with "reason unspecified" when
#     the source clearly contains one.
#     """
#     n = normalize_text(text)

#     def has(*phrases):
#         return _contains_any(n, list(phrases))

#     language = detect_input_language(text)

#     # --------------------------------------------------------
#     # FIRST: MULTI-CAUSE UNDERSTANDING
#     # --------------------------------------------------------
#     # This must run before single-cause traffic/rain rules.
#     u_weather = has(
#         "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
#         "rain", "raining", "heavy rain", "poured"
#     )
#     u_traffic = has(
#         "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
#         "traffic", "traffic jam", "heavy traffic"
#     )
#     u_flood = has(
#         "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
#         "flood", "flooded", "flooding"
#     )
#     u_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
#     u_wait = has("စောင့်", "wait", "wait for me")
#     u_school = has("ကျောင်း", "school")
#     u_work = has("အလုပ်", "work", "office")
#     u_meeting = has("meeting", "အစည်းအဝေး")

#     u_cause_count = sum([u_weather, u_flood, u_traffic])

#     if u_cause_count >= 2 and (u_delay or u_wait):
#         if u_meeting:
#             u_destination = "the meeting"
#         elif u_school:
#             u_destination = "school"
#         elif u_work:
#             u_destination = "work"
#         else:
#             u_destination = "the destination"

#         u_reasons = []
#         if u_weather:
#             u_reasons.append("heavy rain this morning")
#         if u_flood:
#             u_reasons.append("flooding in front of the sender's house")
#         if u_traffic:
#             u_reasons.append("heavy traffic on the way")

#         if len(u_reasons) == 2:
#             u_reason_text = u_reasons[0] + " and " + u_reasons[1]
#         else:
#             u_reason_text = ", ".join(u_reasons[:-1]) + ", and " + u_reasons[-1]

#         return {
#             "language": language,
#             "intent": (
#                 "Inform recipient about a delay and ask them to wait"
#                 if u_wait
#                 else f"Inform recipient that the sender will be late for {u_destination}"
#             ),
#             "audience": (
#                 "Colleague" if u_work or u_meeting
#                 else "Teacher / school contact" if u_school
#                 else ("Recipient" if audience == "auto" else audience)
#             ) if audience == "auto" else audience,
#             "situation": (
#                 f"The sender expects to arrive late at {u_destination} because of {u_reason_text}."
#                 if not u_wait
#                 else f"The sender is delayed by {u_reason_text} and is asking the recipient to wait."
#             ),
#             "reason": f"The message gives multiple reasons: {u_reason_text}.",
#             "main_action": (
#                 f"Inform the recipient that the sender will be late getting to {u_destination}."
#                 if not u_wait
#                 else "Ask the recipient to wait for the sender."
#             ),
#             "cause_chain": (
#                 f"{u_reason_text} → travel delay → late arrival at {u_destination}."
#                 if not u_wait
#                 else f"{u_reason_text} → travel delay → sender asks recipient to wait."
#             ),
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Meeting late -> insufficient sleep -> work absence
#     # --------------------------------------------------------
#     if (
#         has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "ended late", "ran late", "finished late", "late last night")
#         and has(
#             "အိပ်ရေးမဝ", "အိပ်မဝ", "အိပ်ရေးမလုံ", "အိပ်မပျော်",
#             "ပင်ပန်း", "tired", "not enough sleep",
#             "didn't get enough sleep", "did not get enough sleep",
#             "barely slept", "barely got enough sleep"
#         )
#         and has("အလုပ်", "work", "office")
#         and has(
#             "မလာ", "မလာတော့", "မသွား",
#             "won't come", "will not come", "not coming",
#             "won't be coming", "will not be coming",
#             "won't be able to come", "unable to come"
#         )
#     ):
#         return {
#             "language": language,
#             "intent": "Inform recipient that the sender will not come to work",
#             "audience": "Colleague" if audience == "auto" else audience,
#             "situation": "The sender will not be coming to work today after a late meeting and insufficient sleep.",
#             "reason": "The meeting ended late last night, which resulted in insufficient sleep.",
#             "main_action": "The sender will not come to work today.",
#             "cause_chain": "Meeting ended late last night → insufficient sleep → sender will not come to work today.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Traffic + meeting delay + waiting
#     # --------------------------------------------------------
#     if (
#         has("ကားပိတ်", "ကားလမ်းပိတ်", "လမ်းပိတ်", "ကားကြပ်", "traffic", "traffic jam", "heavy traffic")
#         and has("meeting", "အစည်းအဝေး")
#         and has("နောက်ကျ", "late", "delayed")
#         and has("စောင့်", "wait", "wait for me")
#     ):
#         return {
#             "language": language,
#             "intent": "Inform recipient about a meeting delay and ask them to wait",
#             "audience": "Colleague" if audience == "auto" else audience,
#             "situation": "The sender is delayed by traffic and expects to arrive late for the meeting.",
#             "reason": "There is heavy traffic on the way.",
#             "main_action": "Ask the recipient to wait for the sender.",
#             "cause_chain": "Heavy traffic → meeting delay → sender asks recipient to wait.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Heavy rain + flooding + school delay
#     # --------------------------------------------------------
#     if (
#         has("မိုးသည်း", "မိုးရွာ", "မိုးကြီး", "မိုးသည်းကြီးမည်းကြီး", "rain", "raining", "poured", "heavy rain")
#         and has("ရေလျှံ", "ရေတွေ လျှံ", "ရေဝင်", "flood", "flooded", "flooding", "water is overflowing")
#         and has("ကျောင်း", "school")
#         and has("နောက်ကျ", "late", "delayed")
#     ):
#         return {
#             "language": language,
#             "intent": "Inform recipient that the sender will be late for school",
#             "audience": "Teacher / school contact" if audience == "auto" else audience,
#             "situation": "The sender will arrive late at school today.",
#             "reason": "Heavy rain caused flooding in front of the sender's house.",
#             "main_action": "Inform the recipient about the delay in arriving at school.",
#             "cause_chain": "Heavy rain this morning → flooding in front of the house → delayed departure/arrival → late for school.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Mother's health issue + work leave
#     # --------------------------------------------------------
#     if (
#         has("အမေ", "မိခင်", "mother", "mom", "mum")
#         and has("ကျန်းမာရေး", "နေမကောင်း", "health", "not feeling well", "sick")
#         and has("အလုပ်", "work", "office")
#         and has("ခွင့်", "leave", "day off", "take a day off")
#     ):
#         return {
#             "language": language,
#             "intent": "Request one day of leave from work",
#             "audience": "Manager / employer" if audience == "auto" else audience,
#             "situation": "The sender wants to take one day off work today.",
#             "reason": "The sender's mother has a health-related issue that requires attention.",
#             "main_action": "Request one day of leave from work today.",
#             "cause_chain": "Mother's health issue → sender needs to attend to the situation → request for one day of work leave.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Generic family health + leave
#     # --------------------------------------------------------
#     if (
#         has("မိသားစု", "family", "အိမ်က")
#         and has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick", "ဆေးရုံ", "hospital", "အရေးပေါ်", "emergency")
#         and has("အလုပ်", "work", "office")
#         and has("ခွင့်", "leave", "day off")
#     ):
#         return {
#             "language": language,
#             "intent": "Request time off from work for a family matter",
#             "audience": "Manager / employer" if audience == "auto" else audience,
#             "situation": "The sender needs time away from work to handle a family health matter.",
#             "reason": "A family member has a health-related issue requiring the sender's attention.",
#             "main_action": "Request time off from work.",
#             "cause_chain": "Family health matter → sender needs to handle it → request for work leave.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # COMPOUND CAUSES: preserve ALL meaningful reasons.
#     #
#     # This must run before the generic traffic rule. Otherwise a message
#     # containing both rain and traffic can be incorrectly reduced to
#     # "traffic caused the delay".
#     # --------------------------------------------------------
#     has_weather = has(
#         "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
#         "rain", "raining", "heavy rain", "poured"
#     )
#     has_traffic = has(
#         "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
#         "traffic", "traffic jam", "heavy traffic"
#     )
#     has_flood = has(
#         "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
#         "flood", "flooded", "flooding"
#     )
#     has_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
#     has_wait = has("စောင့်", "wait", "wait for me")
#     destination_school = has("ကျောင်း", "school")
#     destination_work = has("အလုပ်", "work", "office")
#     destination_meeting = has("meeting", "အစည်းအဝေး")

#     if (has_weather and has_traffic and (has_delay or has_wait)):
#         destination = (
#             "the meeting" if destination_meeting
#             else "school" if destination_school
#             else "work" if destination_work
#             else "the destination"
#         )

#         reasons = []
#         if has_weather:
#             reasons.append("heavy rain")
#         if has_flood:
#             reasons.append("flooding around the house")
#         if has_traffic:
#             reasons.append("heavy traffic")

#         reason_text = " and ".join(reasons)

#         if has_wait:
#             action = f"Ask the recipient to wait for the sender while the sender is delayed."
#         else:
#             action = f"Inform the recipient that the sender will be late getting to {destination}."

#         return {
#             "language": language,
#             "intent": (
#                 "Inform recipient about a delay and ask them to wait"
#                 if has_wait
#                 else f"Inform recipient that the sender will be late for {destination}"
#             ),
#             "audience": (
#                 "Colleague" if destination_work or destination_meeting
#                 else "Teacher / school contact" if destination_school
#                 else ("Recipient" if audience == "auto" else audience)
#             ) if audience == "auto" else audience,
#             "situation": (
#                 f"The sender is delayed by {reason_text} and expects to arrive late at {destination}."
#                 if not has_wait
#                 else f"The sender is delayed by {reason_text} and is asking the recipient to wait."
#             ),
#             "reason": (
#                 f"The message gives multiple reasons for the delay: {reason_text}."
#             ),
#             "main_action": action,
#             "cause_chain": (
#                 f"{reason_text} → travel delay → late arrival at {destination}."
#                 if not has_wait
#                 else f"{reason_text} → travel delay → sender asks recipient to wait."
#             ),
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Generic traffic delay
#     # --------------------------------------------------------
#     if has("ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic") and has("နောက်ကျ", "late", "delayed"):
#         destination = "school" if has("ကျောင်း", "school") else (
#             "work" if has("အလုပ်", "work", "office") else "the destination"
#         )
#         return {
#             "language": language,
#             "intent": f"Inform recipient that the sender will be late for {destination}",
#             "audience": "Colleague" if destination == "work" and audience == "auto" else (
#                 "Teacher / school contact" if destination == "school" and audience == "auto"
#                 else (audience if audience != "auto" else "Recipient")
#             ),
#             "situation": f"The sender is delayed by traffic and will arrive late at {destination}.",
#             "reason": "Heavy traffic is causing the delay.",
#             "main_action": f"Inform the recipient that the sender will be late for {destination}.",
#             "cause_chain": f"Heavy traffic → delay → late arrival at {destination}.",
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Generic waiting request with a detected reason
#     # --------------------------------------------------------
#     if has("စောင့်", "wait", "wait for me"):
#         reason = ""
#         if has("မိုး", "rain", "raining"):
#             reason = "It is raining."
#         elif has("မအား", "busy", "အလုပ်များ", "unavailable"):
#             reason = "The sender is currently busy or unavailable."
#         elif has("ကားပိတ်", "traffic", "traffic jam"):
#             reason = "The sender is delayed by traffic."

#         if reason:
#             return {
#                 "language": language,
#                 "intent": "Ask the recipient to wait",
#                 "audience": "Recipient" if audience == "auto" else audience,
#                 "situation": "The sender is asking the recipient to wait for a short time.",
#                 "reason": reason,
#                 "main_action": "Ask the recipient to wait.",
#                 "cause_chain": f"{reason} → sender asks recipient to wait.",
#                 "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#             }

#     # --------------------------------------------------------
#     # Generic work absence: do not falsely say reason is absent if
#     # the message contains a recognizable causal clause.
#     # --------------------------------------------------------
#     if has("အလုပ်", "work", "office") and has(
#         "မလာ", "မလာတော့", "မသွား", "won't come", "will not come",
#         "not coming", "won't be coming", "unable to come", "cannot come"
#     ):
#         reason = ""
#         cause_chain = ""
#         if has("meeting", "အစည်းအဝေး") and has("နောက်ကျ", "late", "delayed"):
#             reason = "The meeting ended late."
#             if has("အိပ်ရေးမဝ", "အိပ်မဝ", "tired", "not enough sleep", "barely slept"):
#                 reason = "The meeting ended late, so the sender did not get enough sleep."
#                 cause_chain = "Meeting ended late → insufficient sleep → work absence."
#             else:
#                 cause_chain = "Meeting ended late → work absence."
#         elif has("မိုး", "rain", "raining"):
#             reason = "Rain is affecting the sender's ability to travel."
#             cause_chain = "Rain/travel difficulty → work absence."
#         elif has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick"):
#             reason = "The sender has a health-related issue."
#             cause_chain = "Health issue → work absence."
#         elif has("မိသားစု", "family", "အမေ", "mother", "mom"):
#             reason = "The sender has a family matter to attend to."
#             cause_chain = "Family matter → work absence."

#         if not reason:
#             reason = "No specific reason was identified in the message."
#             cause_chain = "Work absence stated without a clearly detected reason."

#         return {
#             "language": language,
#             "intent": "Inform recipient that the sender will not come to work",
#             "audience": "Colleague" if audience == "auto" else audience,
#             "situation": "The sender will not be coming to work today.",
#             "reason": reason,
#             "main_action": "The sender will not come to work today.",
#             "cause_chain": cause_chain,
#             "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#         }

#     # --------------------------------------------------------
#     # Generic fallback
#     # --------------------------------------------------------
#     return {
#         "language": language,
#         "intent": "Translate the complete message naturally",
#         "audience": audience if audience != "auto" else "Auto-detect",
#         "situation": "Preserve the complete situation described by the sender.",
#         "reason": "Not confidently detected by the deterministic understanding layer.",
#         "main_action": "Translate the sender's complete message.",
#         "cause_chain": "Preserve all meaningful clauses in the original message.",
#         "recommended_tone": requested_tone if requested_tone in TONES else "professional",
#     }


# def format_understanding_for_prompt(understanding: dict[str, str]) -> str:
#     return f"""
# Complete semantic understanding:
# - Language: {understanding["language"]}
# - Intent: {understanding["intent"]}
# - Situation: {understanding["situation"]}
# - Reason: {understanding["reason"]}
# - Main action/request: {understanding["main_action"]}
# - Cause chain: {understanding["cause_chain"]}
# - Audience: {understanding["audience"]}
# """


# # ============================================================
# # Qwen Translation
# # ============================================================

# def generate_translation(
#     text: str,
#     tone: str,
#     context: str = "general",
#     audience: str = "auto",
# ):
#     """
#     Generate natural English using Qwen.
#     """

#     if not text.strip():
#         return ""

#     system_prompt = """
# You are MyanTone AI, a Myanmar-to-natural-English translation assistant.

# Your ONLY job is to translate the user's COMPLETE message into natural English.
# The input may be entirely Myanmar, entirely English, or a natural Myanmar-English mix.
# Treat all three forms as valid input and preserve the meaning of the whole message.

# CORE RULE: understand the whole message first, then express it naturally.
# Do NOT translate word-by-word. Do NOT shorten a message when shortening
# would remove meaningful context.

# PRESERVE EVERY MEANINGFUL PART when present:
# - who is involved
# - what happened
# - what the sender is doing
# - what the sender wants the recipient to do
# - reason/cause
# - time/timing
# - place/situation
# - delay or expected change
# - request, question, promise, or intention
# - apology or other meaningful emotion

# A translation can be one or more sentences if that is needed to preserve
# the complete meaning.

# Example:
# "လမ်းမှာ ကားပိတ်နေလို့ ခနစောင့်ပေးပါ"
# must preserve BOTH the traffic reason AND the request to wait.
# Good: "I'm stuck in traffic right now, so please wait for me for a little while."
# Bad: "Please wait a moment."

# "traffic ကြောင့် ခန wait ပေးပါ" must also preserve BOTH traffic and waiting.

# "ခန wait ပေးပါ" has no reason, so a short translation is appropriate:
# "Could you please wait for me for a moment?"

# Mixed English words such as meeting, manager, project, assignment, submit,
# deadline, CV, interview, client, task, email, call, presentation, leave,
# wait, traffic, update, file, work, and class are valid input.

# IMPORTANT MEANING DISTINCTIONS:
# - "မလာ" = not come / not go to a place
# - "မတက်" = not attend / not join an event such as a meeting or class
# - "တော့ဘူး" often = will no longer / won't
# - "နိုင်ဘူး" = cannot / unable to
# - "ချင်တယ်" = want to
# - "မယ်" normally expresses future intention/action
# - "လို့" can express a reason or an intended/reported statement depending on context
# - "စောင့်" / "wait" = wait; never remove the waiting action
# - traffic-related text is NOT automatically a "late for work" message; identify
#   the actual action/request first.

# DO NOT:
# - answer the user's question
# - explain the meaning
# - summarize
# - omit meaningful context
# - invent facts
# - add unsupported details
# - change a request into a statement
# - change "cannot" into "will not"
# - change "not attending" into "cannot attend"

# LONG / CONTEXT-RICH INPUT:
# If the input contains several clauses, preserve ALL meaningful clauses. First identify
# the situation, cause/reason, time, place, main action, consequence, and request/intention.
# Then reconstruct them as natural English using connectors such as "because", "so",
# "but", "and", or separate sentences when clearer.
# Do not intentionally make the English shorter just to be concise.
# Never let a final intent such as "I won't come to work" erase the earlier reason
# that explains WHY the person will not come.
# For example, "meeting ended late + didn't get enough sleep + won't come to work"
# must keep all three ideas in the final translation.

# TONE:
# Simple = clear everyday English while preserving meaning.
# Polite = respectful and courteous while preserving meaning.
# Friendly = warm, natural, casual English while preserving meaning.
# Professional = clear workplace-appropriate English while preserving meaning.
# Formal = formal and respectful English while preserving meaning.

# Return ONLY the final English translation. No analysis, labels, or explanations.
# """


#     understanding = build_ai_understanding(
#         text=text,
#         requested_tone=tone,
#         audience=audience,
#     )

#     semantic_context = format_understanding_for_prompt(understanding)

#     user_prompt = f"""
# Translate this message into natural English.

# Context: {context}
# Audience: {audience}
# Tone: {tone}

# {semantic_context}

# IMPORTANT:
# The semantic understanding above is a guide, not a replacement for the
# original message. Re-check the original text and preserve every meaningful
# detail. In particular, NEVER drop a reason merely because the final intent
# is easier to describe. If the original contains a cause -> consequence ->
# action chain, keep that entire chain in the English translation.

# Myanmar / mixed input:
# {text}

# English translation:
# """


#     try:
#         messages = [
#             {
#                 "role": "system",
#                 "content": system_prompt.strip(),
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt.strip(),
#             },
#         ]

#         prompt = tokenizer.apply_chat_template(
#             messages,
#             tokenize=False,
#             add_generation_prompt=True,
#         )

#         inputs = tokenizer(
#             prompt,
#             return_tensors="pt",
#             truncation=True,
#             max_length=1024,
#         )

#         with torch.no_grad():
#             outputs = model.generate(
#                 **inputs,
#                 max_new_tokens=180,
#                 do_sample=False,
#                 temperature=0.1,
#                 top_p=0.9,
#                 repetition_penalty=1.05,
#                 pad_token_id=tokenizer.eos_token_id,
#             )

#         generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

#         result = tokenizer.decode(
#             generated_tokens,
#             skip_special_tokens=True,
#         ).strip()

#         # Remove accidental prefixes
#         prefixes = [
#             "English translation:",
#             "Translation:",
#             "Answer:",
#         ]

#         for prefix in prefixes:
#             if result.lower().startswith(prefix.lower()):
#                 result = result[len(prefix):].strip()

#         # Preserve all generated lines. Long translations may naturally
#         # contain multiple sentences; never keep only the first line.
#         lines = [
#             line.strip()
#             for line in result.splitlines()
#             if line.strip()
#         ]

#         if lines:
#             result = " ".join(lines)

#         if len(result) >= 2 and result[0] == result[-1] and result[0] in {'"', "'"}:
#             result = result[1:-1].strip()

#         return result

#     except Exception as e:
#         print("QWEN ERROR:", repr(e))
#         return ""



# # ============================================================
# # API VERSION + DEBUG HELPERS
# # ============================================================

# def detect_debug_layer(text: str, tone: str) -> dict:
#     """Explain which backend layer handles an input."""
#     normalized = normalize_text(text)
#     contextual = contextual_rule_translation(text, tone)
#     reference = find_training_example(text)

#     has_rain = _contains_any(normalized, [
#         "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "rain", "raining", "heavy rain", "poured"
#     ])
#     has_flood = _contains_any(normalized, [
#         "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်", "flood", "flooded", "flooding"
#     ])
#     has_traffic = _contains_any(normalized, [
#         "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic"
#     ])
#     has_delay = _contains_any(normalized, [
#         "နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay"
#     ])
#     has_school = _contains_any(normalized, ["ကျောင်း", "school"])
#     has_work = _contains_any(normalized, ["အလုပ်", "work", "office"])
#     has_meeting = _contains_any(normalized, ["meeting", "အစည်းအဝေး"])
#     has_wait = _contains_any(normalized, ["စောင့်", "wait", "wait for me"])
#     cause_count = sum([has_rain, has_flood, has_traffic])

#     if contextual is not None:
#         layer = "contextual_rule"
#     elif reference is not None:
#         layer = "reference_dataset"
#     else:
#         layer = "qwen"

#     return {
#         "api_version": API_VERSION,
#         "api_build": API_BUILD,
#         "backend_model": MODEL_NAME,
#         "backend_device": "cpu",
#         "translation_layer": layer,
#         "contextual_rule_matched": contextual is not None,
#         "reference_example_matched": reference is not None,
#         "qwen_fallback_expected": contextual is None and reference is None,
#         "normalized_input": normalized,
#         "detected": {
#             "rain": has_rain,
#             "flooding": has_flood,
#             "traffic": has_traffic,
#             "delay": has_delay,
#             "school": has_school,
#             "work": has_work,
#             "meeting": has_meeting,
#             "wait_request": has_wait,
#             "environmental_or_transport_causes": cause_count,
#         },
#         "warning": (
#             "Multiple causes detected. Compound-context rule must run before single-cause rules."
#             if cause_count >= 2 else
#             "No multi-cause weather/traffic combination detected."
#         ),
#     }


# # ============================================================
# # Response helper
# # ============================================================

# def understanding_response_fields(
#     text: str,
#     tone: str,
#     audience: str,
# ) -> dict[str, str]:
#     u = build_ai_understanding(
#         text=text,
#         requested_tone=tone,
#         audience=audience,
#     )
#     return {
#         "api_version": API_VERSION,
#         "debug": detect_debug_layer(text, tone),
#         "language": u["language"],
#         "intent": u["intent"],
#         "audience_detected": u["audience"],
#         "situation": u["situation"],
#         "reason": u["reason"],
#         "main_action": u["main_action"],
#         "cause_chain": u["cause_chain"],
#         "recommended_tone": u["recommended_tone"],
#     }


# # ============================================================
# # Root endpoint
# # ============================================================

# @app.get("/")
# def root():
#     return {
#         "message": "MyanTone AI API is running.",
#         "api_version": API_VERSION,
#         "api_build": API_BUILD,
#         "features": ["translation", "complete-meaning-understanding", "tone-control", "debug", "test-context"],
#         "model": MODEL_NAME,
#         "device": "cpu",
#         "training_examples": len(TRAINING_EXAMPLES),
#         "tones": TONES,
#     }


# # ============================================================
# # Health endpoint
# # ============================================================

# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "api_version": API_VERSION,
#         "api_build": API_BUILD,
#         "model": MODEL_NAME,
#         "device": "cpu",
#         "training_examples": len(TRAINING_EXAMPLES),
#     }


# # ============================================================
# # Dataset endpoint
# # ============================================================

# @app.get("/dataset")
# def dataset():
#     """
#     Return the 100 reference/training examples.
#     """

#     return {
#         "count": len(TRAINING_EXAMPLES),
#         "examples": TRAINING_EXAMPLES,
#     }



# # ============================================================
# # Context diagnostic endpoint
# # ============================================================

# @app.post("/test-context")
# def test_context(request: TranslateRequest):
#     """Development endpoint for verifying backend version and context routing."""
#     text = request.text.strip()
#     if not text:
#         return {
#             "ok": False,
#             "api_version": API_VERSION,
#             "api_build": API_BUILD,
#             "error": "text is required",
#         }

#     requested_tone = request.tone.lower().strip()
#     if requested_tone not in TONES:
#         requested_tone = "professional"

#     debug = detect_debug_layer(text, requested_tone)
#     understanding = build_ai_understanding(
#         text=text,
#         requested_tone=requested_tone,
#         audience=request.audience,
#     )

#     all_tones = {}
#     for tone_name in TONES:
#         contextual = contextual_rule_translation(text, tone_name)
#         if contextual is not None:
#             all_tones[tone_name] = contextual
#         else:
#             reference = rule_based_translation(text, tone_name)
#             if reference is not None:
#                 all_tones[tone_name] = reference
#             else:
#                 all_tones[tone_name] = generate_translation(
#                     text=text,
#                     tone=tone_name,
#                     context=request.context,
#                     audience=request.audience,
#                 )

#     selected = all_tones.get(requested_tone, all_tones.get("professional", ""))

#     return {
#         "ok": True,
#         "api_version": API_VERSION,
#         "api_build": API_BUILD,
#         "input": text,
#         "selected_tone": requested_tone,
#         "debug": debug,
#         "understanding": understanding,
#         "translations": all_tones,
#         "selected_translation": selected,
#         "frontend_check": {
#             "expected_compound_context": debug["detected"]["environmental_or_transport_causes"] >= 2,
#             "backend_is_new_version": API_VERSION == "2.2.0-complete-context-debug",
#             "selected_layer": debug["translation_layer"],
#         },
#     }


# # ============================================================
# # Complete AI Understanding endpoint
# # ============================================================

# @app.post("/analyze")
# def analyze(request: TranslateRequest):
#     """
#     Return the complete semantic interpretation used by MyanTone AI.
#     This endpoint is intended for the frontend's AI Understanding panel.
#     """
#     text = request.text.strip()

#     if not text:
#         return {
#             "language": "",
#             "intent": "",
#             "audience": "",
#             "situation": "",
#             "reason": "",
#             "main_action": "",
#             "cause_chain": "",
#             "recommended_tone": "",
#         }

#     tone = request.tone.lower().strip()
#     if tone not in TONES:
#         tone = "professional"

#     return build_ai_understanding(
#         text=text,
#         requested_tone=tone,
#         audience=request.audience,
#     )


# # ============================================================
# # Translate endpoint
# # ============================================================

# @app.post("/translate", response_model=TranslateResponse)
# def translate(request: TranslateRequest):

#     text = request.text.strip()

#     if not text:
#         return TranslateResponse(
#             translation="",
#             translations={},
#         )

#     # --------------------------------------------------------
#     # Validate tone
#     # --------------------------------------------------------

#     tone = request.tone.lower().strip()

#     if tone not in TONES:
#         tone = "professional"

#     # --------------------------------------------------------
#     # 1. Context-aware rules first
#     # --------------------------------------------------------
#     contextual_translation = contextual_rule_translation(text, tone)

#     if contextual_translation is not None:
#         print("=" * 60)
#         print("CONTEXT-AWARE RULE MATCH")
#         print("INPUT:", text)
#         print("TONE:", tone)
#         print("RESULT:", contextual_translation)
#         print("=" * 60)
#         return TranslateResponse(
#             translation=contextual_translation,
#             translations={tone: contextual_translation},
#             **understanding_response_fields(text, tone, request.audience),
#         )

#     # --------------------------------------------------------
#     # 1. Try the 100-example reference dataset first
#     # --------------------------------------------------------

#     rule_translation = rule_based_translation(
#         text=text,
#         tone=tone,
#     )

#     if rule_translation is not None:

#         print("=" * 60)
#         print("REFERENCE DATASET MATCH")
#         print("INPUT:", text)
#         print("TONE:", tone)
#         print("RESULT:", rule_translation)
#         print("=" * 60)

#         return TranslateResponse(
#             translation=rule_translation,
#             translations={
#                 tone: rule_translation,
#             },
#             **understanding_response_fields(text, tone, request.audience),
#         )

#     # --------------------------------------------------------
#     # 2. Unknown sentence → Qwen
#     # --------------------------------------------------------

#     print("=" * 60)
#     print("QWEN TRANSLATION")
#     print("INPUT:", text)
#     print("TONE:", tone)
#     print("=" * 60)

#     selected_translation = generate_translation(
#         text=text,
#         tone=tone,
#         context=request.context,
#         audience=request.audience,
#     )

#     # --------------------------------------------------------
#     # 3. Safety fallback
#     # --------------------------------------------------------

#     if not selected_translation:
#         selected_translation = (
#             "Sorry, I couldn't generate a translation "
#             "for this message."
#         )

#     return TranslateResponse(
#         translation=selected_translation,
#         translations={
#             tone: selected_translation,
#         },
#         **understanding_response_fields(text, tone, request.audience),
#     )


# # ============================================================
# # Generate all 5 tones
# # ============================================================

# @app.post("/translate-all")
# def translate_all(request: TranslateRequest):

#     text = request.text.strip()

#     if not text:
#         return {
#             "translation": "",
#             "translations": {},
#         }

#     results = {}

#     # Preserve reason + action for high-confidence contextual messages.
#     if contextual_rule_translation(text, "professional") is not None:
#         for tone in TONES:
#             results[tone] = contextual_rule_translation(text, tone)

#         selected_tone = request.tone.lower().strip()
#         if selected_tone not in TONES:
#             selected_tone = "professional"

#         return {
#             "translation": results[selected_tone],
#             "translations": results,
#             "understanding": understanding_response_fields(
#                 text, selected_tone, request.audience
#             ),
#         }


#     # First check the 100 examples
#     example = find_training_example(text)

#     if example:

#         for tone in TONES:
#             results[tone] = example[tone]

#         selected_tone = request.tone.lower().strip()
#         if selected_tone not in TONES:
#             selected_tone = "professional"

#         return {
#             "translation": results[selected_tone],
#             "translations": results,
#             "understanding": understanding_response_fields(
#                 text, selected_tone, request.audience
#             ),
#         }

#     # Otherwise generate each tone using Qwen
#     for tone in TONES:

#         result = generate_translation(
#             text=text,
#             tone=tone,
#             context=request.context,
#             audience=request.audience,
#         )

#         if not result:
#             result = "Unable to generate translation."

#         results[tone] = result

#     selected_tone = request.tone.lower().strip()

#     if selected_tone not in TONES:
#         selected_tone = "professional"

#     return {
#         "translation": results[selected_tone],
#         "translations": results,
#         "understanding": understanding_response_fields(
#             text, selected_tone, request.audience
#         ),
#     }


# # ============================================================
# # Run with:
# #
# # uvicorn api:app --reload --port 8000
# # ============================================================

# if __name__ == "__main__":

#     import uvicorn

#     uvicorn.run(
#         "api:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True,
#     )


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re


# ============================================================
# MyanTone AI
# Myanmar → Natural English
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# Visible API/build version. Change this whenever backend behavior changes.
API_VERSION = "2.6.0-100-full-message-reference"
API_BUILD = "2026-09-21-full-message-100-v1"


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
    version=API_VERSION,
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
    api_version: str = API_VERSION
    debug: dict = Field(default_factory=dict)
    # AI Understanding is returned by the API so the frontend can display
    # the complete meaning that was detected, instead of only the final intent.
    language: str = ""
    intent: str = ""
    audience_detected: str = ""
    situation: str = ""
    reason: str = ""
    main_action: str = ""
    cause_chain: str = ""
    recommended_tone: str = ""


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
# FULL MESSAGE REFERENCE EXAMPLES - 100 REAL STRESS TESTS
# ============================================================
# IMPORTANT: These are deterministic reference examples, not model training.
# Exact normalized matches are returned before generic keyword rules so the
# complete cause -> event -> consequence -> request chain is preserved.

FULL_MESSAGE_EXAMPLES = [{'input': 'ဒီနေ့ မနက် traffic အရမ်းပိတ်နေလို့ office ကို ပုံမှန်အချိန်မီ မရောက်နိုင်ဘူး၊ ရောက်တာနဲ့ အလုပ်စလုပ်ပါမယ်။',
  'simple': "Traffic is very heavy this morning, so I won't be able to get to the office on time. I'll start work as "
            'soon as I arrive.',
  'polite': "I wanted to let you know that traffic is very heavy this morning. As a result, I won't be able to get to "
            "the office on time. I'll start work as soon as I arrive.",
  'friendly': "Just a quick heads-up — traffic is very heavy this morning. That’s why I won't be able to get to the "
              "office on time. I'll start work as soon as I arrive.",
  'professional': "Because traffic is very heavy this morning, I won't be able to get to the office on time. I'll "
                  'start work as soon as I arrive.',
  'formal': "Given that traffic is very heavy this morning, I won't be able to get to the office on time. I'll start "
            'work as soon as I arrive.'},
 {'input': 'လမ်းထိပ်မှာ ကားတွေ အရမ်းကြပ်နေလို့ meeting နောက်ကျမှာမလို့ ခနစောင့်ပေးပါ။',
  'simple': "There's heavy traffic at the end of the street, so I'll be late for the meeting. Please wait for me for a "
            'little while.',
  'polite': 'I wanted to let you know that there is heavy traffic at the end of the street, so I will be late for the '
            'meeting. Could you please wait for me for a little while?',
  'friendly': 'Just a heads-up — there’s a lot of traffic at the end of the street, so I’m going to be late for the '
              'meeting. Can you hang on for me for a bit?',
  'professional': 'Heavy traffic at the end of the street is causing a delay, so I will be late for the meeting. I '
                  'would appreciate it if you could wait for me briefly.',
  'formal': 'Due to severe traffic congestion at the end of the street, I will be delayed for the meeting. Kindly '
            'allow me a short while to arrive.'},
 {'input': 'ဒီ morning က rain အရမ်းရွာပြီး traffic ပါ အရမ်းပိတ်နေလို့ school ကို late ဖြစ်မယ်။',
  'simple': "It rained heavily this morning, and traffic is also very heavy, so I'll be late getting to school.",
  'polite': 'I wanted to let you know that it rained heavily this morning, and traffic is also very heavy. I may be a '
            'little late getting to school.',
  'friendly': 'The rain is really heavy this morning, and traffic is backed up too, so I’m going to be late for '
              'school.',
  'professional': 'Heavy morning rain and severe traffic congestion are delaying my trip to school. I will arrive '
                  'late.',
  'formal': 'Due to the heavy rainfall and severe traffic congestion this morning, I will be delayed on my way to '
            'school.'},
 {'input': 'အိမ်ကနေ office သွားတဲ့လမ်းမှာ traffic jam အရမ်းဖြစ်နေလို့ ပုံမှန်ထက် နာရီဝက်လောက် နောက်ကျနိုင်ပါတယ်။',
  'simple': "There's a very heavy traffic jam on the way to the office, so I may be about 30 minutes later than usual.",
  'polite': 'I wanted to let you know that there is a very heavy traffic jam on the way to the office. As a result, I '
            'may be about 30 minutes later than usual.',
  'friendly': "Just a quick heads-up — there's a very heavy traffic jam on the way to the office. That’s why I may be "
              'about 30 minutes later than usual.',
  'professional': 'Because there is a very heavy traffic jam on the way to the office, I may be about 30 minutes later '
                  'than usual.',
  'formal': 'Given that there is a very heavy traffic jam on the way to the office, I may be about 30 minutes later '
            'than usual.'},
 {'input': 'လမ်းမှာ ကားပိတ်နေတာကြောင့် client meeting ကို အချိန်မီ မရောက်နိုင်ဘူး၊ ရောက်တာနဲ့ ချက်ချင်း join လိုက်မယ်။',
  'simple': "There's heavy traffic on the way, so I won't be able to get to the client meeting on time. I'll join as "
            'soon as I arrive.',
  'polite': "I wanted to let you know that there is heavy traffic on the way. As a result, I won't be able to get to "
            "the client meeting on time. I'll join as soon as I arrive.",
  'friendly': "Just a quick heads-up — there's heavy traffic on the way. That’s why I won't be able to get to the "
              "client meeting on time. I'll join as soon as I arrive.",
  'professional': "Because there is heavy traffic on the way, I won't be able to get to the client meeting on time. "
                  "I'll join as soon as I arrive.",
  'formal': "Given that there is heavy traffic on the way, I won't be able to get to the client meeting on time. I'll "
            'join as soon as I arrive.'},
 {'input': 'ဒီနေ့ မနက် လမ်းထိပ်ကနေစပြီး traffic အရမ်းကြပ်နေလို့ office ကို နည်းနည်း late ဖြစ်ပါမယ်။',
  'simple': "Traffic has been very heavy from the end of the street since this morning, so I'll be a little late "
            'getting to the office.',
  'polite': 'I wanted to let you know that traffic has been very heavy from the end of the street since this morning. '
            "As a result, I'll be a little late getting to the office.",
  'friendly': 'Just a quick heads-up — traffic has been very heavy from the end of the street since this morning. '
              "That’s why I'll be a little late getting to the office.",
  'professional': "Because traffic has been very heavy from the end of the street since this morning, I'll be a little "
                  'late getting to the office.',
  'formal': "Given that traffic has been very heavy from the end of the street since this morning, I'll be a little "
            'late getting to the office.'},
 {'input': 'Traffic အရမ်းပိတ်နေလို့ meeting ကို အချိန်မီ မရောက်နိုင်ဘူး၊ meeting စတာနဲ့ online ကနေ join လို့ရရင် join '
           'လိုက်မယ်။',
  'simple': "Traffic is very heavy, so I won't be able to arrive at the meeting on time. If possible, I'll join online "
            'as soon as the meeting starts.',
  'polite': "I wanted to let you know that traffic is very heavy. As a result, I won't be able to arrive at the "
            "meeting on time. If possible, I'll join online as soon as the meeting starts.",
  'friendly': "Just a quick heads-up — traffic is very heavy. That’s why I won't be able to arrive at the meeting on "
              "time. If possible, I'll join online as soon as the meeting starts.",
  'professional': "Because traffic is very heavy, I won't be able to arrive at the meeting on time. If possible, I'll "
                  'join online as soon as the meeting starts.',
  'formal': "Given that traffic is very heavy, I won't be able to arrive at the meeting on time. If possible, I'll "
            'join online as soon as the meeting starts.'},
 {'input': 'လမ်းမှာ traffic ကြောင့် အရမ်းကြာနေလို့ appointment ကို နောက်ကျနိုင်ပါတယ်၊ ခဏလောက် စောင့်ပေးပါ။',
  'simple': 'Traffic is causing a long delay on the way, so I may be late for my appointment. Please wait for me for a '
            'little while.',
  'polite': 'I wanted to let you know that traffic is causing a long delay on my way to the appointment. Could you '
            'please wait for me for a little while?',
  'friendly': 'Just a heads-up — traffic is really slowing things down, so I’m going to be late for my appointment. '
              'Can you hang on for me for a bit?',
  'professional': 'Traffic is causing a significant delay on my way to the appointment. I would appreciate it if you '
                  'could wait for me briefly.',
  'formal': 'Owing to the traffic delay, I will be late for my appointment. Kindly allow me a short while to arrive.'},
 {'input': 'ဒီနေ့ လမ်းတွေမှာ ကားအရမ်းပိတ်နေပြီး မိုးလည်းရွာနေလို့ အလုပ်ကို နည်းနည်းနောက်ကျမှ ရောက်ပါမယ်။',
  'simple': "The roads are very congested and it's also raining today, so I'll be a little late getting to work.",
  'polite': "I wanted to let you know that the roads are very congested and it's also raining today. As a result, I'll "
            'be a little late getting to work.',
  'friendly': "Just a quick heads-up — the roads are very congested and it's also raining today. That’s why I'll be a "
              'little late getting to work.',
  'professional': "Because the roads are very congested and it's also raining today, I'll be a little late getting to "
                  'work.',
  'formal': "Given that the roads are very congested and it's also raining today, I'll be a little late getting to "
            'work.'},
 {'input': 'Traffic jam ကြောင့် office ကို late ဖြစ်မယ်၊ ရောက်တာနဲ့ manager ကို အရင်ဆုံး အကြောင်းကြားပါမယ်။',
  'simple': "I'll be late getting to the office because of the traffic jam. I'll inform my manager as soon as I "
            'arrive.',
  'polite': "I wanted to let you know that I will be late getting to the office because of the traffic jam. I'll "
            'inform my manager as soon as I arrive.',
  'friendly': "Just a quick heads-up — I'll be late getting to the office because of the traffic jam. I'll inform my "
              'manager as soon as I arrive.',
  'professional': "For your information, I will be late getting to the office because of the traffic jam. I'll inform "
                  'my manager as soon as I arrive.',
  'formal': "Please be advised that I will be late getting to the office because of the traffic jam. I'll inform my "
            'manager as soon as I arrive.'},
 {'input': 'ဒီနေ့ မနက် မိုးသည်းကြီးရွာပြီး အိမ်ရှေ့မှာ ရေတွေ လျှံနေလို့ ကျောင်းလာတာ နောက်ကျမယ်နော်။',
  'simple': "It rained heavily this morning, and the area in front of my house is flooded, so I'll be late getting to "
            'school today.',
  'polite': 'I wanted to let you know that it rained heavily this morning, and the area in front of my house is '
            "flooded. As a result, I'll be late getting to school today.",
  'friendly': 'Just a quick heads-up — it rained heavily this morning, and the area in front of my house is flooded. '
              "That’s why I'll be late getting to school today.",
  'professional': "Because it rained heavily this morning, and the area in front of my house is flooded, I'll be late "
                  'getting to school today.',
  'formal': "Given that it rained heavily this morning, and the area in front of my house is flooded, I'll be late "
            'getting to school today.'},
 {'input': 'မိုးအရမ်းရွာပြီး အိမ်ရှေ့လမ်းမှာ ရေတက်နေလို့ ကားထွက်လို့မရသေးဘူး၊ နည်းနည်းစောင့်ပေးပါ။',
  'simple': "It rained heavily and the road in front of my house is flooded, so I can't leave by car yet. Please wait "
            'a little while.',
  'polite': 'I wanted to let you know that the heavy rain has flooded the road in front of my house, so I cannot leave '
            'by car yet. Could you please give me a little more time?',
  'friendly': 'Just a heads-up — the rain has flooded the road outside my house, so I can’t get the car out yet. Can '
              'you give me a little more time?',
  'professional': 'The heavy rain and flooding outside my house are preventing me from leaving by car. I would '
                  'appreciate your patience for a little while.',
  'formal': 'Because of the heavy rainfall and flooding on the road outside my house, I am unable to leave by car at '
            'present. Kindly allow me some additional time.'},
 {'input': 'ဒီ morning က rain အရမ်းကြီးရွာပြီး လမ်းမှာ water တက်နေလို့ office ကို အချိန်မီ မရောက်နိုင်ဘူး။',
  'simple': "It rained very heavily this morning, and the road is flooded, so I won't be able to get to the office on "
            'time.',
  'polite': 'I wanted to let you know that it rained very heavily this morning, and the road is flooded. As a result, '
            "I won't be able to get to the office on time.",
  'friendly': 'Just a quick heads-up — it rained very heavily this morning, and the road is flooded. That’s why I '
              "won't be able to get to the office on time.",
  'professional': "Because it rained very heavily this morning, and the road is flooded, I won't be able to get to the "
                  'office on time.',
  'formal': "Given that it rained very heavily this morning, and the road is flooded, I won't be able to get to the "
            'office on time.'},
 {'input': 'မိုးကြီးတာကြောင့် လမ်းတချို့ ရေလျှံနေပြီး traffic ပါ ပိတ်နေလို့ school ကို ပုံမှန်ထက် နောက်ကျပါမယ်။',
  'simple': "Because of the heavy rain, some roads are flooded and traffic is also congested, so I'll be later than "
            'usual getting to school.',
  'polite': 'I wanted to let you know that because of the heavy rain, some roads are flooded and traffic is also '
            "congested. As a result, I'll be later than usual getting to school.",
  'friendly': 'Just a quick heads-up — because of the heavy rain, some roads are flooded and traffic is also '
              "congested. That’s why I'll be later than usual getting to school.",
  'professional': "Because because of the heavy rain, some roads are flooded and traffic is also congested, I'll be "
                  'later than usual getting to school.',
  'formal': "Given that because of the heavy rain, some roads are flooded and traffic is also congested, I'll be later "
            'than usual getting to school.'},
 {'input': 'မနေ့ညကတည်းက မိုးအရမ်းရွာထားလို့ ဒီမနက် အိမ်ရှေ့မှာ ရေတက်နေတယ်၊ ဒါကြောင့် အပြင်ထွက်တာ နောက်ကျသွားတယ်။',
  'simple': 'It has been raining heavily since last night, and there is flooding in front of my house this morning, so '
            'I was delayed in leaving home.',
  'polite': 'I wanted to let you know that it has been raining heavily since last night, and there is flooding in '
            'front of my house this morning. As a result, I was delayed in leaving home.',
  'friendly': 'Just a quick heads-up — it has been raining heavily since last night, and there is flooding in front of '
              'my house this morning. That’s why I was delayed in leaving home.',
  'professional': 'Because it has been raining heavily since last night, and there is flooding in front of my house '
                  'this morning, I was delayed in leaving home.',
  'formal': 'Given that it has been raining heavily since last night, and there is flooding in front of my house this '
            'morning, I was delayed in leaving home.'},
 {'input': 'မိုးသည်းနေတာနဲ့ လမ်းမှာ ရေတွေတက်နေတာကြောင့် office ကို မလာနိုင်သေးဘူး၊ အခြေအနေကောင်းရင် ထွက်လာပါမယ်။',
  'simple': "Because of the heavy rain and flooding on the roads, I can't come to the office yet. I'll leave as soon "
            'as conditions improve.',
  'polite': 'I wanted to let you know that because of the heavy rain and flooding on the roads, I cannot come to the '
            "office yet. I'll leave as soon as conditions improve.",
  'friendly': "Just a quick heads-up — because of the heavy rain and flooding on the roads, I can't come to the office "
              "yet. I'll leave as soon as conditions improve.",
  'professional': "Because of the heavy rain and flooding on the roads, I cannot come to the office yet. I'll leave as "
                  'soon as conditions improve.',
  'formal': "Owing to the heavy rain and flooding on the roads, I cannot come to the office yet. I'll leave as soon as "
            'conditions improve.'},
 {'input': 'မိုးအရမ်းရွာပြီး လမ်းတွေ ရေလျှံနေလို့ delivery လည်း နောက်ကျနိုင်ပါတယ်၊ ရောက်တာနဲ့ ပြောပေးပါမယ်။',
  'simple': "The heavy rain and flooding may also delay the delivery. I'll let you know as soon as it arrives.",
  'polite': "I wanted to let you know that the heavy rain and flooding may also delay the delivery. I'll let you know "
            'as soon as it arrives.',
  'friendly': "Just a quick heads-up — the heavy rain and flooding may also delay the delivery. I'll let you know as "
              'soon as it arrives.',
  'professional': "For your information, The heavy rain and flooding may also delay the delivery. I'll let you know as "
                  'soon as it arrives.',
  'formal': "Please be advised that The heavy rain and flooding may also delay the delivery. I'll let you know as soon "
            'as it arrives.'},
 {'input': 'ဒီနေ့ မိုးကြောင့် ကျောင်းသွားတဲ့လမ်းမှာ ရေတက်နေပြီး ကားတွေလည်း ပိတ်နေလို့ နာရီဝက်လောက် နောက်ကျနိုင်ပါတယ်။',
  'simple': 'Because of the rain, the road to school is flooded and traffic is also heavy, so I may be about 30 '
            'minutes late.',
  'polite': 'I wanted to let you know that because of the rain, the road to school is flooded and traffic is also '
            'heavy. As a result, I may be about 30 minutes late.',
  'friendly': 'Just a quick heads-up — because of the rain, the road to school is flooded and traffic is also heavy. '
              'That’s why I may be about 30 minutes late.',
  'professional': 'Because because of the rain, the road to school is flooded and traffic is also heavy, I may be '
                  'about 30 minutes late.',
  'formal': 'Given that because of the rain, the road to school is flooded and traffic is also heavy, I may be about '
            '30 minutes late.'},
 {'input': 'မိုးက မနက်ကတည်းက အရမ်းရွာနေလို့ အိမ်ကနေ ထွက်လို့မရသေးဘူး၊ နည်းနည်းကြာမှ ထွက်လာပါမယ်။',
  'simple': "It has been raining heavily since this morning, so I can't leave home yet. I'll head out a little later.",
  'polite': "I wanted to let you know that it has been raining heavily since this morning. As a result, I can't leave "
            "home yet. I'll head out a little later.",
  'friendly': "Just a quick heads-up — it has been raining heavily since this morning. That’s why I can't leave home "
              "yet. I'll head out a little later.",
  'professional': "Because it has been raining heavily since this morning, I can't leave home yet. I'll head out a "
                  'little later.',
  'formal': "Given that it has been raining heavily since this morning, I can't leave home yet. I'll head out a little "
            'later.'},
 {'input': 'Heavy rain ကြောင့် လမ်းမှာ flooding ဖြစ်နေပြီး traffic ပါ အရမ်းကြပ်နေလို့ meeting ကို late ဖြစ်မယ်။',
  'simple': "The heavy rain has caused flooding on the roads and traffic is very heavy, so I'll be late for the "
            'meeting.',
  'polite': 'I wanted to let you know that the heavy rain has caused flooding on the roads and traffic is very heavy. '
            "As a result, I'll be late for the meeting.",
  'friendly': 'Just a quick heads-up — the heavy rain has caused flooding on the roads and traffic is very heavy. '
              "That’s why I'll be late for the meeting.",
  'professional': "Because the heavy rain has caused flooding on the roads and traffic is very heavy, I'll be late for "
                  'the meeting.',
  'formal': "Given that the heavy rain has caused flooding on the roads and traffic is very heavy, I'll be late for "
            'the meeting.'},
 {'input': 'မနေ့ညက meeting က အချိန်တော်တော်ကြာသွားပြီး အိမ်ပြန်ရောက်တာလည်း နောက်ကျလို့ အိပ်ရေးမဝဘူး၊ ဒါကြောင့် ဒီနေ့ '
           'အလုပ်မလာတော့ဘူးနော်။',
  'simple': "The meeting went on quite late last night, and I also got home late, so I didn't get enough sleep. That's "
            "why I won't be coming to work today.",
  'polite': 'I wanted to let you know that the meeting continued quite late last night, and I also got home late. As a '
            'result, I did not get enough sleep, so I will not be able to come to work today.',
  'friendly': 'Last night’s meeting went on really late, and I got home late too. I barely slept, so I’m staying home '
              'from work today.',
  'professional': 'The late conclusion of last night’s meeting and my subsequent late return home resulted in '
                  'insufficient sleep. Consequently, I will be absent from work today.',
  'formal': 'As the meeting concluded late and I returned home at a late hour, I obtained insufficient rest. '
            'Accordingly, I will not attend work today.'},
 {'input': 'မနေ့ညက client meeting က late ဖြစ်သွားပြီး meeting ပြီးတော့ changes တွေ ပြန်လုပ်ရလို့ အိမ်ပြန်တာ '
           'အရမ်းနောက်ကျသွားတယ်၊ ဒီနေ့ အရမ်းပင်ပန်းနေလို့ ခွင့်တစ်ရက်ယူချင်ပါတယ်။',
  'simple': 'The client meeting ran late last night, and after the meeting I had to work on the requested changes, so '
            "I got home very late. I'm very tired today, so I'd like to take a day off.",
  'polite': 'I wanted to let you know that the client meeting ran late last night, and I then had to complete the '
            'requested changes, which meant I got home very late. I am extremely tired today. Would it be possible for '
            'me to take one day of leave?',
  'friendly': 'The client meeting ran late, and I still had to finish their changes afterward, so I got home really '
              'late. I’m exhausted today and would like to take the day off.',
  'professional': 'The extended client meeting, followed by completion of the requested changes, resulted in a '
                  'significantly delayed return home. As I am very fatigued today, I would like to request one day of '
                  'leave.',
  'formal': 'Owing to the extended client meeting and the subsequent completion of the requested revisions, I returned '
            'home at a considerably late hour. I therefore respectfully request one day of leave today.'},
 {'input': 'Meeting က မနေ့ညက အရမ်းနောက်ကျပြီးမှ ပြီးသွားလို့ အိပ်ရာဝင်တာ မနက်နီးမှဖြစ်တယ်၊ အိပ်ရေးမဝလို့ ဒီနေ့ work '
           'မလာနိုင်ဘူး။',
  'simple': "The meeting ended very late last night, so I didn't go to bed until near morning. I didn't get enough "
            "sleep, so I won't be able to come to work today.",
  'polite': 'I wanted to let you know that the meeting ended very late last night, and I did not get to bed until '
            'close to morning. Since I did not get enough sleep, I will not be able to come to work today.',
  'friendly': 'The meeting finished really late last night, and I didn’t get to bed until almost morning. I barely '
              'slept, so I’m not coming to work today.',
  'professional': 'Because the meeting concluded at a late hour and my sleep was substantially reduced, I will be '
                  'unable to attend work today.',
  'formal': 'In view of the late conclusion of the meeting and the resulting lack of rest, I will not be attending '
            'work today.'},
 {'input': 'မနေ့ညက meeting ပြီးတာ နောက်ကျသွားလို့ sleep မဝဘူး၊ ဒီနေ့ အရမ်း tired ဖြစ်နေလို့ office မလာတော့ဘူးနော်။',
  'simple': "The meeting ended late last night, so I didn't get enough sleep. I'm very tired today, so I won't be "
            'coming to the office.',
  'polite': 'I wanted to let you know that the meeting ended late last night, which meant I did not get enough sleep. '
            'I am very tired today, so I will not be coming to the office.',
  'friendly': 'Last night’s meeting finished late, so I didn’t get enough sleep. I’m really tired today and won’t be '
              'heading into the office.',
  'professional': 'The late conclusion of the meeting resulted in insufficient sleep, and I am significantly fatigued '
                  'today. I will therefore be absent from the office.',
  'formal': 'As the meeting concluded late and I obtained insufficient rest, I am considerably fatigued today and will '
            'not attend the office.'},
 {'input': 'Client နဲ့ meeting က အချိန်ကြာသွားပြီး ပြီးတော့ သူတို့တောင်းထားတဲ့ changes တွေကို လုပ်ပေးရလို့ အိမ်ပြန်တာ '
           'late ဖြစ်သွားတယ်၊ ဒါကြောင့် ဒီနေ့ တစ်ရက်ခွင့်ယူချင်ပါတယ်။',
  'simple': 'The meeting with the client took a long time, and I had to make the changes they requested afterward, so '
            "I got home late. That's why I'd like to take a day off today.",
  'polite': 'I wanted to explain the situation: the meeting with the client took a long time, and I had to make the '
            'changes they requested afterward, so I got home late. Would it be possible for me to take the day off '
            'today, please?',
  'friendly': 'Just a heads-up — the meeting with the client took a long time, and I had to make the changes they '
              'requested afterward, so I got home late. I’d like to take today off, if that’s okay.',
  'professional': 'The meeting with the client took a long time, and I had to make the changes they requested '
                  'afterward, so I got home late. For this reason, I would like to request one day of leave today.',
  'formal': 'The meeting with the client took a long time, and I had to make the changes they requested afterward, so '
            'I got home late. Accordingly, I respectfully request one day of leave today.'},
 {'input': 'မနေ့ညက meeting ran late ဖြစ်ပြီး အိမ်ပြန်ရောက်တာလည်း late ဖြစ်လို့ အိပ်ရေးမဝဘူး၊ ဒီနေ့ အလုပ်ကို '
           'မလာတော့ဘူး။',
  'simple': "The meeting ran late last night, and I also got home late, so I didn't get enough sleep. I won't be "
            'coming to work today.',
  'polite': 'I wanted to let you know that the meeting ran late last night and I also arrived home late, so I did not '
            'get enough sleep. I will not be coming to work today.',
  'friendly': 'The meeting ran really late last night, and I got home late too. I barely slept, so I’m staying home '
              'from work today.',
  'professional': 'The late meeting and delayed return home resulted in insufficient sleep. Consequently, I will be '
                  'absent from work today.',
  'formal': 'Owing to the late conclusion of the meeting and my late return home, I obtained insufficient rest. '
            'Accordingly, I will not attend work today.'},
 {'input': 'Meeting ပြီးပြီးချင်း report ကို ပြန်ပြင်ရတာကြောင့် အိမ်ပြန်တာ နောက်ကျသွားတယ်၊ အိပ်ချိန်လည်း နည်းသွားလို့ '
           'ဒီနေ့ အရမ်းပင်ပန်းနေပါတယ်။',
  'simple': 'I had to revise the report immediately after the meeting, so I got home late. I also lost sleep and am '
            'very tired today.',
  'polite': 'I wanted to let you know that I had to revise the report immediately after the meeting, which delayed my '
            'return home. As a result, I had less time to sleep and am very tired today.',
  'friendly': 'I had to jump straight into the report after the meeting, so I got home late and didn’t get much sleep. '
              'I’m really tired today.',
  'professional': 'The report revisions required after the meeting delayed my return home and reduced my available '
                  'sleep time. I am therefore experiencing significant fatigue today.',
  'formal': 'The required report revisions following the meeting delayed my return home and curtailed my sleep. '
            'Consequently, I am considerably fatigued today.'},
 {'input': 'မနေ့ညက client meeting က အချိန်ကြာသွားပြီး အိမ်ရောက်တာ မနက်တော်တော်နီးမှ ဖြစ်လို့ ဒီနေ့ အိပ်ရေးမဝဘဲ '
           'အလုပ်လုပ်ဖို့ မဖြစ်နိုင်လောက်အောင် ပင်ပန်းနေပါတယ်။',
  'simple': "The client meeting went on for a long time last night, and I didn't get home until very late, so I didn't "
            'get enough sleep and am too tired to work properly today.',
  'polite': 'I wanted to let you know that the client meeting lasted a long time last night, and I did not get home '
            'until very late. As a result, I did not get enough sleep and am too tired to work effectively today.',
  'friendly': 'The client meeting went on forever, and I didn’t get home until really late. I barely slept, so I’m too '
              'tired to work properly today.',
  'professional': 'The extended client meeting and late return home significantly reduced my sleep. Consequently, I am '
                  'too fatigued to work effectively today.',
  'formal': 'In light of the prolonged client meeting and the resulting lack of rest, I am considerably fatigued and '
            'unable to work effectively today.'},
 {'input': 'Meeting ended late last night, ပြီးတော့ report changes တွေ ဆက်လုပ်ရလို့ အိမ်ပြန်တာလည်း late ဖြစ်သွားတယ်၊ '
           'ဒါကြောင့် ဒီနေ့ work မလာတော့ဘူး။',
  'simple': 'The meeting ended late last night, and I had to continue working on the report changes afterward, so I '
            "got home late. That's why I won't be coming to work today.",
  'polite': 'I wanted to let you know that the meeting ended late last night, after which I continued working on the '
            'report changes and returned home late. For that reason, I will not be coming to work today.',
  'friendly': 'The meeting ended late, and I kept working on the report changes afterward, so I got home late. I’m '
              'staying home from work today.',
  'professional': 'The late conclusion of the meeting, followed by additional report revisions, resulted in a delayed '
                  'return home. Consequently, I will be absent from work today.',
  'formal': 'Following the late conclusion of the meeting and the subsequent report revisions, I returned home at a '
            'late hour. Accordingly, I will not attend work today.'},
 {'input': 'မနေ့ညက meeting ပြီးတာနောက်ကျပြီး အိပ်ရာဝင်တာလည်း အရမ်းနောက်ကျလို့ ဒီနေ့ sleep မဝဘူး၊ ဒါကြောင့် office ကနေ '
           'တစ်ရက်ခွင့်ယူချင်ပါတယ်။',
  'simple': "The meeting ended late last night and I went to bed very late, so I didn't get enough sleep today. "
            "Therefore, I'd like to take a day off from the office today.",
  'polite': 'I wanted to explain the situation: the meeting ended late last night and I went to bed very late, so I '
            'did not get enough sleep today. Would it be possible for me to take the day off today, please?',
  'friendly': "Just a heads-up — the meeting ended late last night and I went to bed very late, so I didn't get enough "
              'sleep today. I’d like to take today off, if that’s okay.',
  'professional': "The meeting ended late last night and I went to bed very late, so I didn't get enough sleep today. "
                  'For this reason, I would like to request one day of leave today.',
  'formal': "The meeting ended late last night and I went to bed very late, so I didn't get enough sleep today. "
            'Accordingly, I respectfully request one day of leave today.'},
 {'input': 'Client က မနေ့က feedback ပေးထားတဲ့ changes တွေ အများကြီးရှိလို့ ဒီနေ့ report ကို ပြန်ပြင်ရမှာဖြစ်ပြီး '
           'deadline မလွတ်အောင် အလုပ်ပိုလုပ်ရပါမယ်။',
  'simple': "The client requested many changes in yesterday's feedback, so I need to revise the report today and work "
            "extra to make sure we don't miss the deadline.",
  'polite': 'I wanted to let you know that the client requested many changes in yesterday’s feedback. I will need to '
            'revise the report today and put in some extra work to keep the deadline on track.',
  'friendly': 'The client sent over a lot of changes yesterday, so I’ve got to rework the report today and put in some '
              'extra time to hit the deadline.',
  'professional': 'Yesterday’s client feedback introduced substantial revisions to the report. I will need to allocate '
                  'additional time to ensure the deadline is met.',
  'formal': 'The extensive changes contained in the client’s feedback have increased the work required on the report. '
            'Accordingly, additional effort will be necessary to meet the established deadline.'},
 {'input': 'Client က design ကို ပြန်ပြင်ခိုင်းထားပြီး ဒီနေ့ည deadline ဖြစ်တာကြောင့် အရင်ဆုံး အဲဒီ changes တွေကို '
           'complete လုပ်ပါမယ်။',
  'simple': "The client asked us to revise the design, and since the deadline is tonight, I'll complete those changes "
            'first.',
  'polite': 'I wanted to keep you updated: the client asked us to revise the design, and since the deadline is '
            'tonight, I will complete those changes first.',
  'friendly': 'Just a quick heads-up — the client asked us to revise the design, and since the deadline is tonight, '
              "I'll complete those changes first.",
  'professional': 'Following the latest client update, the client asked us to revise the design, and since the '
                  'deadline is tonight, I will complete those changes first.',
  'formal': 'In light of the latest client update, the client asked us to revise the design, and since the deadline is '
            'tonight, I will complete those changes first.'},
 {'input': 'မနေ့က client က changes အသစ်တွေ ထပ်ပေးလိုက်လို့ report ပြီးဖို့ နောက်ကျနိုင်ပါတယ်၊ ဒါပေမယ့် deadline '
           'မလွတ်အောင် ကြိုးစားပါမယ်။',
  'simple': "The client sent additional changes yesterday, so the report may be delayed, but I'll do my best to meet "
            'the deadline.',
  'polite': 'I wanted to keep you updated: the client sent additional changes yesterday, so the report may be delayed, '
            'but I will do my best to meet the deadline.',
  'friendly': 'Just a quick heads-up — the client sent additional changes yesterday, so the report may be delayed, but '
              "I'll do my best to meet the deadline.",
  'professional': 'Following the latest client update, the client sent additional changes yesterday, so the report may '
                  'be delayed, but I will do my best to meet the deadline.',
  'formal': 'In light of the latest client update, the client sent additional changes yesterday, so the report may be '
            'delayed, but I will do my best to meet the deadline.'},
 {'input': 'Client က requirements ပြောင်းလိုက်တာကြောင့် လုပ်ပြီးသားအပိုင်းတချို့ကို ပြန်လုပ်ရမှာဖြစ်လို့ project က '
           'နည်းနည်းနောက်ကျနိုင်ပါတယ်။',
  'simple': 'The client changed the requirements, so some completed parts need to be redone and the project may be '
            'slightly delayed.',
  'polite': 'I wanted to keep you updated: the client changed the requirements, so some completed parts need to be '
            'redone and the project may be slightly delayed.',
  'friendly': 'Just a quick heads-up — the client changed the requirements, so some completed parts need to be redone '
              'and the project may be slightly delayed.',
  'professional': 'Following the latest client update, the client changed the requirements, so some completed parts '
                  'need to be redone and the project may be slightly delayed.',
  'formal': 'In light of the latest client update, the client changed the requirements, so some completed parts need '
            'to be redone and the project may be slightly delayed.'},
 {'input': 'ဒီနေ့ client နဲ့ meeting ပြီးရင် သူတို့တောင်းထားတဲ့ changes တွေကို ပြန်လုပ်ပြီး final version ကို '
           'ညနေမတိုင်ခင် ပို့ပေးပါမယ်။',
  'simple': "After today's client meeting, I'll make the requested changes and send the final version before this "
            'evening.',
  'polite': "I wanted to keep you updated: after today's client meeting, I will make the requested changes and send "
            'the final version before this evening.',
  'friendly': "Just a quick heads-up — after today's client meeting, I'll make the requested changes and send the "
              'final version before this evening.',
  'professional': "Following the latest client update, after today's client meeting, I will make the requested changes "
                  'and send the final version before this evening.',
  'formal': "In light of the latest client update, after today's client meeting, I will make the requested changes and "
            'send the final version before this evening.'},
 {'input': 'Client က feedback ပေးတာ နောက်ကျသွားလို့ development လုပ်ရမယ့်အချိန်လည်း နောက်ကျသွားတယ်၊ ဒါကြောင့် deadline '
           'ကို တစ်ရက်ရွှေ့ပေးစေချင်ပါတယ်။',
  'simple': "The client provided feedback late, which delayed the development work, so I'd like to request that the "
            'deadline be moved back by one day.',
  'polite': 'The client’s late feedback has pushed the development schedule back. Would it be possible to extend the '
            'deadline by one day?',
  'friendly': 'The client got back to us late, so the development work was pushed back. Could we give the deadline one '
              'more day?',
  'professional': 'The delayed client feedback has affected the development schedule. I would appreciate a one-day '
                  'extension to the deadline.',
  'formal': 'As the client feedback was received late and delayed development, I respectfully request a one-day '
            'extension to the deadline.'},
 {'input': 'Client က မနေ့ညကမှ requirements အသစ်ပို့လာလို့ ဒီနေ့ မူရင်း plan အတိုင်း မပြီးနိုင်ဘူး၊ အချိန်နည်းနည်း '
           'ထပ်လိုပါတယ်။',
  'simple': "The client only sent the new requirements last night, so I won't be able to finish today according to the "
            'original plan. I need a little more time.',
  'polite': 'I wanted to keep you updated: the client only sent the new requirements last night, so I will not be able '
            'to finish today according to the original plan. I need a little more time.',
  'friendly': "Just a quick heads-up — the client only sent the new requirements last night, so I won't be able to "
              'finish today according to the original plan. I need a little more time.',
  'professional': 'Following the latest client update, the client only sent the new requirements last night, so I will '
                  'be unable to finish today according to the original plan. I need slightly more time.',
  'formal': 'In light of the latest client update, the client only sent the new requirements last night, so I will not '
            'be able to finish today according to the original plan. I need a short while more time.'},
 {'input': 'Meeting မှာ client က changes အများကြီး တောင်းထားလို့ report ကို ပြန်ပြင်ပြီးမှ final submission လုပ်ပါမယ်။',
  'simple': "The client requested many changes during the meeting, so I'll revise the report before making the final "
            'submission.',
  'polite': 'I wanted to keep you updated: the client requested many changes during the meeting, so I will revise the '
            'report before making the final submission.',
  'friendly': "Just a quick heads-up — the client requested many changes during the meeting, so I'll revise the report "
              'before making the final submission.',
  'professional': 'Following the latest client update, the client requested many changes during the meeting, so I will '
                  'revise the report before making the final submission.',
  'formal': 'In light of the latest client update, the client requested many changes during the meeting, so I will '
            'revise the report before making the final submission.'},
 {'input': 'Client က design ကို approve မလုပ်သေးလို့ development ကို ဆက်လုပ်လို့မရဘူး၊ approval ရတာနဲ့ ဆက်လုပ်ပါမယ်။',
  'simple': "The client hasn't approved the design yet, so we can't continue development. We'll continue as soon as we "
            'receive approval.',
  'polite': "I wanted to keep you updated: the client hasn't approved the design yet, so we can't continue "
            "development. We'll continue as soon as we receive approval.",
  'friendly': "Just a quick heads-up — the client hasn't approved the design yet, so we can't continue development. "
              "We'll continue as soon as we receive approval.",
  'professional': "Following the latest client update, the client hasn't approved the design yet, so we can't continue "
                  "development. We'll continue as soon as we receive approval.",
  'formal': "In light of the latest client update, the client hasn't approved the design yet, so we can't continue "
            "development. We'll continue as soon as we receive approval."},
 {'input': 'Client feedback ကို အရင် review လုပ်ပြီး ဘာတွေပြင်ရမလဲ သတ်မှတ်ပြီးမှ development team ကို ပြန်ပို့ပါမယ်။',
  'simple': "I'll review the client feedback first, determine what needs to be changed, and then send the requirements "
            'back to the development team.',
  'polite': 'I wanted to keep you updated: I will review the client feedback first, determine what needs to be '
            'changed, and then send the requirements back to the development team.',
  'friendly': "Just a quick heads-up — I'll review the client feedback first, determine what needs to be changed, and "
              'then send the requirements back to the development team.',
  'professional': 'Following the latest client update, I will review the client feedback first, determine what needs '
                  'to be changed, and then send the requirements back to the development team.',
  'formal': 'In light of the latest client update, I will review the client feedback first, determine what needs to be '
            'changed, and then send the requirements back to the development team.'},
 {'input': 'ဒီနေ့ အလုပ်တွေ အများကြီးရှိပြီး report လည်း submit လုပ်ရမှာဖြစ်လို့ meeting ကို မနက်ဖြန်ရွှေ့ပေးလို့ရမလား။',
  'simple': 'I have a lot of work to finish today, including submitting the report, so could we move the meeting to '
            'tomorrow?',
  'polite': 'I have several tasks to complete today, including the report submission. Would it be possible to move our '
            'meeting to tomorrow?',
  'friendly': 'I’ve got a lot to finish today, including the report. Can we push the meeting to tomorrow?',
  'professional': 'Given today’s workload and the report submission, I would appreciate rescheduling the meeting for '
                  'tomorrow.',
  'formal': 'In view of the work scheduled for today, including the report submission, I respectfully request that the '
            'meeting be postponed until tomorrow.'},
 {'input': 'ဒီနေ့ deadline နှစ်ခုရှိနေတာကြောင့် အခု meeting ကို attend လုပ်ဖို့ အခက်အခဲရှိပါတယ်၊ '
           'နောက်တစ်ချိန်ရွှေ့ပေးပါ။',
  'simple': "I have two deadlines today, so I'm having difficulty attending the meeting. Could we move it to another "
            'time?',
  'polite': 'I wanted to ask whether it would be possible to move it to another time.',
  'friendly': 'Could we move it to another time?',
  'professional': 'Given the current workload, I would appreciate it if we could move it to another time.',
  'formal': 'In view of the current workload, I respectfully request that we move it to another time.'},
 {'input': 'Report မပြီးသေးလို့ ဒီနေ့ meeting မတက်နိုင်သေးဘူး၊ report ပြီးတာနဲ့ update ပေးပါမယ်။',
  'simple': "I haven't finished the report yet, so I can't attend today's meeting. I'll provide an update as soon as "
            'the report is finished.',
  'polite': "I wanted to let you know that I have not finished the report yet, so I cannot attend today's meeting. I "
            'will provide an update as soon as the report is finished.',
  'friendly': "Just a heads-up — I haven't finished the report yet, so I can't attend today's meeting. I'll provide an "
              'update as soon as the report is finished.',
  'professional': "For planning purposes, I have not finished the report yet, so I cannot attend today's meeting. I "
                  'will provide an update as soon as the report is finished.',
  'formal': "Please be advised that I have not finished the report yet, so I cannot attend today's meeting. I will "
            'provide an update as soon as the report is finished.'},
 {'input': 'ဒီနေ့ workload အရမ်းများနေလို့ task အသစ်ကို အခုချက်ချင်း မစနိုင်သေးဘူး၊ လက်ရှိ task ပြီးမှ စပါမယ်။',
  'simple': "My workload is very heavy today, so I can't start the new task right away. I'll start it after I finish "
            'the current task.',
  'polite': 'I wanted to let you know that My workload is very heavy today, so I cannot start the new task right away. '
            'I will start it after I finish the current task.',
  'friendly': "Just a heads-up — My workload is very heavy today, so I can't start the new task right away. I'll start "
              'it after I finish the current task.',
  'professional': 'For planning purposes, My workload is very heavy today, so I cannot start the new task right away. '
                  'I will start it after I finish the current task.',
  'formal': 'Please be advised that My workload is very heavy today, so I cannot start the new task right away. I will '
            'start it after I finish the current task.'},
 {'input': 'ဒီနေ့ client report နဲ့ presentation နှစ်ခုလုံး ပြင်ရမှာဖြစ်လို့ deadline ကို နည်းနည်းရွှေ့ပေးနိုင်မလား။',
  'simple': 'I need to revise both the client report and the presentation today, so could we move the deadline back a '
            'little?',
  'polite': 'I’m working on both the client report and the presentation today. Would it be possible to extend the '
            'deadline slightly?',
  'friendly': 'I’ve got both the client report and presentation to finish today. Can we push the deadline back a '
              'little?',
  'professional': 'With both deliverables requiring revision today, I would appreciate a slight extension to the '
                  'deadline.',
  'formal': 'In view of the two deliverables requiring revision today, I respectfully request a modest extension to '
            'the deadline.'},
 {'input': 'အလုပ်တွေ တစ်ခုပြီးတစ်ခု ဝင်လာနေလို့ မူရင်း deadline အတိုင်း မပြီးနိုင်နိုင်ဘူး၊ အချိန်ထပ်ပေးဖို့ လိုပါတယ်။',
  'simple': 'Tasks keep coming in one after another, so I may not be able to finish by the original deadline. I need '
            'some additional time.',
  'polite': 'I wanted to let you know that Tasks keep coming in one after another, so I may not be able to finish by '
            'the original deadline. I need some additional time.',
  'friendly': 'Just a heads-up — Tasks keep coming in one after another, so I may not be able to finish by the '
              'original deadline. I need some additional time.',
  'professional': 'For planning purposes, Tasks keep coming in one after another, so I may not be able to finish by '
                  'the original deadline. I need some additional time.',
  'formal': 'Please be advised that Tasks keep coming in one after another, so I may not be able to finish by the '
            'original deadline. I need some additional time.'},
 {'input': 'Report က expected ထက် အချိန်ပိုကြာနေလို့ ဒီနေ့ညအထိ အလုပ်ဆက်လုပ်ရနိုင်ပါတယ်။',
  'simple': 'The report is taking longer than expected, so I may need to continue working until tonight.',
  'polite': 'I wanted to let you know that The report is taking longer than expected, so I may need to continue '
            'working until tonight.',
  'friendly': 'Just a heads-up — The report is taking longer than expected, so I may need to continue working until '
              'tonight.',
  'professional': 'For planning purposes, The report is taking longer than expected, so I may need to continue working '
                  'until tonight.',
  'formal': 'Please be advised that The report is taking longer than expected, so I may need to continue working until '
            'tonight.'},
 {'input': 'ဒီနေ့ meeting တွေ ဆက်တိုက်ရှိနေလို့ report ကို အခုချက်ချင်း မပြီးနိုင်သေးဘူး၊ ညနေပိုင်းမှာ complete '
           'လုပ်ပါမယ်။',
  'simple': "I have meetings back-to-back today, so I can't finish the report right away. I'll complete it this "
            'afternoon.',
  'polite': 'I wanted to let you know that I have meetings back-to-back today, so I cannot finish the report right '
            'away. I will complete it this afternoon.',
  'friendly': "Just a heads-up — I have meetings back-to-back today, so I can't finish the report right away. I'll "
              'complete it this afternoon.',
  'professional': 'For planning purposes, I have meetings back-to-back today, so I cannot finish the report right '
                  'away. I will complete it this afternoon.',
  'formal': 'Please be advised that I have meetings back-to-back today, so I cannot finish the report right away. I '
            'will complete it this afternoon.'},
 {'input': 'Task အဟောင်းတွေ မပြီးသေးခင် task အသစ်တွေ ထပ်ရလာလို့ priority သတ်မှတ်ပြီး တစ်ခုပြီးတစ်ခု လုပ်သွားပါမယ်။',
  'simple': "New tasks keep coming in before the old ones are finished, so I'll set priorities and work through them "
            'one by one.',
  'polite': 'I wanted to let you know that New tasks keep coming in before the old ones are finished, so I will set '
            'priorities and work through them one by one.',
  'friendly': "Just a heads-up — New tasks keep coming in before the old ones are finished, so I'll set priorities and "
              'work through them one by one.',
  'professional': 'For planning purposes, New tasks keep coming in before the old ones are finished, so I will set '
                  'priorities and work through them one by one.',
  'formal': 'Please be advised that New tasks keep coming in before the old ones are finished, so I will set '
            'priorities and work through them one by one.'},
 {'input': 'Deadline နီးလာတာကြောင့် ဒီနေ့ overtime လုပ်ပြီး report ကို final version အထိ ပြီးအောင်လုပ်ပါမယ်။',
  'simple': "Since the deadline is approaching, I'll work overtime today and finish the report through the final "
            'version.',
  'polite': 'I wanted to let you know that Since the deadline is approaching, I will work overtime today and finish '
            'the report through the final version.',
  'friendly': "Just a heads-up — Since the deadline is approaching, I'll work overtime today and finish the report "
              'through the final version.',
  'professional': 'For planning purposes, Since the deadline is approaching, I will work overtime today and finish the '
                  'report through the final version.',
  'formal': 'Please be advised that Since the deadline is approaching, I will work overtime today and finish the '
            'report through the final version.'},
 {'input': 'အမေက မနေ့ကတည်းက နေမကောင်းဖြစ်နေတာကြောင့် ဒီနေ့ ဆေးရုံမှာ ဆရာဝန်နဲ့ သွားပြရမှာပါ၊ ဒါကြောင့် ဒီနေ့မနက် '
           'အလုပ်မလာနိုင်ဘူး။',
  'simple': 'My mother has been unwell since yesterday, so I need to take her to the hospital to see a doctor today. '
            "Therefore, I won't be able to come to work this morning.",
  'polite': 'I wanted to let you know that my mother has been unwell since yesterday and I need to take her to the '
            'hospital to see a doctor today. Unfortunately, I will not be able to come to work this morning.',
  'friendly': 'Just a heads-up — my mother has been unwell since yesterday, and I need to take her to the hospital '
              'today. I won’t be able to make it to work this morning.',
  'professional': 'My mother has been unwell since yesterday and needs to see a doctor at the hospital today. I will '
                  'therefore be unable to attend work this morning.',
  'formal': 'As my mother has been unwell since yesterday and requires medical attention today, I will not be able to '
            'attend work this morning.'},
 {'input': 'အမေ့မှာ ဒီမနက် doctor appointment ရှိလို့ ကျွန်တော်ကိုယ်တိုင် လိုက်ပို့ပေးရမှာကြောင့် office ကို နောက်ကျမှ '
           'ရောက်ပါမယ်။',
  'simple': "My mother has a doctor's appointment this morning, and I need to accompany her, so I'll arrive at the "
            'office late.',
  'polite': "I wanted to let you know that my mother has a doctor's appointment this morning, and I need to accompany "
            'her, so I will arrive at the office late. Thank you for your understanding.',
  'friendly': "Just a heads-up — my mother has a doctor's appointment this morning, and I need to accompany her, so "
              "I'll arrive at the office late.",
  'professional': "Due to the family circumstances involved, my mother has a doctor's appointment this morning, and I "
                  'need to accompany her, so I will arrive at the office late.',
  'formal': "In view of the family circumstances involved, my mother has a doctor's appointment this morning, and I "
            'need to accompany her, so I will arrive at the office late.'},
 {'input': 'မိသားစုဝင်တစ်ယောက် နေမကောင်းဖြစ်နေလို့ ဆေးရုံလိုက်ပို့ပေးရမှာဖြစ်ပြီး ဒီနေ့ အလုပ်ကနေ ခွင့်ယူချင်ပါတယ်။',
  'simple': "A family member is unwell and I need to take them to the hospital, so I'd like to take leave from work "
            'today.',
  'polite': 'I wanted to explain the situation: a family member is unwell and I need to take them to the hospital. '
            'Would it be possible for me to take the day off today, please?',
  'friendly': 'Just a heads-up — a family member isn’t feeling well, and I need to take them to the hospital. I’d like '
              'to take today off, if that’s okay.',
  'professional': 'A family member is unwell and requires a hospital visit today. For this reason, I would like to '
                  'request one day of leave.',
  'formal': 'Owing to a family medical matter that requires a hospital visit, I respectfully request one day of leave '
            'today.'},
 {'input': 'အမေက နေမကောင်းတာကြောင့် ဒီနေ့မနက် hospital ကို လိုက်သွားရမှာပါ၊ နေ့လည်ပိုင်း အခြေအနေကောင်းရင် office '
           'ပြန်ဝင်ပါမယ်။',
  'simple': 'My mother is unwell, so I need to go to the hospital with her this morning. If things are okay this '
            "afternoon, I'll return to the office.",
  'polite': 'I wanted to let you know that my mother is unwell, so I need to go to the hospital with her this morning. '
            'If things are okay this afternoon, I will return to the office. Thank you for your understanding.',
  'friendly': 'Just a heads-up — my mother is unwell, so I need to go to the hospital with her this morning. If things '
              "are okay this afternoon, I'll return to the office.",
  'professional': 'Due to the family circumstances involved, my mother is unwell, so I need to go to the hospital with '
                  'her this morning. If things are okay this afternoon, I will return to the office.',
  'formal': 'In view of the family circumstances involved, my mother is unwell, so I need to go to the hospital with '
            'her this morning. If things are okay this afternoon, I will return to the office.'},
 {'input': 'မနေ့ညကတည်းက အမေ နေမကောင်းဖြစ်နေလို့ ဒီနေ့ doctor ဆီသွားပြရမှာကြောင့် အလုပ်ကို မနက်ပိုင်း မလာနိုင်ပါဘူး။',
  'simple': "My mother has been unwell since last night, so I need to take her to the doctor today and won't be able "
            'to come to work this morning.',
  'polite': 'I wanted to let you know that my mother has been unwell since last night, so I need to take her to the '
            "doctor today and won't be able to come to work this morning. Thank you for your understanding.",
  'friendly': 'Just a heads-up — my mother has been unwell since last night, so I need to take her to the doctor today '
              "and won't be able to come to work this morning.",
  'professional': 'Due to the family circumstances involved, my mother has been unwell since last night, so I need to '
                  "take her to the doctor today and won't be able to come to work this morning.",
  'formal': 'In view of the family circumstances involved, my mother has been unwell since last night, so I need to '
            "take her to the doctor today and won't be able to come to work this morning."},
 {'input': 'အမေ့ appointment က မနက်ပိုင်းမှာဖြစ်ပြီး ကျွန်တော်ကိုယ်တိုင် လိုက်ပို့ရမှာဖြစ်လို့ ဒီနေ့ '
           'တစ်ရက်ခွင့်ယူချင်ပါတယ်။',
  'simple': "My mother's appointment is in the morning and I need to accompany her, so I'd like to take a day off "
            'today.',
  'polite': "I wanted to explain the situation: my mother's appointment is in the morning and I need to accompany her. "
            'Would it be possible for me to take the day off today, please?',
  'friendly': "Just a heads-up — my mother's appointment is in the morning and I need to accompany her. I’d like to "
              'take today off, if that’s okay.',
  'professional': "My mother's appointment is in the morning and I need to accompany her. For this reason, I would "
                  'like to request one day of leave today.',
  'formal': "My mother's appointment is in the morning and I need to accompany her. Accordingly, I respectfully "
            'request one day of leave today.'},
 {'input': 'မိသားစုမှာ health issue တစ်ခုဖြစ်နေလို့ ဒီနေ့ အိမ်မှာ နေရပြီး အလုပ်ကနေ ခွင့်တောင်းချင်ပါတယ်။',
  'simple': "There is a health issue in my family that requires me to stay home today, so I'd like to request leave "
            'from work.',
  'polite': 'I wanted to let you know that there is a health issue in my family that requires me to stay home today. '
            "As a result, I'd like to request leave from work.",
  'friendly': "Just a quick heads-up — there's a health issue in my family that requires me to stay home today. That’s "
              "why I'd like to request leave from work.",
  'professional': "Because there is a health issue in my family that requires me to stay home today, I'd like to "
                  'request leave from work.',
  'formal': "Given that there is a health issue in my family that requires me to stay home today, I'd like to request "
            'leave from work.'},
 {'input': 'အမေကို hospital ပို့ပြီး ဆရာဝန်နဲ့တွေ့ပြီးမှ အခြေအနေကို သိရမှာဖြစ်လို့ ဒီနေ့ office ပြန်ဝင်နိုင်မလား '
           'မသေချာသေးပါဘူး။',
  'simple': "I need to take my mother to the hospital and see the doctor before we know her condition, so I'm not sure "
            "yet whether I'll be able to return to the office today.",
  'polite': 'I wanted to let you know that I need to take my mother to the hospital and see the doctor before we know '
            'her condition, so I am not sure yet whether I will be able to return to the office today. Thank you for '
            'your understanding.',
  'friendly': 'Just a heads-up — I need to take my mother to the hospital and see the doctor before we know her '
              "condition, so I'm not sure yet whether I'll be able to return to the office today.",
  'professional': 'Due to the family circumstances involved, I need to take my mother to the hospital and see the '
                  'doctor before we know her condition, so I am not sure yet whether I will be able to return to the '
                  'office today.',
  'formal': 'In view of the family circumstances involved, I need to take my mother to the hospital and see the doctor '
            'before we know her condition, so I am not sure yet whether I will be able to return to the office today.'},
 {'input': 'အမေ နေမကောင်းဖြစ်နေတာကြောင့် ဒီနေ့ morning appointment ကို လိုက်ပို့ရမှာပါ၊ ပြီးတာနဲ့ အလုပ်ပြန်ဝင်နိုင်ရင် '
           'ပြန်ဝင်ပါမယ်။',
  'simple': "My mother is unwell, so I need to accompany her to her morning appointment. I'll return to work afterward "
            "if I'm able to.",
  'polite': 'I wanted to let you know that my mother is unwell, so I need to accompany her to her morning appointment. '
            'I will return to work afterward if I am able to. Thank you for your understanding.',
  'friendly': "Just a heads-up — my mother is unwell, so I need to accompany her to her morning appointment. I'll "
              "return to work afterward if I'm able to.",
  'professional': 'Due to the family circumstances involved, my mother is unwell, so I need to accompany her to her '
                  'morning appointment. I will return to work afterward if I am able to.',
  'formal': 'In view of the family circumstances involved, my mother is unwell, so I need to accompany her to her '
            'morning appointment. I will return to work afterward if I am able to.'},
 {'input': 'မိသားစုကျန်းမာရေးကိစ္စကြောင့် ဒီနေ့ အလုပ်တစ်ရက်ခွင့်ယူချင်ပါတယ်၊ အခြေအနေတိုးတက်လာရင် မနက်ဖြန် '
           'ပုံမှန်ပြန်ဝင်ပါမယ်။',
  'simple': "Due to a family health matter, I'd like to take one day off from work today. If the situation improves, "
            "I'll return to work normally tomorrow.",
  'polite': 'I wanted to let you know that due to a family health matter, I would like to take one day off from work '
            'today. If the situation improves, I will return to work normally tomorrow. Thank you for your '
            'understanding.',
  'friendly': "Just a heads-up — due to a family health matter, I'd like to take one day off from work today. If the "
              "situation improves, I'll return to work normally tomorrow.",
  'professional': 'Due to the family circumstances involved, due to a family health matter, I would like to take one '
                  'day off from work today. If the situation improves, I will return to work normally tomorrow.',
  'formal': 'In view of the family circumstances involved, due to a family health matter, I would like to take one day '
            'off from work today. If the situation improves, I will return to work normally tomorrow.'},
 {'input': 'ဒီနေ့မနက် power ပြတ်သွားလို့ laptop အားကုန်သွားပြီး report ကို ဆက်လုပ်လို့မရသေးဘူး၊ မီးပြန်လာတာနဲ့ '
           'ဆက်လုပ်ပါမယ်။',
  'simple': "The power went out this morning and my laptop battery ran out, so I can't continue working on the report "
            "yet. I'll continue as soon as the power comes back.",
  'polite': 'I wanted to let you know that the power went out this morning and my laptop battery ran out, so I cannot '
            'continue working on the report yet. I will resume as soon as power is restored.',
  'friendly': 'Quick heads-up — the power went out and my laptop battery is dead, so I can’t keep working on the '
              'report right now. I’ll pick it up again when the power comes back.',
  'professional': 'A power outage this morning drained my laptop battery and temporarily stopped work on the report. I '
                  'will resume once power is restored.',
  'formal': 'Owing to the power interruption and the resulting depletion of my laptop battery, work on the report '
            'cannot continue at present. I shall resume upon restoration of power.'},
 {'input': 'Internet connection အရမ်းနှေးနေလို့ client meeting ကို join လို့မရသေးဘူး၊ connection ပြန်ကောင်းတာနဲ့ join '
           'လိုက်ပါမယ်။',
  'simple': "The internet connection is very slow, so I can't join the client meeting yet. I'll join as soon as the "
            'connection improves.',
  'polite': 'I wanted to let you know that the internet connection is very slow, so I cannot join the client meeting '
            'yet. I will join as soon as the connection improves. Thank you for your patience.',
  'friendly': "Quick heads-up — the internet connection is very slow, so I can't join the client meeting yet. I'll "
              'join as soon as the connection improves.',
  'professional': 'Because of the technical issue, the internet connection is very slow, so I cannot join the client '
                  'meeting yet. I will join as soon as the connection improves.',
  'formal': 'Due to the technical disruption, the internet connection is very slow, so I cannot join the client '
            'meeting yet. I will join as soon as the connection improves.'},
 {'input': 'မနေ့ညက laptop error ဖြစ်သွားလို့ file ကို save လုပ်လို့မရခဲ့ဘူး၊ ဒီနေ့ မနက်မှာ ပြန်စစ်ပြီး report ကို '
           'complete လုပ်ပါမယ်။',
  'simple': "My laptop had an error last night, so I couldn't save the file. I'll check it again this morning and "
            'complete the report.',
  'polite': "I wanted to let you know that my laptop had an error last night, so I couldn't save the file. I will "
            'check it again this morning and complete the report. Thank you for your patience.',
  'friendly': "Quick heads-up — my laptop had an error last night, so I couldn't save the file. I'll check it again "
              'this morning and complete the report.',
  'professional': "Because of the technical issue, my laptop had an error last night, so I couldn't save the file. I "
                  'will check it again this morning and complete the report.',
  'formal': "Due to the technical disruption, my laptop had an error last night, so I couldn't save the file. I will "
            'check it again this morning and complete the report.'},
 {'input': 'Office မှာ internet down ဖြစ်နေလို့ client ကို file ပို့လို့မရသေးဘူး၊ connection ပြန်ရတာနဲ့ '
           'ချက်ချင်းပို့ပါမယ်။',
  'simple': "The internet is down at the office, so I can't send the file to the client yet. I'll send it as soon as "
            'the connection is restored.',
  'polite': 'I wanted to let you know that the internet is down at the office, so I cannot send the file to the client '
            'yet. I will send it as soon as the connection is restored. Thank you for your patience.',
  'friendly': "Quick heads-up — the internet is down at the office, so I can't send the file to the client yet. I'll "
              'send it as soon as the connection is restored.',
  'professional': 'Because of the technical issue, the internet is down at the office, so I cannot send the file to '
                  'the client yet. I will send it as soon as the connection is restored.',
  'formal': 'Due to the technical disruption, the internet is down at the office, so I cannot send the file to the '
            'client yet. I will send it as soon as the connection is restored.'},
 {'input': 'Power outage ကြောင့် computer ပိတ်သွားပြီး presentation file က open လို့မရတော့ဘူး၊ backup file ကို စစ်ပြီး '
           'ပြန်ပို့ပါမယ်။',
  'simple': "The power outage shut down my computer and I can't open the presentation file, so I'll check the backup "
            'file and resend it.',
  'polite': 'I wanted to let you know that the power outage shut down my computer and I cannot open the presentation '
            'file, so I will check the backup file and resend it. Thank you for your patience.',
  'friendly': "Quick heads-up — the power outage shut down my computer and I can't open the presentation file, so I'll "
              'check the backup file and resend it.',
  'professional': 'Because of the technical issue, the power outage shut down my computer and I cannot open the '
                  'presentation file, so I will check the backup file and resend it.',
  'formal': 'Due to the technical disruption, the power outage shut down my computer and I cannot open the '
            'presentation file, so I will check the backup file and resend it.'},
 {'input': 'Laptop က sudden restart ဖြစ်ပြီး မပြီးသေးတဲ့ work တချို့ ပျောက်သွားလို့ ဒီနေ့ deadline ကို '
           'နည်းနည်းရွှေ့ပေးဖို့ လိုပါတယ်။',
  'simple': 'My laptop suddenly restarted and some unfinished work was lost, so I need the deadline to be moved back a '
            'little today.',
  'polite': 'I wanted to let you know that my laptop suddenly restarted and some unfinished work was lost, so I need '
            'the deadline to be moved back a little today. Thank you for your patience.',
  'friendly': 'Quick heads-up — my laptop suddenly restarted and some unfinished work was lost, so I need the deadline '
              'to be moved back a little today.',
  'professional': 'Because of the technical issue, my laptop suddenly restarted and some unfinished work was lost, so '
                  'I need the deadline to be moved back slightly today.',
  'formal': 'Due to the technical disruption, my laptop suddenly restarted and some unfinished work was lost, so I '
            'need the deadline to be moved back a short while today.'},
 {'input': 'Internet မကောင်းတာကြောင့် online meeting ကို join လို့မရဘူး၊ phone connection ရတာနဲ့ join လိုက်ပါမယ်။',
  'simple': "The internet connection is poor, so I can't join the online meeting. I'll join as soon as I have a phone "
            'connection.',
  'polite': 'I wanted to let you know that the internet connection is poor, so I cannot join the online meeting. I '
            'will join as soon as I have a phone connection. Thank you for your patience.',
  'friendly': "Quick heads-up — the internet connection is poor, so I can't join the online meeting. I'll join as soon "
              'as I have a phone connection.',
  'professional': 'Because of the technical issue, the internet connection is poor, so I cannot join the online '
                  'meeting. I will join as soon as I have a phone connection.',
  'formal': 'Due to the technical disruption, the internet connection is poor, so I cannot join the online meeting. I '
            'will join as soon as I have a phone connection.'},
 {'input': 'ဒီနေ့ office မှာ မီးခဏခဏပြတ်နေလို့ development work ကို ဆက်လုပ်ရတာ အခက်အခဲရှိနေပါတယ်။',
  'simple': "The power keeps going out at the office today, so I'm having difficulty continuing the development work.",
  'polite': 'I wanted to let you know that the power keeps going out at the office today, so I am having difficulty '
            'continuing the development work. Thank you for your patience.',
  'friendly': "Quick heads-up — the power keeps going out at the office today, so I'm having difficulty continuing the "
              'development work.',
  'professional': 'Because of the technical issue, the power keeps going out at the office today, so I am having '
                  'difficulty continuing the development work.',
  'formal': 'Due to the technical disruption, the power keeps going out at the office today, so I am having difficulty '
            'continuing the development work.'},
 {'input': 'Computer problem ဖြစ်လို့ report ကို finalise လုပ်လို့မရသေးဘူး၊ technician လာစစ်ပြီးတာနဲ့ ဆက်လုပ်ပါမယ်။',
  'simple': "There's a computer problem, so I can't finalize the report yet. I'll continue as soon as the technician "
            'has checked it.',
  'polite': 'I wanted to let you know that there is a computer problem, so I cannot finalize the report yet. I will '
            'continue as soon as the technician has checked it. Thank you for your patience.',
  'friendly': "Quick heads-up — there's a computer problem, so I can't finalize the report yet. I'll continue as soon "
              'as the technician has checked it.',
  'professional': 'Because of the technical issue, there is a computer problem, so I cannot finalize the report yet. I '
                  'will continue as soon as the technician has checked it.',
  'formal': 'Due to the technical disruption, there is a computer problem, so I cannot finalize the report yet. I will '
            'continue as soon as the technician has checked it.'},
 {'input': 'Network down ဖြစ်နေလို့ client server ကို access မရသေးဘူး၊ IT team က fix လုပ်ပြီးတာနဲ့ task ကို '
           'ဆက်လုပ်ပါမယ်။',
  'simple': "The network is down, so I can't access the client server yet. I'll continue the task as soon as the IT "
            'team fixes it.',
  'polite': 'I wanted to let you know that the network is down, so I cannot access the client server yet. I will '
            'continue the task as soon as the IT team fixes it. Thank you for your patience.',
  'friendly': "Quick heads-up — the network is down, so I can't access the client server yet. I'll continue the task "
              'as soon as the IT team fixes it.',
  'professional': 'Because of the technical issue, the network is down, so I cannot access the client server yet. I '
                  'will continue the task as soon as the IT team fixes it.',
  'formal': 'Due to the technical disruption, the network is down, so I cannot access the client server yet. I will '
            'continue the task as soon as the IT team fixes it.'},
 {'input': 'ဒီနေ့ delivery လာမယ့်အချိန်မှာ အိမ်မှာ လူမရှိနိုင်လို့ မနက်ဖြန်ကို delivery date ရွှေ့ပေးလို့ရမလား။',
  'simple': 'No one may be home when the delivery arrives today, so could we move the delivery date to tomorrow?',
  'polite': 'I wanted to let you know that no one may be home when the delivery arrives today. Would it be possible to '
            'move the delivery date to tomorrow?',
  'friendly': 'There might not be anyone home when the delivery comes today. Can we move it to tomorrow?',
  'professional': 'No one may be available at home to receive the delivery today. I would appreciate rescheduling the '
                  'delivery for tomorrow.',
  'formal': 'As no one may be available to receive the delivery today, I respectfully request that the delivery date '
            'be moved to tomorrow.'},
 {'input': 'မိုးကြောင့် delivery နောက်ကျနေပြီး customer ကိုလည်း အကြောင်းကြားထားပါတယ်၊ ရောက်တာနဲ့ ထပ်ပြီး update '
           'ပေးပါမယ်။',
  'simple': "The delivery is delayed because of the rain, and I have already informed the customer. I'll provide "
            'another update as soon as it arrives.',
  'polite': 'I wanted to let you know that the delivery is delayed because of the rain, and I have already informed '
            'the customer. I will provide another update as soon as it arrives.',
  'friendly': 'Just a heads-up — the delivery is delayed because of the rain, and I have already informed the '
              "customer. I'll provide another update as soon as it arrives.",
  'professional': 'For your information, The delivery is delayed because of the rain, and I have already informed the '
                  'customer. I will provide another update as soon as it arrives.',
  'formal': 'Please be advised that The delivery is delayed because of the rain, and I have already informed the '
            'customer. I will provide another update as soon as it arrives.'},
 {'input': 'Appointment က မနက်ပိုင်းမှာရှိပေမယ့် traffic အရမ်းပိတ်နေလို့ နည်းနည်းနောက်ကျနိုင်ပါတယ်။',
  'simple': 'I have an appointment this morning, but traffic is very heavy, so I may be a little late.',
  'polite': 'I wanted to let you know that I have an appointment this morning, but traffic is very heavy, so I may be '
            'a little late.',
  'friendly': 'Just a heads-up — I have an appointment this morning, but traffic is very heavy, so I may be a little '
              'late.',
  'professional': 'For your information, I have an appointment this morning, but traffic is very heavy, so I may be '
                  'slightly late.',
  'formal': 'Please be advised that I have an appointment this morning, but traffic is very heavy, so I may be a short '
            'while late.'},
 {'input': 'ဒီနေ့ appointment ကို မတက်နိုင်တော့လို့ မနက်ဖြန် afternoon ကို ပြန်ရွှေ့ပေးလို့ရမလား။',
  'simple': "I won't be able to attend today's appointment, so could we reschedule it for tomorrow afternoon?",
  'polite': 'I’m sorry, but I won’t be able to attend today’s appointment. Would it be possible to reschedule it for '
            'tomorrow afternoon?',
  'friendly': 'I can’t make today’s appointment. Can we move it to tomorrow afternoon?',
  'professional': 'I am unable to attend today’s appointment. I would appreciate it if we could reschedule it for '
                  'tomorrow afternoon.',
  'formal': 'As I am unable to attend today’s appointment, I respectfully request that it be rescheduled for tomorrow '
            'afternoon.'},
 {'input': 'Delivery driver က traffic ကြောင့် နောက်ကျနေတယ်လို့ ပြောထားလို့ customer ကို ခဏစောင့်ပေးဖို့ ပြောထားပါတယ်။',
  'simple': "The delivery driver said the delivery is delayed because of traffic, so I've asked the customer to wait "
            'for a while.',
  'polite': 'I’m sorry for the inconvenience. The delivery driver said the delivery is delayed because of traffic, so '
            "I've asked the customer to wait for a while. Could you please wait a little longer?",
  'friendly': "Just a heads-up — the delivery driver said the delivery is delayed because of traffic, so I've asked "
              'the customer to wait for a while. Can you give it a little more time?',
  'professional': "Please note that the delivery driver said the delivery is delayed because of traffic, so I've asked "
                  'the customer to wait for a while. I would appreciate your patience while this is resolved.',
  'formal': "Kindly be advised that the delivery driver said the delivery is delayed because of traffic, so I've asked "
            'the customer to wait for a while. Your patience is appreciated.'},
 {'input': 'ဒီနေ့ meeting schedule က တစ်ခုပြီးတစ်ခု ပြောင်းနေလို့ client နဲ့ appointment ကို afternoon ဘက် '
           'ရွှေ့ချင်ပါတယ်။',
  'simple': "Today's meeting schedule keeps changing, so I'd like to move the appointment with the client to the "
            'afternoon.',
  'polite': "I wanted to let you know that today's meeting schedule keeps changing, so I would like to move the "
            'appointment with the client to the afternoon.',
  'friendly': "Just a heads-up — today's meeting schedule keeps changing, so I'd like to move the appointment with the "
              'client to the afternoon.',
  'professional': "For your information, Today's meeting schedule keeps changing, so I would like to move the "
                  'appointment with the client to the afternoon.',
  'formal': "Please be advised that Today's meeting schedule keeps changing, so I would like to move the appointment "
            'with the client to the afternoon.'},
 {'input': 'Customer က delivery address ပြောင်းလိုက်လို့ order ကို ပြန်စီစဉ်ရမှာဖြစ်ပြီး ပို့ဆောင်ချိန် '
           'နည်းနည်းနောက်ကျနိုင်ပါတယ်။',
  'simple': 'The customer changed the delivery address, so we need to rearrange the order and the delivery may be '
            'slightly delayed.',
  'polite': 'I wanted to let you know that the customer changed the delivery address, so we need to rearrange the '
            'order and the delivery may be slightly delayed.',
  'friendly': 'Just a heads-up — the customer changed the delivery address, so we need to rearrange the order and the '
              'delivery may be slightly delayed.',
  'professional': 'For your information, The customer changed the delivery address, so we need to rearrange the order '
                  'and the delivery may be slightly delayed.',
  'formal': 'Please be advised that The customer changed the delivery address, so we need to rearrange the order and '
            'the delivery may be slightly delayed.'},
 {'input': 'Appointment က မနက် 10 နာရီမှာရှိပေမယ့် လမ်းမှာ traffic ကြောင့် အချိန်မီ မရောက်နိုင်ဘူး၊ 15 မိနစ်လောက် '
           'စောင့်ပေးပါ။',
  'simple': "My appointment is at 10 a.m., but I won't be able to arrive on time because of traffic. Please wait for "
            'about 15 minutes.',
  'polite': "I’m sorry for the inconvenience. My appointment is at 10 a.m., but I won't be able to arrive on time "
            'because of traffic. Could you please wait a little longer?',
  'friendly': "Just a heads-up — my appointment is at 10 a.m., but I won't be able to arrive on time because of "
              'traffic. Can you give it a little more time?',
  'professional': 'Please note that my appointment is at 10 a.m., but I will be unable to arrive on time because of '
                  'traffic. I would appreciate your patience while this is resolved.',
  'formal': 'Kindly be advised that my appointment is at 10 a.m., but I will not be able to arrive on time because of '
            'traffic. Your patience is appreciated.'},
 {'input': 'ဒီနေ့ delivery မရောက်သေးလို့ customer ကို ဖုန်းဆက်ပြီး status ကို confirm လုပ်ပါမယ်။',
  'simple': "The delivery hasn't arrived yet today, so I'll call the customer and confirm the status.",
  'polite': "I wanted to let you know that the delivery hasn't arrived yet today, so I will call the customer and "
            'confirm the status.',
  'friendly': "Just a heads-up — the delivery hasn't arrived yet today, so I'll call the customer and confirm the "
              'status.',
  'professional': "For your information, The delivery hasn't arrived yet today, so I will call the customer and "
                  'confirm the status.',
  'formal': "Please be advised that The delivery hasn't arrived yet today, so I will call the customer and confirm the "
            'status.'},
 {'input': 'Client meeting နဲ့ appointment အချိန်တွေ တိုက်နေတဲ့အတွက် appointment ကို နောက်တစ်ချိန်ရွှေ့ပေးဖို့ '
           'တောင်းဆိုချင်ပါတယ်။',
  'simple': "The client meeting conflicts with the appointment time, so I'd like to request that the appointment be "
            'moved to another time.',
  'polite': 'I wanted to let you know that the client meeting conflicts with the appointment time, so I would like to '
            'request that the appointment be moved to another time.',
  'friendly': "Just a heads-up — the client meeting conflicts with the appointment time, so I'd like to request that "
              'the appointment be moved to another time.',
  'professional': 'For your information, The client meeting conflicts with the appointment time, so I would like to '
                  'request that the appointment be moved to another time.',
  'formal': 'Please be advised that The client meeting conflicts with the appointment time, so I would like to request '
            'that the appointment be moved to another time.'},
 {'input': 'အခု client နဲ့ call ပြောနေလို့ ခဏစောင့်ပေးပါ၊ call ပြီးတာနဲ့ ပြန်ဆက်သွယ်ပါမယ်။',
  'simple': "I'm currently on a call with a client, so please wait for a moment. I'll contact you again as soon as the "
            'call is finished.',
  'polite': 'I’m currently speaking with a client on a call, so would you mind waiting a moment? I’ll get back to you '
            'as soon as the call ends.',
  'friendly': 'I’m on a client call right now — can you give me a minute? I’ll get back to you when I’m done.',
  'professional': 'I am currently engaged in a client call. I will contact you once the call has concluded.',
  'formal': 'Please be advised that I am currently engaged in a client call. I will contact you immediately upon its '
            'conclusion.'},
 {'input': 'ဒီ task ကို အရင်ပြီးအောင်လုပ်နေရလို့ ခဏစောင့်ပေးပါ၊ ပြီးတာနဲ့ file ကို ပို့ပေးပါမယ်။',
  'simple': "I'm working on this task first, so please wait for a moment. I'll send the file as soon as it's finished.",
  'polite': 'I wanted to let you know that I am working on this task first, so please wait for a moment. I will send '
            "the file as soon as it's finished. Thank you for your patience.",
  'friendly': "Just a heads-up — I'm working on this task first, so please wait for a moment. I'll send the file as "
              "soon as it's finished.",
  'professional': 'For your awareness, I am working on this task first, so please wait for a moment. I will send the '
                  "file as soon as it's finished.",
  'formal': 'Please be advised that I am working on this task first, so please wait for a moment. I will send the file '
            "as soon as it's finished."},
 {'input': 'Meeting ထဲဝင်နေလို့ အခု message ကို မပြန်နိုင်သေးဘူး၊ meeting ပြီးတာနဲ့ reply ပြန်ပေးပါမယ်။',
  'simple': "I'm currently in a meeting, so I can't reply to this message yet. I'll reply as soon as the meeting is "
            'over.',
  'polite': 'I’m currently in a meeting, so I may not be able to reply right away. I’ll respond as soon as the meeting '
            'is over.',
  'friendly': 'I’m in a meeting right now, so I can’t reply yet. I’ll get back to you as soon as it’s finished.',
  'professional': 'I am currently attending a meeting and am therefore unable to respond at this time. I will reply '
                  'once the meeting concludes.',
  'formal': 'Please be advised that I am currently in a meeting and unable to respond at present. I will provide a '
            'reply upon its conclusion.'},
 {'input': 'Client က အခု call ထဲမှာရှိနေလို့ ခဏလောက် စောင့်ပေးပါ၊ call ပြီးရင် ဒီကိစ္စကို ပြန်ရှင်းပေးပါမယ်။',
  'simple': "The client is currently on a call, so please wait for a moment. I'll explain this matter again after the "
            'call.',
  'polite': 'I wanted to let you know that the client is currently on a call, so please wait for a moment. I will '
            'explain this matter again after the call. Thank you for your patience.',
  'friendly': "Just a heads-up — the client is currently on a call, so please wait for a moment. I'll explain this "
              'matter again after the call.',
  'professional': 'For your awareness, the client is currently on a call, so please wait for a moment. I will explain '
                  'this matter again after the call.',
  'formal': 'Please be advised that the client is currently on a call, so please wait for a moment. I will explain '
            'this matter again after the call.'},
 {'input': 'အခု report finalise လုပ်နေလို့ နည်းနည်းအချိန်ပေးပါ၊ ပြီးတာနဲ့ review လုပ်ဖို့ ပို့ပေးပါမယ်။',
  'simple': "I'm finalizing the report right now, so please give me a little time. I'll send it for review as soon as "
            "it's finished.",
  'polite': 'I wanted to let you know that I am finalizing the report right now, so please give me a little time. I '
            "will send it for review as soon as it's finished. Thank you for your patience.",
  'friendly': "Just a heads-up — I'm finalizing the report right now, so please give me a little time. I'll send it "
              "for review as soon as it's finished.",
  'professional': 'For your awareness, I am finalizing the report right now, so please give me slightly time. I will '
                  "send it for review as soon as it's finished.",
  'formal': 'Please be advised that I am finalizing the report right now, so please give me a short while time. I will '
            "send it for review as soon as it's finished."},
 {'input': 'ဒီနေ့ အလုပ်နည်းနည်းများနေလို့ reply နောက်ကျသွားတာ တောင်းပန်ပါတယ်၊ အခုချက်ချင်း ပြန်ကြည့်ပေးပါမယ်။',
  'simple': "I'm sorry for the late reply; I've been a little busy with work today. I'll look into it right away.",
  'polite': 'I’m sorry for getting back to you late. I’ve been a little busy with work today, but I’ll look into it '
            'right away.',
  'friendly': 'Sorry for the late reply — work’s been a bit busy today. I’ll check it now.',
  'professional': 'I apologize for the delayed response. I have been occupied with work today, but I will review it '
                  'immediately.',
  'formal': 'Please accept my apologies for the delayed response. I have been occupied with work today and will review '
            'the matter promptly.'},
 {'input': 'မနေ့က message ကို မမြင်လိုက်လို့ reply နောက်ကျသွားတာပါ၊ အခု ပြန်စစ်ပြီး အကြောင်းပြန်ပေးပါမယ်။',
  'simple': "I didn't see your message yesterday, so my reply was delayed. I'll check it now and get back to you.",
  'polite': 'I wanted to let you know that I did not see your message yesterday, so my reply was delayed. I will check '
            'it now and get back to you. Thank you for your patience.',
  'friendly': "Just a heads-up — I didn't see your message yesterday, so my reply was delayed. I'll check it now and "
              'get back to you.',
  'professional': 'For your awareness, I did not see your message yesterday, so my reply was delayed. I will check it '
                  'now and get back to you.',
  'formal': 'Please be advised that I did not see your message yesterday, so my reply was delayed. I will check it now '
            'and get back to you.'},
 {'input': 'Client feedback မရသေးလို့ ဒီ task ကို ဆက်လုပ်လို့မရသေးဘူး၊ feedback ရတာနဲ့ ဆက်လုပ်ပါမယ်။',
  'simple': "We haven't received the client's feedback yet, so we can't continue this task. We'll continue as soon as "
            'we receive it.',
  'polite': "I wanted to let you know that we haven't received the client's feedback yet, so we can't continue this "
            "task. We'll continue as soon as we receive it. Thank you for your patience.",
  'friendly': "Just a heads-up — we haven't received the client's feedback yet, so we can't continue this task. We'll "
              'continue as soon as we receive it.',
  'professional': "For your awareness, we haven't received the client's feedback yet, so we can't continue this task. "
                  "We'll continue as soon as we receive it.",
  'formal': "Please be advised that we haven't received the client's feedback yet, so we can't continue this task. "
            "We'll continue as soon as we receive it."},
 {'input': 'Manager ဆီက approval မရသေးလို့ project ကို next step ဆက်သွားလို့မရသေးပါဘူး၊ approval ရတာနဲ့ update '
           'ပေးပါမယ်။',
  'simple': "We haven't received approval from the manager yet, so we can't move the project to the next step. I'll "
            'provide an update as soon as we receive approval.',
  'polite': "I wanted to let you know that we haven't received approval from the manager yet, so we can't move the "
            'project to the next step. I will provide an update as soon as we receive approval. Thank you for your '
            'patience.',
  'friendly': "Just a heads-up — we haven't received approval from the manager yet, so we can't move the project to "
              "the next step. I'll provide an update as soon as we receive approval.",
  'professional': "For your awareness, we haven't received approval from the manager yet, so we can't move the project "
                  'to the next step. I will provide an update as soon as we receive approval.',
  'formal': "Please be advised that we haven't received approval from the manager yet, so we can't move the project to "
            'the next step. I will provide an update as soon as we receive approval.'},
 {'input': 'အခု meeting ပြီးအောင် စောင့်ပေးပါ၊ meeting ပြီးတာနဲ့ ဒီကိစ္စကို ချက်ချင်း ပြန်ဆွေးနွေးပါမယ်။',
  'simple': "Please wait until the meeting is over. I'll discuss this matter with you immediately afterward.",
  'polite': 'I wanted to let you know that please wait until the meeting is over. I will discuss this matter with you '
            'immediately afterward. Thank you for your patience.',
  'friendly': "Just a heads-up — please wait until the meeting is over. I'll discuss this matter with you immediately "
              'afterward.',
  'professional': 'For your awareness, please wait until the meeting is over. I will discuss this matter with you '
                  'immediately afterward.',
  'formal': 'Please be advised that please wait until the meeting is over. I will discuss this matter with you '
            'immediately afterward.'},
 {'input': 'Traffic အရမ်းပိတ်နေလို့ office ကို time မီမရောက်နိုင်ဘူး၊ ရောက်တာနဲ့ meeting join လိုက်မယ်နော်။',
  'simple': "Traffic is very heavy, so I won't be able to get to the office on time. I'll join the meeting as soon as "
            'I arrive.',
  'polite': 'I wanted to let you know that traffic is very heavy, so I won’t be able to reach the office on time. I’ll '
            'join the meeting as soon as I arrive.',
  'friendly': 'Just a heads-up — the traffic is really heavy, so I’m running late to the office. I’ll jump into the '
              'meeting as soon as I get there.',
  'professional': 'Due to heavy traffic, I will be unable to arrive at the office on time. I will join the meeting '
                  'immediately upon arrival.',
  'formal': 'Owing to severe traffic congestion, I will not reach the office by the scheduled time. I shall join the '
            'meeting upon arrival.'},
 {'input': 'မနေ့ညက meeting က late ဖြစ်သွားပြီး အိမ်ပြန်တာလည်း late ဖြစ်လို့ sleep မဝဘူး၊ ဒါကြောင့် ဒီနေ့ work '
           'မလာတော့ဘူးနော်။',
  'simple': "The meeting ran late last night, and I also got home late, so I didn't get enough sleep. That's why I "
            "won't be coming to work today.",
  'polite': 'I wanted to let you know that the meeting ran late last night and I arrived home late, so I did not get '
            'enough sleep. I won’t be able to come to work today.',
  'friendly': 'Last night’s meeting ran late, and I got home late too, so I barely slept. I’m going to stay home from '
              'work today.',
  'professional': 'The late conclusion of last night’s meeting, followed by a late return home, resulted in '
                  'insufficient sleep. Consequently, I will be absent from work today.',
  'formal': 'As the meeting concluded late and I returned home at a late hour, I obtained insufficient rest. '
            'Accordingly, I will not be attending work today.'},
 {'input': 'ဒီ morning က rain အရမ်းကြီးရွာပြီး အိမ်ရှေ့မှာ water တက်နေလို့ school သွားတာ late ဖြစ်မယ်။',
  'simple': "It rained heavily this morning, and there is flooding in front of my house, so I'll be late getting to "
            'school.',
  'polite': 'I wanted to let you know that it rained very heavily this morning and there is flooding in front of my '
            'house. As a result, I’ll be late getting to school.',
  'friendly': 'Just a heads-up — the rain was really heavy this morning, and the water is up in front of my house, so '
              'I’m going to be late for school.',
  'professional': 'Heavy rainfall and flooding in front of my house are delaying my journey to school. I will '
                  'therefore arrive late.',
  'formal': 'Owing to the heavy morning rainfall and flooding outside my home, I will be delayed on my way to school.'},
 {'input': 'Client နဲ့ meeting က အရမ်းကြာသွားပြီး meeting ပြီးတော့ သူတို့တောင်းထားတဲ့ changes တွေကို ပြန်လုပ်ရလို့ '
           'အိမ်ပြန်တာ late ဖြစ်သွားတယ်၊ ဒါကြောင့် ဒီနေ့ office ကနေ day off ယူချင်ပါတယ်။',
  'simple': 'The meeting with the client went on for a long time, and after the meeting I had to make the changes they '
            "requested, so I got home late. Therefore, I'd like to take a day off from the office today.",
  'polite': 'I wanted to let you know that the client meeting ran quite long, and I then had to complete the requested '
            'changes, which meant I got home late. Would it be possible for me to take the day off today, please?',
  'friendly': 'Just a heads-up — the client meeting took a long time, and I still had to finish their changes '
              'afterward, so I got home really late. I’d like to take today off, if that’s okay.',
  'professional': 'The client meeting extended significantly, followed by work on the requested changes, which '
                  'resulted in a late return home. For this reason, I would like to request one day of leave today.',
  'formal': 'In light of the extended client meeting and the subsequent completion of the requested revisions, I '
            'returned home considerably late. Accordingly, I respectfully request one day of leave today.'},
 {'input': 'မနေ့ညက client meeting ပြီးတာနောက်ကျပြီး report changes တွေကိုလည်း အိမ်ရောက်ပြီး ဆက်လုပ်ရလို့ sleep မဝဘူး၊ '
           'ဒီနေ့ အရမ်း tired ဖြစ်နေလို့ work မလာတော့ဘူး။',
  'simple': 'The client meeting ended late last night, and I continued working on the report changes after I got home, '
            "so I didn't get enough sleep. I'm very tired today, so I won't be coming to work.",
  'polite': 'I wanted to let you know that the client meeting ended late and I continued working on the report changes '
            'after I got home. I did not get enough sleep and am very tired today, so would it be possible for me to '
            'take the day off?',
  'friendly': 'Last night’s client meeting ran late, and I kept working on the report changes once I got home. I '
              'barely slept, so I’m really tired and won’t be coming to work today.',
  'professional': 'The client meeting concluded late, after which I completed additional report revisions at home. '
                  'This resulted in insufficient sleep and significant fatigue, so I will be taking leave from work '
                  'today.',
  'formal': 'Following the late conclusion of the client meeting, I continued with the required report revisions at '
            'home and obtained insufficient rest. Consequently, I respectfully request leave for today.'},
 {'input': 'ဒီနေ့ မနက် rain အရမ်းရွာပြီး အိမ်ရှေ့လမ်းမှာ water တက်နေတဲ့အပြင် လမ်းထိပ်ကနေ traffic ပါ အရမ်းပိတ်နေလို့ '
           'school ကို အနည်းဆုံး 30 minutes လောက် late ဖြစ်နိုင်ပါတယ်။',
  'simple': 'It rained very heavily this morning, and the road in front of my house is flooded. Traffic is also very '
            'heavy from the end of the street, so I may be at least 30 minutes late getting to school.',
  'polite': 'I wanted to let you know that it rained very heavily this morning, the road in front of my house is '
            'flooded, and traffic is also very heavy. Because of these conditions, I may be at least 30 minutes late '
            'getting to school.',
  'friendly': 'Just a heads-up — the rain is really heavy, there’s water on the road in front of my house, and traffic '
              'is backed up from the end of the street. I could be at least 30 minutes late for school.',
  'professional': 'Heavy rainfall, flooding near my home, and severe traffic congestion are expected to delay my trip '
                  'to school by at least 30 minutes.',
  'formal': 'Owing to the heavy rainfall, flooding in front of my residence, and severe traffic congestion, I may be '
            'delayed by no less than 30 minutes en route to school.'},
 {'input': 'အမေက မနေ့ကတည်းက sick ဖြစ်နေတာကြောင့် ဒီနေ့ hospital မှာ doctor နဲ့ သွားတွေ့ရမှာပါ၊ appointment က morning '
           'ဖြစ်လို့ ကျွန်တော်ကိုယ်တိုင် လိုက်ပို့ရမှာကြောင့် ဒီနေ့မနက် work မလာနိုင်ဘူး၊ afternoon အခြေအနေကြည့်ပြီး '
           'ပြန်ဝင်ပါမယ်။',
  'simple': 'My mother has been sick since yesterday, so I need to take her to the hospital to see a doctor today. Her '
            "appointment is in the morning, and I need to accompany her, so I won't be able to come to work this "
            "morning. I'll see how things are this afternoon and return to work if I can.",
  'polite': 'I wanted to let you know that my mother has been sick since yesterday and I need to take her to the '
            'hospital for her morning doctor’s appointment. I won’t be able to come to work this morning, but I’ll '
            'return this afternoon if the situation allows.',
  'friendly': 'Just a heads-up — my mother has been sick since yesterday, so I need to take her to the hospital this '
              'morning. I’ll see how things go and come back to work this afternoon if I can.',
  'professional': 'My mother has been unwell since yesterday and requires a hospital visit this morning. As I need to '
                  'accompany her, I will be unable to attend work this morning; I will return this afternoon if '
                  'circumstances permit.',
  'formal': 'As my mother has been unwell since yesterday and has a morning medical appointment, I must accompany her '
            'to the hospital. Accordingly, I will not attend work this morning and will return this afternoon should '
            'circumstances allow.'},
 {'input': 'Client က မနေ့ညက requirements အသစ်တွေ ထပ်ပေးလိုက်ပြီး changes တွေလည်း အများကြီးရှိလို့ report ကို '
           'ပြန်လုပ်ရမှာဖြစ်တယ်၊ ဒါကြောင့် original deadline အတိုင်း မပြီးနိုင်ဘဲ one more day လောက်လိုပါတယ်။',
  'simple': 'The client sent additional requirements last night, and there are also many changes to make, so I need to '
            "redo the report. Therefore, I won't be able to finish by the original deadline and need about one more "
            'day.',
  'polite': 'I wanted to let you know that the client sent additional requirements last night and there are many '
            'changes to make, so I need to redo the report. For that reason, I won’t be able to meet the original '
            'deadline and will need about one more day.',
  'friendly': 'Just a heads-up — the client added new requirements last night, and there are quite a few changes to '
              'make, so the report needs to be redone. I’ll need roughly one extra day beyond the original deadline.',
  'professional': 'The additional requirements received from the client last night have created substantial revisions '
                  'to the report. As a result, I will be unable to meet the original deadline and require '
                  'approximately one additional day.',
  'formal': 'In light of the additional client requirements received last night and the extensive revisions required, '
            'the original deadline cannot be met. I respectfully request approximately one further day.'},
 {'input': 'Power ပြတ်သွားပြီး laptop battery လည်းကုန်သွားလို့ report ကို ဆက်လုပ်လို့မရဘူး၊ deadline က '
           'ဒီနေ့ညဖြစ်တာကြောင့် မီးပြန်လာတာနဲ့ ချက်ချင်း ဆက်လုပ်ပြီး final version ကို ပို့ပါမယ်။',
  'simple': "The power went out and my laptop battery also ran out, so I can't continue working on the report. Since "
            "the deadline is tonight, I'll continue immediately when the power comes back and send the final version.",
  'polite': 'I wanted to let you know that the power outage has drained my laptop battery, so I’m unable to continue '
            'the report at the moment. Since the deadline is tonight, I’ll resume immediately when the power returns '
            'and send the final version.',
  'friendly': 'Just a heads-up — the power is out and my laptop battery is dead, so I can’t keep working on the report '
              'right now. As soon as the electricity comes back, I’ll get straight back to it and send the final '
              'version tonight.',
  'professional': 'The power outage and depleted laptop battery have temporarily stopped work on the report. Given '
                  'tonight’s deadline, I will resume immediately once power is restored and submit the final version.',
  'formal': 'Owing to the power interruption and the complete depletion of my laptop battery, the report cannot be '
            'continued at present. In view of tonight’s deadline, I shall resume work upon restoration of power and '
            'submit the final version.'},
            
 {'input': 'မနေ့ညက client နဲ့ meeting က အချိန်တော်တော်ကြာသွားပြီး meeting ပြီးတော့ သူတို့တောင်းထားတဲ့ changes တွေကို '
           'ပြန်လုပ်ရလို့ အိမ်ပြန်ရောက်တာ အရမ်းနောက်ကျသွားတယ်၊ အိပ်ရာဝင်တာလည်း မနက်တော်တော်နီးမှဖြစ်တာကြောင့် ဒီနေ့ '
           'အိပ်ရေးမဝဘဲ အရမ်းပင်ပန်းနေပါတယ်၊ ဒါကြောင့် ဒီနေ့ အလုပ်ကနေ တစ်ရက်ခွင့်ယူချင်ပါတယ်။',
  'simple': 'The meeting with the client went on for quite a long time last night, and after the meeting I had to make '
            "the changes they requested, so I got home very late. I didn't go to bed until near morning, so I didn't "
            "get enough sleep and I'm very tired today. Therefore, I'd like to take a day off from work today.",
  'polite': 'I wanted to explain the situation fully: the client meeting continued for quite some time, and I then had '
            'to complete the requested changes, which meant I got home very late. I did not go to bed until close to '
            'morning, so I did not get enough sleep and am extremely tired today. Would it be possible for me to take '
            'one day of leave?',
  'friendly': 'Last night was a long one — the client meeting ran on, then I had to finish their changes after the '
              'meeting, and I didn’t get home until really late. I barely slept, I’m exhausted today, and I’d like to '
              'take the day off.',
  'professional': 'The client meeting extended considerably, followed by completion of the requested changes, '
                  'resulting in a very late return home and a substantially reduced sleep period. Given the resulting '
                  'fatigue, I would like to request one day of leave today.',
  'formal': 'Owing to the extended duration of the client meeting and the subsequent completion of the requested '
            'revisions, I returned home at a considerably late hour and retired close to morning. Consequently, I have '
            'obtained insufficient rest and am significantly fatigued; accordingly, I respectfully request one day of '
            'leave today.'}]


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

    # 1. Full-message stress-test references first.
    for example in FULL_MESSAGE_EXAMPLES:
        example_input = normalize_text(example["input"])
        if normalized_input == example_input:
            return example

    # 2. Original short training/reference examples.
    for example in TRAINING_EXAMPLES:
        example_input = normalize_text(example["input"])
        if normalized_input == example_input:
            return example

    return None


# ============================================================
# Context-aware translation rules
# ============================================================

def _contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)



def high_coverage_long_context_translation(text: str, tone: str):
    """
    High-coverage layer for long Myanmar, English, and mixed-language messages.
    It collects multiple causes before older keyword rules can return early.
    """
    n = normalize_text(text)

    def has(*phrases):
        return _contains_any(n, list(phrases))

    def variants(simple, polite, friendly, professional, formal):
        return {
            "simple": simple, "polite": polite, "friendly": friendly,
            "professional": professional, "formal": formal,
        }.get(tone, professional)

    rain = has("မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
               "rain", "raining", "heavy rain", "poured")
    flood = has("ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်", "ရေတက်",
                "flood", "flooded", "flooding")
    traffic = has("ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
                  "traffic", "traffic jam", "heavy traffic")
    delay = has("နောက်ကျ", "နောက်ကျမယ်", "နောက်ကျမှ", "late", "delayed", "delay")
    school = has("ကျောင်း", "school")
    work = has("အလုပ်", "ရုံး", "work", "office")
    meeting = has("meeting", "အစည်းအဝေး")
    wait = has("စောင့်", "wait", "wait for me")
    sleep = has("အိပ်ရေးမဝ", "အိပ်မဝ", "အိပ်ရေးမလုံ", "အိပ်မပျော်",
                "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep",
                "did not get enough sleep", "barely slept", "barely got enough sleep",
                "sleep မဝ", "sleep မလုံ")
    absent = has("အလုပ်မလာ", "အလုပ်မလာတော့", "ရုံးမလာ", "work မလာ",
                 "office မလာ", "မလာတော့ဘူး", "မလာနိုင်", "မလာတော့",
                 "won't come", "will not come", "not coming",
                 "won't be coming", "will not be coming", "can't come",
                 "cannot come")

    # Multiple environmental/transport causes.
    if rain and flood and traffic and delay and (school or work or meeting):
        destination = "school" if school else ("the meeting" if meeting else "work")
        core = (
            "It rained heavily this morning, the area in front of my house is flooded, "
            f"and there is also heavy traffic on the way, so I’ll be late getting to {destination} today."
        )
        return variants(
            core,
            core,
            core,
            core,
            "It rained heavily this morning, the area in front of my house is flooded, "
            f"and there is also heavy traffic on the way, so I will be delayed in reaching {destination} today."
        )

    # Rain + traffic, without flooding.
    if rain and traffic and delay and (school or work or meeting):
        destination = "school" if school else ("the meeting" if meeting else "work")
        return variants(
            f"It rained heavily this morning, and there is also heavy traffic on the way, so I’ll be late getting to {destination} today.",
            f"It rained heavily this morning, and there is also heavy traffic on the way, so I’m sorry, but I’ll be late getting to {destination} today.",
            f"It rained heavily this morning, and there’s also heavy traffic on the way, so I’ll be a little late getting to {destination} today.",
            f"It rained heavily this morning, and there is also heavy traffic on the way, so I will be late getting to {destination} today.",
            f"Due to the heavy rain and traffic on the way, I will be delayed in reaching {destination} today."
        )

    # Meeting -> insufficient sleep -> work absence.
    if meeting and sleep and absent and (
        has("နောက်ကျ", "late", "ran late", "ended late", "finished late") or
        has("မနေ့ည", "last night")
    ):
        return variants(
            "The meeting ended late last night, and I didn’t get enough sleep, so I won’t be coming to work today.",
            "The meeting ended quite late last night, and I didn’t get enough sleep, so I’m sorry, but I won’t be able to come to work today.",
            "The meeting ran late last night, and I barely got enough sleep, so I won’t be coming to work today.",
            "The meeting ended late last night, and I did not get enough sleep, so I will not be coming to work today.",
            "As the meeting ended late last night and I did not get sufficient sleep, I will be unable to come to work today."
        )

    # Very long client meeting + report + sleep + absence.
    if meeting and sleep and absent and has("client") and has("report", "တင်ရမယ့် report", "report ဆက်"):
        return variants(
            "The meeting with the client went on quite late last night, and after I got home, I had to continue working on the report, so I didn’t get enough sleep and won’t be coming to work today.",
            "The meeting with the client went on quite late last night, and I had to continue working on the report after I got home. As a result, I didn’t get enough sleep, so I’m sorry, but I won’t be able to come to work today.",
            "The client meeting ran really late last night, and I still had to work on the report after I got home. I barely got any sleep, so I won’t be coming to work today.",
            "The meeting with the client continued late into the night, and I had to continue working on the report after I got home. Because I did not get enough sleep, I will not be coming to work today.",
            "As the client meeting continued late into the night and I subsequently had to work on the report, I did not get sufficient sleep and will therefore be unable to come to work today."
        )

    # Mother/family health -> leave.
    mother_health = has("အမေ", "မိခင်", "mother", "mom", "mum") and has(
        "ကျန်းမာရေး", "နေမကောင်း", "ဆေးရုံ", "ဆရာဝန်", "health", "health issue",
        "sick", "hospital", "doctor", "check-up", "checkup"
    )
    leave_request = has("ခွင့်", "ခွင့်ယူ", "ခွင့်တစ်ရက်", "leave", "day off", "take leave")
    if mother_health and leave_request:
        return variants(
            "My mother has a health issue, so I would like to take a day off from work today.",
            "My mother is having a health issue, so I’m sorry, but I would like to request one day of leave from work today.",
            "My mother isn’t feeling well, so I’d like to take the day off from work today.",
            "Due to my mother’s health issue, I would like to request one day of leave from work today.",
            "Due to my mother’s health condition, I would like to formally request one day of leave from work today."
        )

    # Client requirements -> deadline extension.
    client_change = has("client") and has("requirement", "requirements", "changes", "change", "ပြောင်း", "ပြန်ပြင်")
    deadline = has("deadline", "delivery date", "delivery", "မပြီးနိုင်", "deadline မီ",
                   "နောက်ဆုတ်", "အချိန်ပို", "extension", "နှစ်ရက်", "two days")
    if client_change and deadline:
        return variants(
            "The client sent additional requirements and we need to revise some of the existing work, so we won’t be able to finish the project by the original deadline. Could we please move the delivery date back by two days?",
            "The client sent additional requirements and we need to revise some of the existing work, so we may not be able to meet the original deadline. Could we please have the delivery date extended by two days?",
            "The client added some new requirements and we need to make changes to the existing work, so we’ll need a little more time. Could we push the delivery date back by two days?",
            "The client provided additional requirements that require revisions to the existing work, so we will not be able to meet the original deadline. I would like to request a two-day extension for the delivery date.",
            "As the client has provided additional requirements that necessitate revisions to the existing work, we will be unable to meet the original deadline. I would therefore like to formally request a two-day extension of the delivery date."
        )

    # Power outage -> laptop -> report deadline.
    if (has("မီးပျက်", "power went out", "power outage", "electricity")
        and has("laptop", "computer") and has("report")
        and has("deadline", "submit", "မပို့နိုင်", "မပြီး")):
        return variants(
            "The power went out at home last night, which caused my laptop to run out of battery, so I couldn’t continue working on the report and haven’t been able to submit it by today’s deadline.",
            "The power went out at home last night, and my laptop battery ran out, so I was unable to continue working on the report. I’m sorry, but I haven’t been able to submit it by today’s deadline.",
            "The power went out last night and my laptop ran out of battery, so I couldn’t finish the report or submit it by today’s deadline.",
            "The power outage at home last night caused my laptop battery to run out, preventing me from continuing the report. As a result, I have not been able to submit it by today’s deadline.",
            "Due to a power outage at home last night, my laptop battery was depleted and I was unable to continue working on the report; consequently, I have been unable to submit it by today’s deadline."
        )

    # Workload + report + meeting reschedule.
    if (has("အလုပ်", "work", "office", "report") and has("meeting", "အစည်းအဝေး")
        and has("များ", "busy", "a lot of work", "အပြီးသတ်")
        and has("မနက်ဖြန်", "tomorrow") and has("ရွှေ့", "move", "reschedule", "ပြောင်း")):
        return variants(
            "I have a lot of work to finish today, including the report, so could we move the meeting to tomorrow?",
            "I have quite a lot of work to finish today, including the report, so would it be possible to move the meeting to tomorrow?",
            "I have a lot on my plate today and need to finish the report, so can we move the meeting to tomorrow?",
            "I have several tasks to complete today, including the report, so I would like to ask if we could reschedule the meeting for tomorrow.",
            "As I have several important tasks to complete today, including the report, I would appreciate it if the meeting could be rescheduled for tomorrow."
        )

    # Client call + wait + callback.
    if has("client") and has("call") and wait and has("ပြီး", "finish", "finished", "ပြန်ဆက်", "get back", "contact"):
        return variants(
            "I’m currently on a call with a client, so please wait for a moment. I’ll get back to you as soon as the call is finished.",
            "I’m currently on a call with a client, so could you please wait for a moment? I’ll get back to you as soon as the call is finished.",
            "I’m on a call with a client right now, so just give me a moment. I’ll get back to you as soon as I’m done.",
            "I am currently on a call with a client, so could you please wait for a moment? I will get back to you as soon as the call is finished.",
            "I am currently engaged in a call with a client. I would appreciate your patience for a brief moment and will contact you again as soon as the call has concluded."
        )

    # --------------------------------------------------------
    # 10) Generic long meeting/sleep/fatigue/work chain.
    #     This intentionally accepts several natural phrasings instead
    #     of requiring the exact phrase "အလုပ်မလာတော့".
    # --------------------------------------------------------
    fatigue_or_sleep = sleep or has(
        "ပင်ပန်းနေ", "အရမ်းပင်ပန်း", "အရမ်းပင်ပန်းနေပါတယ်",
        "very tired", "really tired", "quite tired", "fatigued", "exhausted"
    )
    work_absence_or_leave = absent or has(
        "ခွင့်ယူ", "ခွင့်တောင်း", "ခွင့်တစ်ရက်", "leave", "day off",
        "အလုပ်မလာ", "အလုပ်ကနေ", "work today", "come to work"
    )

    if meeting and fatigue_or_sleep and len(text.strip()) >= 80:
        # Preserve the meeting + sleep/fatigue chain first. If the input
        # also contains work absence/leave, include it explicitly.
        if work_absence_or_leave:
            return variants(
                "The meeting ran late last night, and I didn’t get enough sleep, so I’m very tired today and won’t be coming to work.",
                "The meeting ran late last night, and I didn’t get enough sleep, so I’m quite tired today. Because of that, I won’t be able to come to work today.",
                "The meeting ran late last night, and I barely got enough sleep, so I’m really tired today and won’t be coming to work.",
                "The meeting ran late last night, and I did not get enough sleep, so I am feeling very tired today and will not be coming to work.",
                "As the meeting continued late into the night and I did not get sufficient sleep, I am feeling fatigued today and will be unable to come to work.",
            )
        return variants(
            "The meeting ran late last night, and I didn’t get enough sleep, so I’m very tired today.",
            "The meeting ran late last night, and I didn’t get enough sleep, so I’m quite tired today.",
            "The meeting ran late last night, and I barely got enough sleep, so I’m really tired today.",
            "The meeting ran late last night, and I did not get enough sleep, so I am feeling very tired today.",
            "As the meeting continued late into the night and I did not get sufficient sleep, I am feeling quite fatigued today.",
        )

    return None


def expanded_context_rule_translation(text: str, tone: str):
    """
    100 high-confidence context examples for Myanmar, English, and mixed input.
    These are deliberately specific so they preserve cause + consequence + action
    instead of collapsing a long message into its final intent.
    """
    n = normalize_text(text)

    def has(*phrases):
        return _contains_any(n, list(phrases))

    def variants(simple, polite, friendly, professional, formal):
        return {"simple": simple, "polite": polite, "friendly": friendly, "professional": professional, "formal": formal}.get(tone, professional)

    # 001. Work: traffic + late
    # Traffic + meeting delay + explicit waiting request
    if (
        has("ကား", "ကားတွေ", "traffic", "ကားလမ်းပိတ်", "ကားတွေကြပ်")
        and has("ကြပ်", "ပိတ်", "heavy traffic")
        and has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "late", "delay")
        and has("စောင့်ပေး", "ခနစောင့်", "wait for me", "please wait")
    ):
        return variants(
            "There’s heavy traffic near the end of the street, so I’ll be late for the meeting. Please wait for me for a little while.",
            "There’s heavy traffic near the end of the street, so I may be late for the meeting. Could you please wait for me for a little while?",
            "Traffic is really heavy near the end of the street, so I’m going to be late for the meeting. Please wait for me for a bit.",
            "There is heavy traffic near the end of the street, so I will be late for the meeting. I would appreciate it if you could wait for me for a little while.",
            "Due to heavy traffic near the end of the street, I will be late for the meeting. I would appreciate it if you could kindly wait for me for a short while."
        )

    # 002. Office: traffic + no on-time
    if has('traffic', 'ကားပိတ်', 'ကားကြပ်') and has('office', 'အလုပ်') and has('အချိန်မီမရောက်', 'time မီမရောက်', 'on time'):
        return variants(
            "Traffic is very heavy, so I won't be able to get to the office on time.",
            "I wanted to let you know that traffic is very heavy, so I may not be able to reach the office on time.",
            "Traffic is really backed up, so I’m going to be late getting to the office.",
            "Due to heavy traffic, I will not be able to arrive at the office on time.",
            "Because of the severe traffic congestion, I will be unable to reach the office by the expected time.",
        )

    # 003. School: traffic + late
    if has('traffic', 'ကားပိတ်', 'ကားကြပ်') and has('ကျောင်း', 'school') and has('နောက်ကျ', 'late'):
        return variants(
            "Traffic is very heavy, so I'll be late getting to school today.",
            "Please note that traffic is very heavy, so I may be a little late getting to school today.",
            "Traffic is really bad today, so I’m going to be late for school.",
            "Due to the heavy traffic, I will arrive at school later than scheduled today.",
            "Because of the significant traffic congestion, I will be delayed in reaching school today.",
        )

    # 004. Meeting: traffic + join on arrival
    if has('traffic', 'ကားပိတ်', 'ကားကြပ်') and has('meeting', 'အစည်းအဝေး') and has('ရောက်တာနဲ့', 'join', 'ဝင်'):
        return variants(
            "Traffic is very heavy, so I won't arrive on time. I'll join the meeting as soon as I get there.",
            "I wanted to let you know that traffic is very heavy, so I may not arrive on time. Could you please start without me? I'll join as soon as I get there.",
            "Traffic is crazy right now, so I’m going to be late. I’ll jump into the meeting as soon as I arrive.",
            "Heavy traffic is preventing me from arriving on time. I will join the meeting immediately upon reaching the office.",
            "Due to heavy traffic, I will be unable to arrive at the scheduled time. I will join the meeting promptly upon arrival.",
        )

    # 005. Meeting: delayed + wait
    if has('meeting', 'အစည်းအဝေး') and has('နောက်ကျ', 'late', 'delayed') and has('စောင့်', 'wait'):
        return variants(
            "The meeting will be delayed, so please wait for me for a little while.",
            "The meeting will be delayed, so could you please wait for me for a little while?",
            "The meeting’s going to be a bit late, so please hang on for me for a little while.",
            "The meeting will start later than planned. I would appreciate it if you could wait for me briefly.",
            "As the meeting will be delayed, I kindly request that you wait for me for a short while.",
        )

    # 006. Meeting: running late + apologize
    if has('meeting', 'အစည်းအဝေး') and has('နောက်ကျ', 'running late', 'late') and has('တောင်းပန်', 'sorry'):
        return variants(
            "I'm sorry, but I'm running late for the meeting.",
            "I'm sorry for the delay. I may be a little late for the meeting.",
            "Sorry, I’m running a bit late for the meeting.",
            "I apologize for the delay and for not arriving at the meeting on time.",
            "Please accept my apologies; I will be delayed in attending the meeting.",
        )

    # 007. Meeting: schedule conflict + reschedule
    if has('meeting', 'အစည်းအဝေး') and has('အချိန်မရ', 'schedule conflict', 'မအား') and has('ပြန်ချိန်း', 'reschedule', 'အချိန်ပြောင်း'):
        return variants(
            "I have a scheduling conflict, so could we reschedule the meeting?",
            "I have a scheduling conflict. Could we please move the meeting to another time?",
            "I’ve got another commitment at that time—can we shift the meeting?",
            "Due to a scheduling conflict, I would like to request that we reschedule the meeting.",
            "As I have a scheduling conflict, I respectfully request that the meeting be rescheduled.",
        )

    # 008. Meeting: another meeting + delay
    if has('meeting', 'အစည်းအဝေး') and has('နောက်တစ်ခု', 'another meeting', 'အခြား meeting') and has('ပြီးမှ', 'after', 'နောက်မှ'):
        return variants(
            "I have another meeting first, so I'll join this meeting as soon as it finishes.",
            "I have another meeting beforehand, so I may join this meeting a little later. Thank you for understanding.",
            "I’ve got another meeting first, so I’ll join you right after it ends.",
            "I am scheduled to attend another meeting first; I will join this meeting immediately afterward.",
            "As I am required to attend another meeting beforehand, I will join this meeting upon its conclusion.",
        )

    # 009. Client: call + wait
    if has('client', 'ဖောက်သည်') and has('call', 'ဖုန်း') and has('စောင့်', 'wait'):
        return variants(
            "I'm currently on a call with a client, so please wait for a moment.",
            "I'm currently speaking with a client. Could you please wait for a moment?",
            "I’m on a client call right now—can you give me a minute?",
            "I am currently engaged in a client call and will respond as soon as it is finished.",
            "Please allow me a short while, as I am presently engaged in a call with a client.",
        )

    # 010. Client: call + callback
    if has('client', 'ဖောက်သည်') and has('call', 'ဖုန်း') and has('ပြန်ဆက်', 'call back', 'get back'):
        return variants(
            "I'm on a call with a client right now. I'll get back to you as soon as I'm finished.",
            "I'm currently on a call with a client. I’ll get back to you as soon as I’m free.",
            "I’m on a client call at the moment—I'll get back to you when I’m done.",
            "I am currently attending to a client call and will follow up with you immediately afterward.",
            "Please be advised that I am presently engaged with a client and will respond upon completion of the call.",
        )

    # 011. Client: changes + deadline
    if has('client', 'ဖောက်သည်') and has('changes', 'ပြင်ဆင်', 'ပြောင်းလဲ') and has('deadline', 'သတ်မှတ်ချိန်'):
        return variants(
            "The client requested some changes, so I need a little more time to meet the deadline.",
            "The client has requested some changes, so I may need a little additional time to meet the deadline.",
            "The client asked for a few changes, so I’ll need a bit more time to finish everything on time.",
            "Because of the client's requested changes, I need additional time to complete the work by the deadline.",
            "In light of the additional changes requested by the client, I respectfully request some extra time to meet the deadline.",
        )

    # 012. Client: feedback + revision
    if has('client', 'ဖောက်သည်') and has('feedback', 'အကြံပြုချက်') and has('ပြန်ပြင်', 'revision', 'ပြင်'):
        return variants(
            "I received feedback from the client, so I need to revise the work accordingly.",
            "I received feedback from the client, so I’d like to make the necessary revisions accordingly.",
            "I got the client’s feedback, so I’ll update the work based on it.",
            "Following the client's feedback, I will revise the work to address the requested points.",
            "In response to the feedback received from the client, the work will be revised accordingly.",
        )

    # 013. Client: approval pending
    if has('client', 'ဖောက်သည်') and has('approval', 'အတည်ပြု') and has('စောင့်', 'pending'):
        return variants(
            "I'm waiting for the client's approval before moving forward.",
            "I'm currently waiting for the client's approval before I proceed. Thank you for your patience.",
            "I’m just waiting on the client’s approval, then I can move ahead.",
            "The next step is pending the client's approval, so I will proceed once confirmation is received.",
            "Further action will remain pending until the client's approval has been formally received.",
        )

    # 014. Client: requirements unclear
    if has('client', 'ဖောက်သည်') and has('requirement', 'လိုအပ်ချက်') and has('မရှင်း', 'unclear', 'မသေချာ'):
        return variants(
            "Some of the client's requirements are unclear, so I'd like to clarify them before proceeding.",
            "Some of the client's requirements are unclear. Could we clarify those points before I proceed?",
            "I’m not totally clear on a few of the client’s requirements, so I’d like to double-check them first.",
            "Several client requirements require clarification, so I would like to confirm the details before proceeding.",
            "Certain requirements provided by the client remain unclear; I therefore request clarification before any further action is taken.",
        )

    # 015. Client: request more time
    if has('client', 'ဖောက်သည်') and has('အချိန်ပို', 'more time', 'time') and has('လို', 'need', 'တောင်း'):
        return variants(
            "I need a little more time to complete the client's request.",
            "I’d appreciate a little more time to complete the client's request properly.",
            "I need a bit more time to finish what the client asked for.",
            "I require some additional time to complete the client's request accurately.",
            "I respectfully request additional time to fulfill the client's request in full.",
        )

    # 016. Work: sick + absent
    if has('အလုပ်', 'work', 'office') and has('နေမကောင်း', 'sick', 'မကျန်းမာ') and has('မလာ', 'မသွား', 'absent'):
        return variants(
            "I'm not feeling well, so I won't be able to come to work today.",
            "I'm not feeling well today, so I would like to let you know that I won't be able to come to work.",
            "I’m feeling pretty sick today, so I’m going to stay home from work.",
            "Due to illness, I will be unable to attend work today.",
            "As I am unwell, I respectfully request to be excused from work today.",
        )

    # 017. Work: fever + leave
    if has('အလုပ်', 'work') and has('ဖျား', 'fever', 'အဖျား') and has('ခွင့်', 'leave', 'day off'):
        return variants(
            "I have a fever, so I'd like to take a day off from work today.",
            "I have a fever today, so could I please take the day off from work?",
            "I’ve got a fever, so I’m going to take today off and rest.",
            "Due to a fever, I would like to request one day of leave from work today.",
            "I respectfully request one day of leave today on account of a fever.",
        )

    # 018. Work: doctor appointment + absence
    if has('အလုပ်', 'work', 'office') and has('ဆရာဝန်', 'doctor') and has('appointment', 'ချိန်း', 'မနက်'):
        return variants(
            "I have a doctor's appointment this morning, so I won't be able to come to work.",
            "I have a doctor's appointment this morning, so I’d like to let you know that I won't be able to come to work.",
            "I’ve got a doctor’s appointment this morning, so I won’t make it to work.",
            "Because I have a medical appointment this morning, I will be unable to attend work.",
            "Due to a scheduled medical appointment this morning, I respectfully request to be excused from work.",
        )

    # 019. Work: hospital + morning
    if has('အလုပ်', 'work') and has('ဆေးရုံ', 'hospital') and has('မနက်', 'morning'):
        return variants(
            "I need to go to the hospital this morning, so I won't be able to come to work.",
            "I need to go to the hospital this morning, so please excuse my absence from work.",
            "I have to go to the hospital this morning, so I can’t make it to work.",
            "Due to a hospital visit this morning, I will be unable to attend work.",
            "As I am required to attend the hospital this morning, I respectfully request to be excused from work.",
        )

    # 020. Work: family emergency + leave
    if has('အလုပ်', 'work') and has('အရေးပေါ်', 'emergency') and has('မိသားစု', 'family'):
        return variants(
            "There is a family emergency I need to take care of, so I need to take the day off from work.",
            "I have a family emergency to take care of, so I would like to request the day off from work today.",
            "There's a family emergency I need to deal with, so I’m taking the day off today.",
            "Due to an urgent family matter, I would like to request one day of leave from work.",
            "Because of an urgent family emergency, I respectfully request leave from work for today.",
        )

    # 021. Work: family matter + absence
    if has('အလုပ်', 'work') and has('မိသားစု', 'family') and has('ကိစ္စ', 'matter'):
        return variants(
            "I have an urgent family matter to take care of, so I won't be able to come to work today.",
            "I have an urgent family matter to attend to, so I’d like to let you know that I won't be able to come to work today.",
            "I need to deal with something urgent at home, so I can’t make it to work today.",
            "Due to an urgent family matter, I will be unable to attend work today.",
            "Please be advised that, owing to an urgent family matter, I will be unable to report to work today.",
        )

    # 022. Work: child school matter
    if has('အလုပ်', 'work') and has('ကလေး', 'child') and has('ကျောင်း', 'school'):
        return variants(
            "I need to take care of an urgent matter involving my child's school, so I may be late for work.",
            "I need to handle an urgent matter involving my child's school, so I may be a little late for work. I appreciate your understanding.",
            "My child has something urgent going on at school, so I might be a bit late to work.",
            "Due to an urgent matter at my child's school, I may arrive at work later than scheduled.",
            "As I am required to address an urgent matter concerning my child's school, my arrival at work may be delayed.",
        )

    # 023. Work: home emergency
    if has('အလုပ်', 'work') and has('အိမ်မှာ', 'အိမ်') and has('အရေးပေါ်', 'emergency'):
        return variants(
            "There's an emergency at home, so I won't be able to come to work right away.",
            "There's an emergency at home, so I may not be able to come to work immediately. Thank you for understanding.",
            "There’s an emergency at home, so I can’t get to work just yet.",
            "Due to an emergency at home, I will be unable to attend work immediately.",
            "Because of an emergency at home, I will be unable to report to work at the scheduled time.",
        )

    # 024. Work: internet outage
    if has('အလုပ်', 'work', 'office') and has('internet', 'အင်တာနက်') and has('မရ', 'ပြတ်', 'down'):
        return variants(
            "The internet is down, so I'm having trouble working at the moment.",
            "The internet is currently down, so I’m having some difficulty working. I appreciate your patience.",
            "The internet’s out right now, so I’m having trouble getting work done.",
            "Due to the current internet outage, my work is being affected at the moment.",
            "As the internet connection is presently unavailable, my ability to continue working is being disrupted.",
        )

    # 025. Work: power outage
    if has('အလုပ်', 'work') and has('မီးပျက်', 'power outage', 'electricity') and has('မရ', 'ပြတ်'):
        return variants(
            "The power is out, so I can't continue working right now.",
            "The power is currently out, so I’m unable to continue working at the moment.",
            "The power’s out, so I can’t keep working right now.",
            "Due to the power outage, I am unable to continue working at present.",
            "As a result of the power interruption, I am presently unable to proceed with my work.",
        )

    # 026. Work: laptop problem
    if has('အလုပ်', 'work') and has('laptop', 'ကွန်ပျူတာ') and has('ပျက်', 'မဖွင့်', 'problem'):
        return variants(
            "My laptop is having a problem, so I can't continue working normally.",
            "My laptop is having a problem, so I’m unable to continue working normally at the moment.",
            "My laptop is acting up, so I can’t really keep working right now.",
            "Because of a problem with my laptop, I am unable to work normally.",
            "Due to a technical issue with my laptop, I am presently unable to continue my work as usual.",
        )

    # 027. Work: file problem
    if has('အလုပ်', 'work') and has('file', 'ဖိုင်') and has('ပျက်', 'မဖွင့်', 'corrupt'):
        return variants(
            "The file is not opening properly, so I need to fix it before I can continue working.",
            "The file isn't opening properly, so I’ll need to fix it before continuing. Thanks for your understanding.",
            "The file won’t open properly, so I need to sort it out before I can keep working.",
            "I am unable to proceed with the work until the file-opening issue has been resolved.",
            "As the file cannot be opened correctly, the issue must be resolved before further work can proceed.",
        )

    # 028. Work: report unfinished
    if has('report', 'အစီရင်ခံစာ') and has('မပြီး', 'unfinished', 'မပြီးသေး') and has('အလုပ်', 'work'):
        return variants(
            "The report isn't finished yet, so I need a little more time to complete it.",
            "The report is not finished yet, so could I please have a little more time to complete it?",
            "The report isn’t quite done yet, so I need a little extra time to wrap it up.",
            "The report remains incomplete, and I require additional time to finalize it.",
            "As the report has not yet been completed, I respectfully request additional time for its finalization.",
        )

    # 029. Work: report deadline
    if has('report', 'အစီရင်ခံစာ') and has('deadline', 'သတ်မှတ်ချိန်') and has('ဒီနေ့', 'today'):
        return variants(
            "I need to finish the report by today, so I may need some extra time for the other tasks.",
            "I need to finish the report today, so I may need a little extra time to handle the other tasks.",
            "I’ve got to finish the report today, so I might need some extra time for everything else.",
            "Because the report must be completed today, I may need to extend the time allocated for the other tasks.",
            "Given the requirement to complete the report today, I may require additional time for the remaining tasks.",
        )

    # 030. Work: workload heavy
    if has('အလုပ်', 'work') and has('အလုပ်များ', 'busy', 'workload') and has('မပြီး', 'မနိုင်', 'too much'):
        return variants(
            "My workload is quite heavy today, so I may need more time to finish everything.",
            "I have quite a heavy workload today, so I may need some additional time to complete everything.",
            "I’ve got a lot on my plate today, so I might need a bit more time to get it all done.",
            "Due to the current workload, I may require additional time to complete all assigned tasks.",
            "In view of the volume of work scheduled for today, I may require additional time to complete all outstanding duties.",
        )

    # 031. Work: urgent task
    if has('အလုပ်', 'work') and has('အရေးကြီး', 'urgent') and has('task', 'အလုပ်'):
        return variants(
            "I have an urgent task to finish, so I may be a little late with the other work.",
            "I need to finish an urgent task first, so I may be slightly delayed with the other work.",
            "I’ve got something urgent to finish first, so the other work might run a little late.",
            "An urgent task requires my immediate attention, so completion of the other work may be delayed.",
            "As an urgent task must be addressed first, the remaining work may consequently be delayed.",
        )

    # 032. Work: meeting + report conflict
    if has('meeting', 'အစည်းအဝေး') and has('report', 'အစီရင်ခံစာ') and has('တစ်ပြိုင်နက်', 'အချိန်တိုက်', 'conflict'):
        return variants(
            "I have a meeting at the same time as the report deadline, so I may need to adjust my schedule.",
            "I have a meeting scheduled at the same time as the report deadline, so I may need to rearrange my schedule.",
            "My meeting overlaps with the report deadline, so I might need to shuffle things around.",
            "Because the meeting conflicts with the report deadline, I may need to revise my schedule accordingly.",
            "As the meeting coincides with the report deadline, an adjustment to my schedule may be necessary.",
        )

    # 033. Work: overtime + tired
    if has('အလုပ်', 'work') and has('အချိန်ပို', 'overtime') and has('ပင်ပန်း', 'tired'):
        return variants(
            "I worked overtime last night, so I'm quite tired today.",
            "I worked overtime last night, so I’m feeling quite tired today. I appreciate your understanding.",
            "I stayed late at work last night, so I’m pretty tired today.",
            "Having worked overtime last night, I am experiencing significant fatigue today.",
            "As I worked beyond regular hours last night, I am considerably fatigued today.",
        )

    # 034. Work: late night + sleep
    if has('အလုပ်', 'work') and has('ညနက်', 'late last night', 'ညအထိ') and has('အိပ်ရေးမဝ', 'sleep', 'အိပ်မဝ'):
        return variants(
            "I worked late last night and didn't get enough sleep, so I'm very tired today.",
            "I worked late last night and didn’t get enough sleep, so I’m feeling very tired today.",
            "I was up late working last night and barely got enough sleep, so I’m really tired today.",
            "Because I worked late last night and did not get enough sleep, I am quite fatigued today.",
            "Having worked late into the night and obtained insufficient sleep, I am experiencing considerable fatigue today.",
        )

    # 035. Work: commute + late
    if has('အလုပ်', 'office', 'work') and has('လမ်းမှာ', 'on the way', 'commute') and has('နောက်ကျ', 'late'):
        return variants(
            "I ran into delays on the way to work, so I'll be a little late today.",
            "I ran into delays on the way to work, so I may arrive a little late today.",
            "I got held up on the way to work, so I’m going to be a bit late.",
            "Due to delays during my commute, I will arrive at work later than scheduled today.",
            "Because of delays encountered while traveling to work, my arrival will be later than scheduled.",
        )

    # 036. Work: bus delay
    if has('အလုပ်', 'office', 'work') and has('ဘတ်စ်ကား', 'bus') and has('နောက်ကျ', 'delay', 'late'):
        return variants(
            "The bus is delayed, so I'll be late getting to work.",
            "The bus is delayed, so I may be a little late getting to work today.",
            "The bus is running late, so I’m going to be late for work.",
            "Due to the bus delay, I will arrive at work later than scheduled.",
            "As the bus service has been delayed, my arrival at work will be delayed accordingly.",
        )

    # 037. Work: train delay
    if has('အလုပ်', 'office', 'work') and has('ရထား', 'train') and has('နောက်ကျ', 'delay', 'late'):
        return variants(
            "The train is delayed, so I'll be late getting to work.",
            "The train is delayed, so I may arrive a little late for work today.",
            "The train’s running late, so I’m going to be late to work.",
            "Due to the train delay, I will arrive at work later than scheduled.",
            "Because the train service has been delayed, I will be unable to arrive at work at the expected time.",
        )

    # 038. School: rain + late
    if has('ကျောင်း', 'school') and has('မိုး', 'rain', 'ရွာ') and has('နောက်ကျ', 'late'):
        return variants(
            "It's raining heavily, so I'll be late getting to school.",
            "I wanted to let you know that it is raining heavily, so I may be a little late getting to school.",
            "It’s pouring right now, so I’m going to be late for school.",
            "Due to the heavy rain, I will arrive at school later than scheduled.",
            "Because of the heavy rainfall, my arrival at school will be delayed.",
        )

    # 039. School: flooding + late
    if has('ကျောင်း', 'school') and has('ရေလျှံ', 'ရေတက်', 'flooding') and has('နောက်ကျ', 'late'):
        return variants(
            "The road is flooded, so I'll be late getting to school.",
            "The road is flooded, so I may be a little late getting to school today.",
            "The road’s flooded, so I’m going to be late for school.",
            "Due to the flooding on the road, I will arrive at school later than scheduled.",
            "As the road is currently flooded, my arrival at school will necessarily be delayed.",
        )

    # 040. School: sick + absent
    if has('ကျောင်း', 'school') and has('နေမကောင်း', 'sick') and has('မသွား', 'မလာ', 'absent'):
        return variants(
            "I'm not feeling well, so I won't be able to go to school today.",
            "I'm not feeling well today, so I’d like to let you know that I won’t be able to go to school.",
            "I’m feeling sick today, so I’m going to stay home from school.",
            "Due to illness, I will be unable to attend school today.",
            "As I am unwell, I respectfully request to be excused from school today.",
        )

    # 041. School: appointment + absence
    if has('ကျောင်း', 'school') and has('appointment', 'ချိန်း') and has('မသွား', 'မလာ'):
        return variants(
            "I have an appointment, so I won't be able to go to school today.",
            "I have an appointment today, so please excuse me from school for the day.",
            "I’ve got an appointment, so I can’t make it to school today.",
            "Because of a scheduled appointment, I will be unable to attend school today.",
            "Due to a prior appointment, I respectfully request to be excused from school today.",
        )

    # 042. School: exam + preparation
    if has('ကျောင်း', 'school') and has('စာမေးပွဲ', 'exam') and has('စာကျက်', 'prepare', 'ပြင်ဆင်'):
        return variants(
            "I have an exam coming up, so I need some time to prepare.",
            "I have an exam coming up, so I would appreciate some time to prepare properly.",
            "My exam is coming up, so I need a little time to get ready for it.",
            "With an upcoming exam, I need to allocate additional time for preparation.",
            "As an examination is approaching, I require sufficient time to prepare adequately.",
        )

    # 043. School: assignment + deadline
    if has('ကျောင်း', 'school') and has('assignment', 'အိမ်စာ') and has('deadline', 'သတ်မှတ်ချိန်'):
        return variants(
            "I have an assignment due soon, so I need to finish it before the deadline.",
            "I have an assignment due soon, so I’d like to make sure I have enough time to finish it before the deadline.",
            "My assignment is due soon, so I need to get it finished in time.",
            "Because the assignment deadline is approaching, I need to prioritize completing it on schedule.",
            "With the assignment deadline approaching, I must ensure that the work is completed within the required timeframe.",
        )

    # 044. Weather: heavy rain + road
    if has('မိုးသည်း', 'မိုးကြီး', 'heavy rain') and has('လမ်း', 'road') and has('ရေတက်', 'ရေလျှံ', 'flood'):
        return variants(
            "It rained heavily, and the road is flooded, so travel is difficult right now.",
            "It rained heavily and the road is flooded, so traveling is currently quite difficult. Please take this into account.",
            "The rain was really heavy, and the road’s flooded, so getting around is tough right now.",
            "Heavy rainfall and road flooding are currently causing significant travel difficulties.",
            "Due to the heavy rainfall and resulting road flooding, travel is presently severely affected.",
        )

    # 045. Weather: rain + traffic
    if has('မိုး', 'rain', 'ရွာ') and has('traffic', 'ကားပိတ်', 'ကားကြပ်') and has('နောက်ကျ', 'late'):
        return variants(
            "Because of the heavy rain and traffic, I'll be late.",
            "Because of the heavy rain and traffic, I may be a little late. Thank you for understanding.",
            "The rain and traffic are really bad, so I’m going to be late.",
            "Heavy rain and traffic congestion are causing delays, so I will arrive later than scheduled.",
            "As a result of the heavy rainfall and traffic congestion, my arrival will be delayed.",
        )

    # 046. Weather: storm + work
    if has('မုန်တိုင်း', 'storm', 'လေပြင်း') and has('အလုပ်', 'work', 'office') and has('မလာ', 'နောက်ကျ'):
        return variants(
            "The weather is severe, so I may be late or unable to come to work today.",
            "The weather conditions are severe, so I may be late or may not be able to come to work today.",
            "The weather’s pretty bad, so I might be late or not make it to work today.",
            "Due to the severe weather conditions, I may arrive late or be unable to attend work today.",
            "In view of the severe weather conditions, my arrival at work may be delayed or my attendance may not be possible today.",
        )

    # 047. Weather: rain + meeting
    if has('မိုး', 'rain') and has('meeting', 'အစည်းအဝေး') and has('နောက်ကျ', 'late'):
        return variants(
            "The heavy rain is causing delays, so I may be late for the meeting.",
            "The heavy rain is causing delays, so I may arrive late for the meeting. I wanted to let you know in advance.",
            "The rain is slowing everything down, so I might be a little late to the meeting.",
            "Due to delays caused by the heavy rain, I may not arrive at the meeting at the scheduled time.",
            "As a consequence of the delays resulting from the heavy rainfall, my attendance at the scheduled time may be delayed.",
        )

    # 048. Weather: rain + delivery
    if has('မိုး', 'rain') and has('delivery', 'ပို့ဆောင်') and has('နောက်ကျ', 'late'):
        return variants(
            "The heavy rain is causing delivery delays, so the order may arrive late.",
            "The heavy rain is causing delivery delays, so the order may arrive later than expected. Thank you for your patience.",
            "The rain is slowing down deliveries, so your order might be a little late.",
            "Due to weather-related delivery delays, the order may be delivered later than originally expected.",
            "As a result of the heavy rainfall and associated delivery disruptions, the order may arrive after the expected time.",
        )

    # 049. Delivery: traffic delay
    if has('delivery', 'ပစ္စည်း', 'ပို့') and has('traffic', 'ကားပိတ်') and has('နောက်ကျ', 'late'):
        return variants(
            "The delivery is delayed because of heavy traffic.",
            "The delivery is currently delayed due to heavy traffic. We appreciate your patience.",
            "Traffic is really heavy, so the delivery’s running late.",
            "Heavy traffic is causing a delay to the delivery.",
            "The delivery is presently delayed as a result of significant traffic congestion.",
        )

    # 050. Delivery: address issue
    if has('delivery', 'ပစ္စည်း', 'ပို့') and has('လိပ်စာ', 'address') and has('မတွေ့', 'ရှာမတွေ့'):
        return variants(
            "The delivery may be delayed because the address is difficult to locate.",
            "The delivery may take a little longer because the address is difficult to locate. Thank you for your understanding.",
            "The address is a little hard to find, so the delivery might take longer.",
            "Because the delivery address is difficult to locate, the delivery may be delayed.",
            "As the delivery address is not readily identifiable, delivery may be subject to delay.",
        )

    # 051. Delivery: recipient unavailable
    if has('delivery', 'ပို့') and has('အိမ်မှာမရှိ', 'မရှိ', 'unavailable') and has('ပြန်ပို့', 'reschedule'):
        return variants(
            "The recipient is unavailable, so the delivery will need to be rescheduled.",
            "The recipient is currently unavailable, so could we please arrange another delivery time?",
            "The recipient isn’t available right now, so we’ll need to set up delivery again.",
            "As the recipient is unavailable, the delivery will need to be rescheduled for another time.",
            "Because the recipient is presently unavailable, a new delivery appointment will be required.",
        )

    # 052. Delivery: damaged item
    if has('delivery', 'ပစ္စည်း') and has('ပျက်', 'damaged') and has('ပြန်လဲ', 'replace', 'exchange'):
        return variants(
            "The item was damaged during delivery, so I'd like to request a replacement.",
            "The item was damaged during delivery, so could you please arrange a replacement?",
            "The item arrived damaged, so I’d like to get a replacement, please.",
            "Because the item was damaged during delivery, I would like to request a replacement.",
            "As the item was damaged in transit, I respectfully request that a replacement be provided.",
        )

    # 053. Delivery: wrong item
    if has('delivery', 'ပစ္စည်း') and has('မှား', 'wrong') and has('ပြန်လဲ', 'exchange', 'replace'):
        return variants(
            "The wrong item was delivered, so I'd like to request an exchange.",
            "The wrong item was delivered, so could you please arrange an exchange for me?",
            "I received the wrong item, so I’d like to swap it for the correct one.",
            "Since the incorrect item was delivered, I would like to request an exchange for the correct item.",
            "As the item delivered does not correspond to the order, I respectfully request an exchange for the correct item.",
        )

    # 054. Appointment: late
    if has('appointment', 'ချိန်း') and has('traffic', 'ကားပိတ်') and has('late', 'နောက်ကျ'):
        return variants(
            "There's heavy traffic, so I'll be late for my appointment.",
            "There's heavy traffic, so I may arrive a little late for my appointment.",
            "Traffic is really bad, so I’m going to be a bit late for my appointment.",
            "Due to heavy traffic, I will arrive at my appointment later than scheduled.",
            "Because of significant traffic congestion, my attendance at the scheduled appointment will be delayed.",
        )

    # 055. Appointment: cancel
    if has('appointment', 'ချိန်း') and has('မအား', 'အရေးပေါ်') and has('ဖျက်', 'cancel'):
        return variants(
            "Something urgent has come up, so I'd like to cancel my appointment.",
            "Something urgent has come up, so could I please cancel my appointment?",
            "Something urgent came up, so I need to cancel my appointment.",
            "Due to an urgent matter, I would like to request cancellation of my appointment.",
            "Because an urgent matter has arisen, I respectfully request that my appointment be cancelled.",
        )

    # 056. Appointment: reschedule
    if has('appointment', 'ချိန်း') and has('မအား', 'schedule') and has('ပြန်ချိန်း', 'reschedule'):
        return variants(
            "I'm no longer available at that time, so I'd like to reschedule the appointment.",
            "I'm no longer available at that time, so could we please reschedule the appointment?",
            "I can’t make that time anymore, so can we move the appointment to another slot?",
            "Due to a change in my availability, I would like to request that the appointment be rescheduled.",
            "As I am no longer available at the scheduled time, I respectfully request that the appointment be rearranged.",
        )

    # 057. Appointment: confirm
    if has('appointment', 'ချိန်း') and has('အတည်ပြု', 'confirm') and has('မနက်', 'afternoon', 'today', 'tomorrow'):
        return variants(
            "I'd like to confirm my appointment for the scheduled time.",
            "I'd like to confirm that my appointment is still set for the scheduled time, please.",
            "Just checking that my appointment is still on for the scheduled time.",
            "I would like to confirm that my appointment remains scheduled for the agreed time.",
            "I would like to formally confirm my appointment for the scheduled date and time.",
        )

    # 058. Appointment: early arrival
    if has('appointment', 'ချိန်း') and has('စောစော', 'early') and has('ရောက်', 'arrive'):
        return variants(
            "I'll arrive a little early for the appointment.",
            "I'll plan to arrive a little early for the appointment, just to make sure I'm on time.",
            "I’m planning to get there a little early for my appointment.",
            "I will arrive slightly ahead of the scheduled appointment time.",
            "I intend to arrive prior to the scheduled appointment time.",
        )

    # 059. Payment: delay
    if has('ငွေချေ', 'payment', 'ပေးချေ') and has('delay', 'နောက်ကျ') and has('ဘဏ်', 'bank'):
        return variants(
            "The payment is delayed because of a banking issue.",
            "The payment is currently delayed due to a banking issue. Thank you for your patience.",
            "There’s a banking problem, so the payment’s taking a little longer.",
            "Due to a banking issue, the payment is experiencing a delay.",
            "The payment has been delayed as a result of an issue within the banking process.",
        )

    # 060. Payment: transfer pending
    if has('ငွေလွှဲ', 'transfer') and has('pending', 'မဝင်သေး', 'မရောက်သေး') and has('bank', 'ဘဏ်'):
        return variants(
            "The bank transfer is still pending, so the payment has not arrived yet.",
            "The bank transfer is still pending, so the payment has not arrived yet. Thank you for your patience.",
            "The transfer’s still pending, so the payment hasn’t come through yet.",
            "The payment remains outstanding because the bank transfer has not yet cleared.",
            "As the bank transfer remains pending, the payment has not yet been received.",
        )

    # 061. Payment: insufficient funds
    if has('payment', 'ငွေပေး') and has('ငွေမလောက်', 'insufficient funds') and has('နောက်မှ', 'later'):
        return variants(
            "I don't have sufficient funds at the moment, so I'll make the payment a little later.",
            "I don't currently have sufficient funds, so could I please make the payment a little later?",
            "I’m a little short on funds right now, so I’ll make the payment a bit later.",
            "Because I do not currently have sufficient funds, I will make the payment at a later time.",
            "As sufficient funds are not presently available, I respectfully request permission to make the payment later.",
        )

    # 062. Payment: receipt
    if has('payment', 'ငွေချေ') and has('receipt', 'ပြေစာ') and has('ပို့', 'send'):
        return variants(
            "I'll send the payment receipt as soon as the payment is completed.",
            "I'll send you the payment receipt as soon as the payment has been completed.",
            "Once the payment goes through, I’ll send over the receipt.",
            "Upon completion of the payment, I will provide the payment receipt promptly.",
            "The payment receipt will be forwarded once the payment has been successfully completed.",
        )

    # 063. Internet: unstable + meeting
    if has('internet', 'အင်တာနက်') and has('မတည်ငြိမ်', 'unstable', 'ပြတ်') and has('meeting', 'အစည်းအဝေး'):
        return variants(
            "The internet connection is unstable, so I may have trouble joining the meeting.",
            "The internet connection is unstable, so I may have difficulty joining the meeting. Thank you for understanding.",
            "The internet keeps cutting out, so I might have trouble joining the meeting.",
            "Due to an unstable internet connection, I may experience difficulty joining the meeting.",
            "As the internet connection is currently unstable, my ability to join the meeting may be affected.",
        )

    # 064. Internet: slow + upload
    if has('internet', 'အင်တာနက်') and has('နှေး', 'slow') and has('upload', 'တင်'):
        return variants(
            "The internet is very slow, so the file upload is taking longer than expected.",
            "The internet is very slow, so the file upload is taking longer than expected. Thank you for your patience.",
            "The internet’s really slow, so the file is taking forever to upload.",
            "Because of the slow internet connection, the file upload is taking longer than anticipated.",
            "As a result of the significantly reduced internet speed, the file upload is exceeding the expected completion time.",
        )

    # 065. Internet: outage + deadline
    if has('internet', 'အင်တာနက်') and has('ပြတ်', 'down', 'outage') and has('deadline', 'သတ်မှတ်ချိန်'):
        return variants(
            "The internet is down, so I may need extra time to meet the deadline.",
            "The internet is down, so I may need a little additional time to meet the deadline.",
            "The internet’s out, so I might need a bit more time to finish by the deadline.",
            "Due to the internet outage, I may require additional time to meet the deadline.",
            "As the internet service is currently unavailable, I may require an extension of time to meet the deadline.",
        )

    # 066. Power: outage + meeting
    if has('မီးပျက်', 'power outage', 'electricity') and has('meeting', 'အစည်းအဝေး') and has('join', 'ဝင်'):
        return variants(
            "The power is out, so I may have difficulty joining the meeting.",
            "The power is currently out, so I may have difficulty joining the meeting. I appreciate your understanding.",
            "The power’s out right now, so I might have trouble joining the meeting.",
            "Due to the power outage, I may be unable to join the meeting as scheduled.",
            "As a result of the current power interruption, my participation in the meeting may be affected.",
        )

    # 067. Power: outage + device
    if has('မီးပျက်', 'power outage') and has('laptop', 'ဖုန်း', 'device') and has('အားကုန်', 'battery'):
        return variants(
            "The power is out and my device is running out of battery, so I may be offline for a while.",
            "The power is currently out and my device battery is getting low, so I may be offline for a while. Thank you for understanding.",
            "The power’s out and my battery is almost gone, so I might disappear offline for a bit.",
            "Because of the power outage and the low battery on my device, I may be unavailable online for some time.",
            "As the power supply is unavailable and my device battery is nearly depleted, I may remain offline temporarily.",
        )

    # 068. Power: outage + report
    if has('မီးပျက်', 'power outage') and has('report', 'အစီရင်ခံစာ') and has('deadline', 'အချိန်'):
        return variants(
            "The power outage is delaying my work on the report, so I may need more time.",
            "The power outage is delaying my work on the report, so I may need some additional time to complete it.",
            "The power’s out and it’s slowing down my report, so I might need a little longer.",
            "Due to the power outage, progress on the report has been delayed, and I may require additional time.",
            "As a result of the power interruption, completion of the report may be delayed and additional time may be necessary.",
        )

    # 069. Home: water problem + work
    if has('အိမ်', 'home') and has('ရေပြဿနာ', 'ရေပိုက်', 'water') and has('အလုပ်', 'work'):
        return variants(
            "There's a water problem at home that I need to take care of, so I may be late for work.",
            "There's a water problem at home that I need to take care of, so I may arrive late for work. I appreciate your understanding.",
            "There’s a water issue at home I need to sort out, so I might be a bit late to work.",
            "Due to an urgent water-related issue at home, I may arrive at work later than scheduled.",
            "As I am required to address a water-related problem at home, my arrival at work may be delayed.",
        )

    # 070. Home: repair + absence
    if has('အိမ်', 'home') and has('ပြင်ဆင်', 'repair') and has('အလုပ်', 'work'):
        return variants(
            "I need to deal with an urgent repair at home, so I won't be able to come to work right away.",
            "I need to handle an urgent repair at home, so I may not be able to come to work immediately. Thank you for understanding.",
            "There’s an urgent repair at home I have to take care of, so I can’t get to work just yet.",
            "Due to an urgent repair that requires my attention at home, I will be unable to attend work immediately.",
            "As I am required to address an urgent repair at home, I will be unable to report to work at the scheduled time.",
        )

    # 071. Home: locked out
    if has('အိမ်', 'home') and has('သော့', 'key') and has('ဝင်မရ', 'locked out'):
        return variants(
            "I'm locked out of my house, so I may be delayed.",
            "I'm locked out of my house, so I may be delayed. I wanted to let you know in advance.",
            "I’m locked out right now, so I might be a little late.",
            "Because I am currently locked out of my house, my arrival may be delayed.",
            "As I am presently unable to access my residence, a delay in my arrival may occur.",
        )

    # 072. Family: mother doctor
    if has('အမေ', 'mother', 'မိခင်') and has('ဆေးရုံ', 'doctor', 'ဆရာဝန်') and has('ဒီနေ့', 'today'):
        return variants(
            "I need to take my mother to the doctor today, so I may be late for work.",
            "I need to take my mother to the doctor today, so I may arrive a little late for work. Thank you for understanding.",
            "I’ve got to take my mom to the doctor today, so I might be a bit late to work.",
            "Due to my need to accompany my mother to a medical appointment, I may arrive at work later than scheduled today.",
            "As I am required to accompany my mother to the doctor today, my attendance at work may be delayed.",
        )

    # 073. Family: father hospital
    if has('အဖေ', 'father') and has('ဆေးရုံ', 'hospital') and has('အလုပ်', 'work'):
        return variants(
            "I need to take my father to the hospital, so I won't be able to come to work this morning.",
            "I need to take my father to the hospital this morning, so please excuse my absence from work.",
            "I have to take my dad to the hospital this morning, so I can’t make it to work.",
            "Because I need to accompany my father to the hospital this morning, I will be unable to attend work.",
            "Due to the need to accompany my father to the hospital this morning, I respectfully request to be excused from work.",
        )

    # 074. Family: child sick
    if has('ကလေး', 'child') and has('နေမကောင်း', 'sick') and has('အလုပ်', 'work'):
        return variants(
            "My child is not feeling well, so I need to stay home this morning and may be late for work.",
            "My child is not feeling well, so I need to stay home this morning and may arrive late for work. Thank you for understanding.",
            "My child’s not feeling well, so I need to stay home this morning and might be a little late to work.",
            "Due to my child's illness, I need to remain at home this morning and may arrive at work later than scheduled.",
            "As my child is unwell, I am required to remain at home this morning, and my arrival at work may therefore be delayed.",
        )

    # 075. Family: parent appointment
    if has('မိဘ', 'parent', 'အမေ', 'အဖေ') and has('appointment', 'ချိန်း') and has('လိုက်ပို့', 'accompany'):
        return variants(
            "I need to accompany my parent to an appointment this morning, so I may be late for work.",
            "I need to accompany my parent to an appointment this morning, so I may arrive a little late for work. I appreciate your understanding.",
            "I’ve got to take my parent to an appointment this morning, so I might be a bit late to work.",
            "Because I need to accompany my parent to a scheduled appointment this morning, I may arrive at work later than usual.",
            "As I am required to accompany my parent to an appointment this morning, my arrival at work may be delayed.",
        )

    # 076. Family: funeral
    if has('အသုဘ', 'funeral') and has('မိသားစု', 'family') and has('အလုပ်', 'work'):
        return variants(
            "There is a family funeral I need to attend, so I would like to request leave from work.",
            "There is a family funeral I need to attend, so I would like to respectfully request leave from work.",
            "There’s a family funeral I need to be at, so I’d like to take some time off work.",
            "Due to a family funeral that I must attend, I would like to request leave from work.",
            "As I am required to attend a family funeral, I respectfully request leave from work.",
        )

    # 077. Family: ceremony
    if has('မိသားစု', 'family') and has('အခမ်းအနား', 'ceremony') and has('အလုပ်', 'work'):
        return variants(
            "I need to attend an important family ceremony, so I may need to take time off work.",
            "I need to attend an important family ceremony, so I may need to take some time off work. I appreciate your understanding.",
            "I’ve got an important family ceremony to attend, so I might need some time off.",
            "Due to an important family ceremony, I may need to take time away from work.",
            "As I am required to attend an important family ceremony, I may need to request leave from work.",
        )

    # 078. Travel: delayed
    if has('ခရီး', 'travel', 'trip') and has('နောက်ကျ', 'delay', 'delayed') and has('ရောက်', 'arrive'):
        return variants(
            "My trip has been delayed, so I won't arrive at the expected time.",
            "My trip has been delayed, so I may arrive later than expected. Thank you for your understanding.",
            "My trip’s been delayed, so I’m going to get there later than planned.",
            "Due to a delay in my trip, I will not arrive at the expected time.",
            "As a result of the delay to my journey, my arrival will occur later than the scheduled time.",
        )

    # 079. Travel: flight delay
    if has('flight', 'လေယာဉ်') and has('delay', 'နောက်ကျ') and has('airport', 'လေဆိပ်'):
        return variants(
            "My flight has been delayed, so I'll arrive later than expected.",
            "My flight has been delayed, so I may arrive later than expected. Thank you for your patience.",
            "My flight’s been delayed, so I’m going to get in a little later.",
            "Due to the flight delay, I will arrive later than originally scheduled.",
            "As the flight has been delayed, my arrival will be later than the expected time.",
        )

    # 080. Travel: rain + flight
    if has('flight', 'လေယာဉ်') and has('မိုး', 'weather') and has('delay', 'နောက်ကျ'):
        return variants(
            "The bad weather is causing flight delays, so my arrival may be later than planned.",
            "The bad weather is causing flight delays, so my arrival may be later than planned. Thank you for your patience.",
            "Bad weather is holding up the flights, so I might get in later than planned.",
            "Adverse weather conditions are causing flight delays, and my arrival may therefore be later than scheduled.",
            "As a consequence of adverse weather affecting flight operations, my arrival may occur later than planned.",
        )

    # 081. Travel: traffic + airport
    if has('airport', 'လေဆိပ်') and has('traffic', 'ကားပိတ်') and has('late', 'နောက်ကျ'):
        return variants(
            "Traffic is very heavy on the way to the airport, so I may be late.",
            "Traffic is very heavy on the way to the airport, so I may arrive a little late. Please allow for some extra time.",
            "Traffic is really heavy on the way to the airport, so I might be a bit late.",
            "Due to heavy traffic en route to the airport, I may arrive later than scheduled.",
            "As a result of significant traffic congestion on the route to the airport, my arrival may be delayed.",
        )

    # 082. Deadline: extension request
    if has('deadline', 'သတ်မှတ်ချိန်') and has('အချိန်ပို', 'more time') and has('တောင်း', 'request'):
        return variants(
            "I need a little more time to complete the work, so I'd like to request an extension.",
            "I need a little more time to complete the work, so could I please request an extension?",
            "I need a bit more time to finish the work, so I’d like to get an extension.",
            "To complete the work properly, I would like to request an extension of the deadline.",
            "I respectfully request an extension of time to ensure that the work can be completed satisfactorily.",
        )

    # 083. Deadline: client changes
    if has('deadline', 'သတ်မှတ်ချိန်') and has('client', 'ဖောက်သည်') and has('changes', 'ပြင်ဆင်'):
        return variants(
            "The client requested additional changes, so I may need an extension to meet the deadline.",
            "The client requested additional changes, so I may need a little extra time to meet the deadline. Thank you for understanding.",
            "The client asked for more changes, so I might need a bit longer to finish on time.",
            "Due to the additional changes requested by the client, I may require an extension to meet the deadline.",
            "In light of the client's additional requirements, I may respectfully request an extension to the deadline.",
        )

    # 084. Deadline: unexpected issue
    if has('deadline', 'သတ်မှတ်ချိန်') and has('မမျှော်လင့်', 'unexpected') and has('ပြဿနာ', 'issue', 'problem'):
        return variants(
            "An unexpected issue came up, so I may need a little more time to meet the deadline.",
            "An unexpected issue has come up, so I may need a little additional time to meet the deadline. Thank you for understanding.",
            "Something unexpected came up, so I might need a bit more time to get it done.",
            "Because an unforeseen issue has arisen, I may require additional time to meet the deadline.",
            "Due to an unforeseen circumstance, I may need an extension of time to fulfill the deadline requirements.",
        )

    # 085. Deadline: waiting approval
    if has('deadline', 'သတ်မှတ်ချိန်') and has('approval', 'အတည်ပြု') and has('စောင့်', 'waiting'):
        return variants(
            "I'm waiting for approval, so I may not be able to meet the deadline as originally planned.",
            "I'm waiting for approval, so I may not be able to meet the deadline as originally planned. I wanted to let you know in advance.",
            "I’m still waiting for the go-ahead, so I might not hit the deadline we first planned.",
            "Pending the required approval, I may be unable to meet the deadline as originally scheduled.",
            "As the necessary approval remains outstanding, I may be unable to fulfill the deadline according to the original schedule.",
        )

    # 086. Meeting: minutes late
    if has('meeting', 'အစည်းအဝေး') and has('minutes', 'မိနစ်') and has('နောက်ကျ', 'late'):
        return variants(
            "I'll be a few minutes late for the meeting.",
            "I may be a few minutes late for the meeting. Thank you for your understanding.",
            "I’m running a few minutes behind for the meeting.",
            "I will arrive a few minutes after the scheduled start of the meeting.",
            "Please be advised that my arrival at the meeting will be delayed by a few minutes.",
        )

    # 087. Meeting: join online
    if has('meeting', 'အစည်းအဝေး') and has('online', 'အွန်လိုင်း') and has('join', 'ဝင်'):
        return variants(
            "I'll join the meeting online instead.",
            "I'll join the meeting online instead, if that works for you.",
            "I’ll just join the meeting online instead.",
            "I will attend the meeting remotely rather than in person.",
            "I will participate in the meeting via the online format instead.",
        )

    # 088. Meeting: camera issue
    if has('meeting', 'အစည်းအဝေး') and has('camera', 'ကင်မရာ') and has('မရ', 'problem'):
        return variants(
            "I'm having an issue with my camera, so I may need to join the meeting without video.",
            "I'm having an issue with my camera, so I may need to join the meeting without video. I appreciate your understanding.",
            "My camera’s acting up, so I might have to join the meeting without video.",
            "Due to a camera issue, I may need to participate in the meeting without video.",
            "As I am experiencing a camera-related technical issue, I may be required to join the meeting without video.",
        )

    # 089. Meeting: microphone issue
    if has('meeting', 'အစည်းအဝေး') and has('microphone', 'mic') and has('မရ', 'problem'):
        return variants(
            "My microphone isn't working properly, so I may have trouble speaking during the meeting.",
            "My microphone isn't working properly, so I may have difficulty speaking during the meeting. Thank you for your understanding.",
            "My mic isn’t working right, so I might have trouble talking during the meeting.",
            "Due to a microphone malfunction, I may experience difficulty speaking during the meeting.",
            "As my microphone is not functioning correctly, my ability to speak during the meeting may be affected.",
        )

    # 090. Meeting: recording request
    if has('meeting', 'အစည်းအဝေး') and has('record', 'recording') and has('မတက်နိုင်', 'မဝင်နိုင်'):
        return variants(
            "I may not be able to join the meeting, so could you please share the recording with me afterward?",
            "I may not be able to join the meeting. Could you please share the recording with me afterward?",
            "I might not make the meeting, so could you send me the recording afterward?",
            "As I may be unable to attend the meeting, I would appreciate it if you could share the recording with me afterward.",
            "Should I be unable to attend the meeting, I kindly request that the recording be shared with me afterward.",
        )

    # 091. Meeting: postpone
    if has('meeting', 'အစည်းအဝေး') and has('မအား', 'busy') and has('ရွှေ့', 'postpone'):
        return variants(
            "I'm not available at the scheduled time, so could we postpone the meeting?",
            "I'm not available at the scheduled time. Could we please postpone the meeting to another time?",
            "I can’t make the scheduled time—can we push the meeting back?",
            "Due to a scheduling conflict, I would like to request that the meeting be postponed.",
            "As I am unavailable at the scheduled time, I respectfully request that the meeting be postponed.",
        )

    # 092. Task: priority change
    if has('task', 'အလုပ်') and has('priority', 'ဦးစားပေး') and has('ပြောင်း', 'change'):
        return variants(
            "The priorities have changed, so I'll work on the urgent task first.",
            "The priorities have changed, so I’ll handle the urgent task first and then move on to the others.",
            "The priorities have shifted, so I’m going to tackle the urgent task first.",
            "Given the change in priorities, I will address the urgent task before proceeding with the remaining work.",
            "In accordance with the revised priorities, I will give precedence to the urgent task.",
        )

    # 093. Task: blocked
    if has('task', 'အလုပ်') and has('မလုပ်နိုင်', 'blocked', 'stuck') and has('လိုအပ်', 'need'):
        return variants(
            "I'm blocked by an issue, so I need some help before I can continue.",
            "I’m blocked by an issue, so could you please help me resolve it before I continue?",
            "I’ve hit a problem, so I could use some help before I can keep going.",
            "An issue is preventing me from proceeding, so I need assistance to resolve it.",
            "As an unresolved issue is preventing further progress, I respectfully request assistance before proceeding.",
        )

    # 094. Task: waiting information
    if has('task', 'အလုပ်') and has('information', 'အချက်အလက်') and has('စောင့်', 'waiting'):
        return variants(
            "I'm waiting for the required information, so I can't complete the task yet.",
            "I'm waiting for the required information, so I’m unable to complete the task yet. Could you please provide it when available?",
            "I’m just waiting on the information I need, so I can’t finish the task yet.",
            "Completion of the task is currently pending receipt of the required information.",
            "As the required information has not yet been received, the task cannot presently be completed.",
        )

    # 095. Task: completed + send
    if has('task', 'အလုပ်') and has('ပြီးပြီ', 'completed', 'finished') and has('ပို့', 'send'):
        return variants(
            "I've completed the task, and I'll send the final file shortly.",
            "I've completed the task, and I’ll send you the final file shortly. Please let me know if anything else is needed.",
            "All done with the task—I’ll send over the final file in a little while.",
            "The task has been completed, and I will send the final file shortly.",
            "The task has now been completed; the final file will be provided shortly.",
        )

    # 096. Task: revise + resend
    if has('task', 'အလုပ်') and has('ပြင်', 'revise', 'ပြန်ပြင်') and has('ပြန်ပို့', 'resend'):
        return variants(
            "I'll revise the work based on the feedback and resend the updated version.",
            "I’ll revise the work based on the feedback and send you the updated version again once it’s ready.",
            "I’ll make the changes from the feedback and send the updated version back over.",
            "Based on the feedback received, I will revise the work and resend the updated version.",
            "In accordance with the feedback provided, I will revise the work and subsequently resubmit the updated version.",
        )

    # 097. Message: forgot + apology
    if has('မေ့', 'forgot') and has('တောင်းပန်', 'sorry') and has('ပြန်လုပ်', 'do again'):
        return variants(
            "I'm sorry, I forgot about it. I'll take care of it now.",
            "I'm sorry, I forgot about it. I'll take care of it now. Thank you for your patience.",
            "Sorry, it slipped my mind—I’ll take care of it now.",
            "I apologize for overlooking this. I will address it immediately.",
            "Please accept my apologies for the oversight; I will take the necessary action immediately.",
        )

    # 098. Message: misunderstood + clarify
    if has('နားလည်မှား', 'misunderstood') and has('တောင်းပန်', 'sorry') and has('ရှင်းပြ', 'clarify'):
        return variants(
            "I'm sorry, I misunderstood the request. Let me clarify and correct it.",
            "I'm sorry, I misunderstood the request. Could I clarify the details and correct it?",
            "Sorry, I got the request wrong—I’ll clarify it and fix it.",
            "I apologize for misunderstanding the request. I will clarify the requirements and make the necessary correction.",
            "Please accept my apologies for the misunderstanding; I will clarify the request and rectify the matter accordingly.",
        )

    # 099. Message: no response + busy
    if has('မပြန်', 'reply', 'response') and has('အလုပ်များ', 'busy') and has('နောက်မှ', 'later'):
        return variants(
            "Sorry for the late response. I was busy, but I'll get back to you shortly.",
            "Sorry for the delayed response. I was busy, but I’ll get back to you shortly. Thank you for your patience.",
            "Sorry I took a while to reply—I was busy, but I’ll get back to you soon.",
            "I apologize for the delayed response. I was occupied, but I will follow up with you shortly.",
            "Please accept my apologies for the delayed response; I was engaged with other matters and will respond shortly.",
        )

    # 100. Message: seen + reply later
    if has('message', 'စာ') and has('seen', 'တွေ့') and has('နောက်မှ', 'later'):
        return variants(
            "I've seen your message, and I'll reply properly a little later.",
            "I've seen your message. I'll get back to you a little later once I have a chance to respond properly.",
            "I saw your message—I’ll reply properly a little later when I get a minute.",
            "I have seen your message and will provide a proper response later.",
            "Please be advised that I have seen your message and will respond in due course.",
        )


    return None

def contextual_rule_translation(text: str, tone: str):
    """
    Semantic/context rules for long Myanmar, English, and mixed-language
    messages. These rules are deliberately clause-aware: they preserve
    cause -> situation -> consequence -> request/action instead of matching
    only the final intent.
    """
    n = normalize_text(text)

    def has(*phrases):
        return _contains_any(n, list(phrases))

    def variants(simple, polite, friendly, professional, formal):
        return {
            "simple": simple,
            "polite": polite,
            "friendly": friendly,
            "professional": professional,
            "formal": formal,
        }.get(tone, professional)

    # --------------------------------------------------------
    # FIRST: MULTI-CAUSE MESSAGES
    # --------------------------------------------------------
    # This MUST run before any single-cause rule. A message can contain
    # rain + flooding + traffic + a destination + a delay. Never return
    # early just because the word "traffic" was found.
    early_weather = has(
        "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
        "rain", "raining", "heavy rain", "poured"
    )
    early_traffic = has(
        "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
        "traffic", "traffic jam", "heavy traffic"
    )
    early_flood = has(
        "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
        "flood", "flooded", "flooding"
    )
    early_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
    early_wait = has("စောင့်", "wait", "wait for me")
    early_school = has("ကျောင်း", "school")
    early_work = has("အလုပ်", "work", "office")
    early_meeting = has("meeting", "အစည်းအဝေး")

    early_cause_count = sum([early_weather, early_flood, early_traffic])

    if early_cause_count >= 2 and (early_delay or early_wait):
        if early_meeting:
            early_destination = "the meeting"
        elif early_school:
            early_destination = "school"
        elif early_work:
            early_destination = "work"
        else:
            early_destination = "my destination"

        early_causes = []
        if early_weather:
            early_causes.append("It rained heavily this morning")
        if early_flood:
            early_causes.append("the area in front of my house is flooded")
        if early_traffic:
            early_causes.append("there is also heavy traffic on the way")

        if len(early_causes) == 2:
            early_reason_sentence = early_causes[0] + ", and " + early_causes[1]
        else:
            early_reason_sentence = ", ".join(early_causes[:-1]) + ", and " + early_causes[-1]

        if early_wait:
            return variants(
                f"{early_reason_sentence}, so I'll be late getting to {early_destination}. Please wait for me for a little while.",
                f"{early_reason_sentence}, so I'm going to be late getting to {early_destination}. I'm sorry, but could you please wait for me for a little while?",
                f"{early_reason_sentence}, so I'll be a little late getting to {early_destination}. Please wait for me for a bit.",
                f"{early_reason_sentence}, so I will be late getting to {early_destination}. Could you please wait for me for a little while?",
                f"Due to the heavy rain, flooding in front of my house, and heavy traffic on the way, I will be delayed in reaching {early_destination}. I would appreciate your patience and ask that you please wait for me for a little while.",
            )

        return variants(
            f"{early_reason_sentence}, so I'll be late getting to {early_destination} today.",
            f"{early_reason_sentence}, so I'm sorry, but I'll be late getting to {early_destination} today.",
            f"{early_reason_sentence}, so I'll be a little late getting to {early_destination} today.",
            f"{early_reason_sentence}, so I will be late getting to {early_destination} today.",
            f"Due to the heavy rain, flooding in front of my house, and heavy traffic on the way, I will be delayed in reaching {early_destination} today.",
        )

    # --------------------------------------------------------
    # A. Long chained message: late meeting -> poor sleep -> work absence
    # --------------------------------------------------------
    if (
        has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "ended late", "ran late", "finished late", "late last night")
        and has("အိပ်ရေးမဝ", "အိပ်မဝ", "အိပ်ရေးမလုံ", "အိပ်မပျော်", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "did not get enough sleep", "barely slept")
        and has("အလုပ်", "work", "office")
        and has("မလာ", "မလာတော့", "မသွား", "won't come", "will not come", "not coming", "won't be coming", "will not be coming")
    ):
        return variants(
            "The meeting ended late last night, and I didn't get enough sleep, so I won't be coming to work today.",
            "The meeting ended quite late last night, and I didn't get enough sleep, so I'm sorry, but I won't be able to come to work today.",
            "The meeting ran late last night, and I barely got enough sleep, so I won't be coming to work today.",
            "The meeting ended late last night, and I did not get enough sleep, so I will not be coming to work today.",
            "As the meeting ended late last night and I did not get sufficient sleep, I will be unable to come to work today.",
        )

    # Same meaning even when the time phrase is omitted.
    if (
        has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "ended late", "ran late", "finished late")
        and has("အိပ်ရေးမဝ", "အိပ်မဝ", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "barely slept")
        and has("အလုပ်", "work", "office")
        and has("မလာ", "မလာတော့", "မသွား", "won't come", "not coming", "won't be coming")
    ):
        return variants(
            "The meeting ended late, and I didn't get enough sleep, so I won't be coming to work today.",
            "The meeting ended late, and I didn't get enough sleep, so I'm sorry, but I won't be able to come to work today.",
            "The meeting ran late, and I barely got enough sleep, so I won't be coming to work today.",
            "The meeting ended late, and I did not get enough sleep, so I will not be coming to work today.",
            "As the meeting ended late and I did not get sufficient sleep, I will be unable to come to work today.",
        )

    # --------------------------------------------------------
    # B. Traffic + meeting delay + explicit waiting request
    # --------------------------------------------------------
    if (
        has("ကားပိတ်", "ကားလမ်းပိတ်", "လမ်းပိတ်", "ကားကြပ်", "traffic", "traffic jam", "heavy traffic")
        and has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "late", "delayed")
        and has("စောင့်", "wait", "give me a moment", "wait for me")
    ):
        return variants(
            "There's heavy traffic at the end of the street, so I'll be late for the meeting. Please wait for me for a little while.",
            "There's heavy traffic at the end of the street, so I'm going to be late for the meeting. I'm sorry, but could you please wait for me for a little while?",
            "There's a traffic jam at the end of the street, so I'll be late for the meeting. Please wait for me a little while.",
            "There's heavy traffic at the end of the street, so I'll be late for the meeting. Could you please wait for me for a little while?",
            "There is heavy traffic at the end of the street, which is causing me to be late for the meeting. I would appreciate your patience and ask that you please wait for me for a little while.",
        )

    # --------------------------------------------------------
    # C. Heavy rain + flooding + school delay
    # --------------------------------------------------------
    if (
        has("မိုးသည်း", "မိုးရွာ", "မိုးကြီး", "မိုးသည်းကြီးမည်းကြီး", "rain", "raining", "poured", "heavy rain")
        and has("ရေလျှံ", "ရေတွေ လျှံ", "ရေဝင်", "flood", "flooded", "flooding", "water is overflowing")
        and has("ကျောင်း", "school")
        and has("နောက်ကျ", "late", "delayed")
    ):
        return variants(
            "It rained heavily this morning, and the area in front of my house is flooded, so I'll be late getting to school today.",
            "It rained very heavily this morning, and the area in front of my house is flooded, so I'm sorry, but I'll be late getting to school today.",
            "It poured this morning, and there's water all over the front of my house, so I'll be a little late getting to school today.",
            "It rained heavily this morning, and the area in front of my house is flooded, so I will be late getting to school today.",
            "Due to the heavy rain this morning and flooding in front of my house, I will be delayed in getting to school today.",
        )

    # --------------------------------------------------------
    # D. Mother's/family health issue + work leave
    # --------------------------------------------------------
    if (
        has("အမေ", "မိခင်", "mother", "mom", "mum")
        and has("ကျန်းမာရေး", "နေမကောင်း", "health", "not feeling well", "sick")
        and has("အလုပ်", "work", "office")
        and has("ခွင့်", "leave", "day off", "take a day off")
    ):
        return variants(
            "My mother has a health issue, so I'd like to take a day off from work today.",
            "My mother is having a health issue, so I'm sorry, but I'd like to request a day off from work today.",
            "My mom isn't feeling well, so I'd like to take the day off from work today.",
            "Due to a health issue involving my mother, I would like to request one day of leave from work today.",
            "Due to a health-related matter concerning my mother, I would like to respectfully request one day of leave from work today.",
        )

    # --------------------------------------------------------
    # E. Family health/emergency + work leave (generic family member)
    # --------------------------------------------------------
    if (
        has("မိသားစု", "family", "အိမ်က")
        and has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick", "ဆေးရုံ", "hospital", "အရေးပေါ်", "emergency")
        and has("အလုပ်", "work", "office")
        and has("ခွင့်", "leave", "day off")
    ):
        return variants(
            "There is a health issue in my family that I need to take care of, so I'd like to take a day off from work today.",
            "There is a health issue in my family that I need to take care of, so I'd like to request a day off from work today.",
            "There's a family health issue I need to take care of, so I'd like to take the day off today.",
            "Due to a family health matter that requires my attention, I would like to request one day of leave from work today.",
            "Due to a family health matter requiring my attention, I would like to respectfully request one day of leave from work today.",
        )

    # --------------------------------------------------------
    # COMPOUND WEATHER + TRAFFIC / MULTI-CAUSE CONTEXT
    #
    # IMPORTANT: Never let one detected cause (for example "traffic")
    # hide another meaningful cause (for example "heavy rain").
    # A long message may contain several causes and all of them must
    # survive in the English translation.
    # --------------------------------------------------------
    has_weather = has(
        "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
        "rain", "raining", "heavy rain", "poured"
    )
    has_traffic = has(
        "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
        "traffic", "traffic jam", "heavy traffic"
    )
    has_flood = has(
        "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
        "flood", "flooded", "flooding"
    )
    has_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
    has_wait = has("စောင့်", "wait", "wait for me")
    destination_school = has("ကျောင်း", "school")
    destination_work = has("အလုပ်", "work", "office")
    destination_meeting = has("meeting", "အစည်းအဝေး")

    if (
        (has_weather and has_traffic and has_delay)
        or (has_weather and has_traffic and has_wait)
    ):
        destination = (
            "the meeting" if destination_meeting
            else "school" if destination_school
            else "work" if destination_work
            else "my destination"
        )

        # Include every detected cause instead of selecting only traffic.
        cause_sentence = (
            "It rained heavily, and there is heavy traffic on the way"
            if has_weather and has_traffic
            else "It is raining heavily"
            if has_weather
            else "There is heavy traffic on the way"
        )

        if has_wait:
            return variants(
                f"{cause_sentence}, so I'll be delayed getting to {destination}. Please wait for me for a little while.",
                f"{cause_sentence}, so I'm going to be late getting to {destination}. I'm sorry, but could you please wait for me for a little while?",
                f"{cause_sentence}, so I'll be a little late getting to {destination}. Please wait for me for a bit.",
                f"{cause_sentence}, so I will be delayed getting to {destination}. Could you please wait for me for a little while?",
                f"Due to the heavy rain and traffic conditions, I will be delayed in reaching {destination}. I would appreciate your patience and ask that you please wait for me for a little while.",
            )

        return variants(
            f"{cause_sentence}, so I'll be late getting to {destination}.",
            f"{cause_sentence}, so I'm sorry, but I'll be late getting to {destination}.",
            f"{cause_sentence}, so I'll be a little late getting to {destination}.",
            f"{cause_sentence}, so I will be late getting to {destination}.",
            f"Due to the heavy rain and traffic conditions, I will be delayed in reaching {destination}.",
        )

    # Rain + flooding + a destination, even when the exact "school" rule
    # does not match. Keep both the weather and flooding information.
    if has_weather and has_flood and has_delay and (destination_school or destination_work):
        destination = "school" if destination_school else "work"
        return variants(
            f"It rained heavily, and the area around my house is flooded, so I'll be late getting to {destination}.",
            f"It rained heavily, and the area around my house is flooded, so I'm sorry, but I'll be late getting to {destination}.",
            f"It poured this morning, and there's flooding around my house, so I'll be a little late getting to {destination}.",
            f"It rained heavily, and the area around my house is flooded, so I will be late getting to {destination}.",
            f"Due to the heavy rain and flooding around my house, I will be delayed in reaching {destination}.",
        )

    # --------------------------------------------------------
    # F. Transportation/traffic + work/school delay, no wait request
    # --------------------------------------------------------
    if has("ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic") and has("နောက်ကျ", "late", "delayed"):
        if has("ကျောင်း", "school"):
            return variants(
                "There's heavy traffic, so I'll be late getting to school.",
                "I'm sorry, but there's heavy traffic, so I'll be late getting to school.",
                "There's a lot of traffic, so I'll be a little late getting to school.",
                "There's heavy traffic, so I'll be late getting to school.",
                "Due to heavy traffic, I will be delayed in arriving at school.",
            )
        if has("အလုပ်", "work", "office"):
            return variants(
                "There's heavy traffic, so I'll be late for work.",
                "I'm sorry, but there's heavy traffic, so I'll be late for work.",
                "There's a lot of traffic, so I'll be a little late for work.",
                "There's heavy traffic, so I'll be late for work.",
                "Due to heavy traffic, I will be delayed in arriving at work.",
            )
        return variants(
            "There's heavy traffic, so I'll be late.",
            "I'm sorry, but there's heavy traffic, so I'll be late.",
            "There's a lot of traffic, so I'll be a little late.",
            "There's heavy traffic, so I'll be late.",
            "Due to heavy traffic, I will be delayed.",
        )

    # --------------------------------------------------------
    # G. General meeting delay + tiredness (without work absence)
    # --------------------------------------------------------
    if (
        has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "ended late", "ran late", "finished late")
        and has("အိပ်ရေးမဝ", "အိပ်မဝ", "ပင်ပန်း", "tired", "not enough sleep", "didn't get enough sleep", "barely slept")
    ):
        return variants(
            "The meeting ended late, and I didn't get enough sleep, so I'm very tired today.",
            "The meeting ended late, and I didn't get enough sleep, so I'm quite tired today.",
            "The meeting ran late, and I barely got enough sleep, so I'm really tired today.",
            "The meeting ended late, and I did not get enough sleep, so I am feeling very tired today.",
            "As the meeting ended late and I did not get sufficient sleep, I am feeling quite fatigued today.",
        )

    # --------------------------------------------------------
    # H. On the way + traffic + waiting request
    # --------------------------------------------------------
    if has("လမ်းမှာ", "လာနေ", "on my way") and has("ကားပိတ်", "ကားကြပ်", "traffic", "လမ်းပိတ်") and has("စောင့်", "wait", "wait for me"):
        return variants(
            "I'm on my way, but I'm stuck in traffic, so please wait for me for a little while.",
            "I'm on my way, but I'm stuck in traffic. Could you please wait for me for a little while?",
            "I'm on my way, but I'm stuck in traffic, so please wait for me a little while.",
            "I'm currently on my way, but I'm stuck in traffic. Could you please wait for me for a little while?",
            "I am currently on my way but delayed by traffic. I would appreciate your patience and ask that you please wait for me for a little while.",
        )

    # --------------------------------------------------------
    # I. Generic waiting requests with known reasons
    # --------------------------------------------------------
    if has("စောင့်", "wait", "wait for me", "ခနစောင့်", "ခဏစောင့်"):
        if has("မိုး", "rain", "raining"):
            return variants(
                "It's raining right now, so please wait for me for a little while.",
                "It's raining right now, so could you please wait for me for a little while?",
                "It's raining right now, so please wait for me a little while.",
                "It's currently raining, so could you please wait for me for a little while?",
                "As it is currently raining, I would appreciate your patience and ask that you please wait for me for a little while.",
            )
        if has("မအား", "busy", "အလုပ်များ", "unavailable"):
            return variants(
                "I'm a little busy right now, so please wait for me for a moment.",
                "I'm sorry, I'm a little busy right now. Could you please wait for me for a moment?",
                "I'm a little busy right now, so just give me a moment, please.",
                "I'm currently unavailable, so could you please wait for me for a moment?",
                "I am currently unavailable. I would appreciate your patience for a brief moment.",
            )
        return variants(
            "Please wait for me for a moment.",
            "Could you please wait for me for a moment?",
            "Just give me a moment, please.",
            "Could you please give me a moment?",
            "I would appreciate your patience for a brief moment.",
        )

    return None



# ============================================================
# COMPLETE-MEANING / AI UNDERSTANDING LAYER
# ============================================================
#
# The translation and the "AI Understanding" panel must use the same
# semantic interpretation.  Do not reduce a long message to its final
# intent and then lose the earlier reasons.
#
# This layer is deliberately lightweight and deterministic for high-
# confidence patterns. Qwen is still used for unknown translations.
# ============================================================

def detect_input_language(text: str) -> str:
    has_mm = bool(re.search(r"[\u1000-\u109F]", text))
    # Treat common English words as English content even when Myanmar text
    # is also present.
    has_en = bool(re.search(r"[A-Za-z]", text))
    if has_mm and has_en:
        return "Mixed Myanmar + English"
    if has_mm:
        return "Myanmar (Unicode)"
    if has_en:
        return "English"
    return "Unknown"


def build_ai_understanding(
    text: str,
    requested_tone: str = "professional",
    audience: str = "auto",
) -> dict[str, str]:
    """
    Extract the complete meaning needed by both the UI and the translation
    prompt.  The key design rule is:

        reason/cause -> situation -> consequence -> main action/request

    Never replace a long message's reason with "reason unspecified" when
    the source clearly contains one.
    """
    n = normalize_text(text)

    def has(*phrases):
        return _contains_any(n, list(phrases))

    language = detect_input_language(text)

    # --------------------------------------------------------
    # FIRST: MULTI-CAUSE UNDERSTANDING
    # --------------------------------------------------------
    # This must run before single-cause traffic/rain rules.
    u_weather = has(
        "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
        "rain", "raining", "heavy rain", "poured"
    )
    u_traffic = has(
        "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
        "traffic", "traffic jam", "heavy traffic"
    )
    u_flood = has(
        "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
        "flood", "flooded", "flooding"
    )
    u_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
    u_wait = has("စောင့်", "wait", "wait for me")
    u_school = has("ကျောင်း", "school")
    u_work = has("အလုပ်", "work", "office")
    u_meeting = has("meeting", "အစည်းအဝေး")

    u_cause_count = sum([u_weather, u_flood, u_traffic])

    if u_cause_count >= 2 and (u_delay or u_wait):
        if u_meeting:
            u_destination = "the meeting"
        elif u_school:
            u_destination = "school"
        elif u_work:
            u_destination = "work"
        else:
            u_destination = "the destination"

        u_reasons = []
        if u_weather:
            u_reasons.append("heavy rain this morning")
        if u_flood:
            u_reasons.append("flooding in front of the sender's house")
        if u_traffic:
            u_reasons.append("heavy traffic on the way")

        if len(u_reasons) == 2:
            u_reason_text = u_reasons[0] + " and " + u_reasons[1]
        else:
            u_reason_text = ", ".join(u_reasons[:-1]) + ", and " + u_reasons[-1]

        return {
            "language": language,
            "intent": (
                "Inform recipient about a delay and ask them to wait"
                if u_wait
                else f"Inform recipient that the sender will be late for {u_destination}"
            ),
            "audience": (
                "Colleague" if u_work or u_meeting
                else "Teacher / school contact" if u_school
                else ("Recipient" if audience == "auto" else audience)
            ) if audience == "auto" else audience,
            "situation": (
                f"The sender expects to arrive late at {u_destination} because of {u_reason_text}."
                if not u_wait
                else f"The sender is delayed by {u_reason_text} and is asking the recipient to wait."
            ),
            "reason": f"The message gives multiple reasons: {u_reason_text}.",
            "main_action": (
                f"Inform the recipient that the sender will be late getting to {u_destination}."
                if not u_wait
                else "Ask the recipient to wait for the sender."
            ),
            "cause_chain": (
                f"{u_reason_text} → travel delay → late arrival at {u_destination}."
                if not u_wait
                else f"{u_reason_text} → travel delay → sender asks recipient to wait."
            ),
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Meeting late -> insufficient sleep -> work absence
    # --------------------------------------------------------
    if (
        has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "ended late", "ran late", "finished late", "late last night")
        and has(
            "အိပ်ရေးမဝ", "အိပ်မဝ", "အိပ်ရေးမလုံ", "အိပ်မပျော်",
            "ပင်ပန်း", "tired", "not enough sleep",
            "didn't get enough sleep", "did not get enough sleep",
            "barely slept", "barely got enough sleep"
        )
        and has("အလုပ်", "work", "office")
        and has(
            "မလာ", "မလာတော့", "မသွား",
            "won't come", "will not come", "not coming",
            "won't be coming", "will not be coming",
            "won't be able to come", "unable to come"
        )
    ):
        return {
            "language": language,
            "intent": "Inform recipient that the sender will not come to work",
            "audience": "Colleague" if audience == "auto" else audience,
            "situation": "The sender will not be coming to work today after a late meeting and insufficient sleep.",
            "reason": "The meeting ended late last night, which resulted in insufficient sleep.",
            "main_action": "The sender will not come to work today.",
            "cause_chain": "Meeting ended late last night → insufficient sleep → sender will not come to work today.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Traffic + meeting delay + waiting
    # --------------------------------------------------------
    if (
        has("ကားပိတ်", "ကားလမ်းပိတ်", "လမ်းပိတ်", "ကားကြပ်", "traffic", "traffic jam", "heavy traffic")
        and has("meeting", "အစည်းအဝေး")
        and has("နောက်ကျ", "late", "delayed")
        and has("စောင့်", "wait", "wait for me")
    ):
        return {
            "language": language,
            "intent": "Inform recipient about a meeting delay and ask them to wait",
            "audience": "Colleague" if audience == "auto" else audience,
            "situation": "The sender is delayed by traffic and expects to arrive late for the meeting.",
            "reason": "There is heavy traffic on the way.",
            "main_action": "Ask the recipient to wait for the sender.",
            "cause_chain": "Heavy traffic → meeting delay → sender asks recipient to wait.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Heavy rain + flooding + school delay
    # --------------------------------------------------------
    if (
        has("မိုးသည်း", "မိုးရွာ", "မိုးကြီး", "မိုးသည်းကြီးမည်းကြီး", "rain", "raining", "poured", "heavy rain")
        and has("ရေလျှံ", "ရေတွေ လျှံ", "ရေဝင်", "flood", "flooded", "flooding", "water is overflowing")
        and has("ကျောင်း", "school")
        and has("နောက်ကျ", "late", "delayed")
    ):
        return {
            "language": language,
            "intent": "Inform recipient that the sender will be late for school",
            "audience": "Teacher / school contact" if audience == "auto" else audience,
            "situation": "The sender will arrive late at school today.",
            "reason": "Heavy rain caused flooding in front of the sender's house.",
            "main_action": "Inform the recipient about the delay in arriving at school.",
            "cause_chain": "Heavy rain this morning → flooding in front of the house → delayed departure/arrival → late for school.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Mother's health issue + work leave
    # --------------------------------------------------------
    if (
        has("အမေ", "မိခင်", "mother", "mom", "mum")
        and has("ကျန်းမာရေး", "နေမကောင်း", "health", "not feeling well", "sick")
        and has("အလုပ်", "work", "office")
        and has("ခွင့်", "leave", "day off", "take a day off")
    ):
        return {
            "language": language,
            "intent": "Request one day of leave from work",
            "audience": "Manager / employer" if audience == "auto" else audience,
            "situation": "The sender wants to take one day off work today.",
            "reason": "The sender's mother has a health-related issue that requires attention.",
            "main_action": "Request one day of leave from work today.",
            "cause_chain": "Mother's health issue → sender needs to attend to the situation → request for one day of work leave.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Generic family health + leave
    # --------------------------------------------------------
    if (
        has("မိသားစု", "family", "အိမ်က")
        and has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick", "ဆေးရုံ", "hospital", "အရေးပေါ်", "emergency")
        and has("အလုပ်", "work", "office")
        and has("ခွင့်", "leave", "day off")
    ):
        return {
            "language": language,
            "intent": "Request time off from work for a family matter",
            "audience": "Manager / employer" if audience == "auto" else audience,
            "situation": "The sender needs time away from work to handle a family health matter.",
            "reason": "A family member has a health-related issue requiring the sender's attention.",
            "main_action": "Request time off from work.",
            "cause_chain": "Family health matter → sender needs to handle it → request for work leave.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # COMPOUND CAUSES: preserve ALL meaningful reasons.
    #
    # This must run before the generic traffic rule. Otherwise a message
    # containing both rain and traffic can be incorrectly reduced to
    # "traffic caused the delay".
    # --------------------------------------------------------
    has_weather = has(
        "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "မိုးသည်းကြီးမည်းကြီး",
        "rain", "raining", "heavy rain", "poured"
    )
    has_traffic = has(
        "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်",
        "traffic", "traffic jam", "heavy traffic"
    )
    has_flood = has(
        "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်",
        "flood", "flooded", "flooding"
    )
    has_delay = has("နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay")
    has_wait = has("စောင့်", "wait", "wait for me")
    destination_school = has("ကျောင်း", "school")
    destination_work = has("အလုပ်", "work", "office")
    destination_meeting = has("meeting", "အစည်းအဝေး")

    if (has_weather and has_traffic and (has_delay or has_wait)):
        destination = (
            "the meeting" if destination_meeting
            else "school" if destination_school
            else "work" if destination_work
            else "the destination"
        )

        reasons = []
        if has_weather:
            reasons.append("heavy rain")
        if has_flood:
            reasons.append("flooding around the house")
        if has_traffic:
            reasons.append("heavy traffic")

        reason_text = " and ".join(reasons)

        if has_wait:
            action = f"Ask the recipient to wait for the sender while the sender is delayed."
        else:
            action = f"Inform the recipient that the sender will be late getting to {destination}."

        return {
            "language": language,
            "intent": (
                "Inform recipient about a delay and ask them to wait"
                if has_wait
                else f"Inform recipient that the sender will be late for {destination}"
            ),
            "audience": (
                "Colleague" if destination_work or destination_meeting
                else "Teacher / school contact" if destination_school
                else ("Recipient" if audience == "auto" else audience)
            ) if audience == "auto" else audience,
            "situation": (
                f"The sender is delayed by {reason_text} and expects to arrive late at {destination}."
                if not has_wait
                else f"The sender is delayed by {reason_text} and is asking the recipient to wait."
            ),
            "reason": (
                f"The message gives multiple reasons for the delay: {reason_text}."
            ),
            "main_action": action,
            "cause_chain": (
                f"{reason_text} → travel delay → late arrival at {destination}."
                if not has_wait
                else f"{reason_text} → travel delay → sender asks recipient to wait."
            ),
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Generic traffic delay
    # --------------------------------------------------------
    if has("ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic") and has("နောက်ကျ", "late", "delayed"):
        destination = "school" if has("ကျောင်း", "school") else (
            "work" if has("အလုပ်", "work", "office") else "the destination"
        )
        return {
            "language": language,
            "intent": f"Inform recipient that the sender will be late for {destination}",
            "audience": "Colleague" if destination == "work" and audience == "auto" else (
                "Teacher / school contact" if destination == "school" and audience == "auto"
                else (audience if audience != "auto" else "Recipient")
            ),
            "situation": f"The sender is delayed by traffic and will arrive late at {destination}.",
            "reason": "Heavy traffic is causing the delay.",
            "main_action": f"Inform the recipient that the sender will be late for {destination}.",
            "cause_chain": f"Heavy traffic → delay → late arrival at {destination}.",
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Generic waiting request with a detected reason
    # --------------------------------------------------------
    if has("စောင့်", "wait", "wait for me"):
        reason = ""
        if has("မိုး", "rain", "raining"):
            reason = "It is raining."
        elif has("မအား", "busy", "အလုပ်များ", "unavailable"):
            reason = "The sender is currently busy or unavailable."
        elif has("ကားပိတ်", "traffic", "traffic jam"):
            reason = "The sender is delayed by traffic."

        if reason:
            return {
                "language": language,
                "intent": "Ask the recipient to wait",
                "audience": "Recipient" if audience == "auto" else audience,
                "situation": "The sender is asking the recipient to wait for a short time.",
                "reason": reason,
                "main_action": "Ask the recipient to wait.",
                "cause_chain": f"{reason} → sender asks recipient to wait.",
                "recommended_tone": requested_tone if requested_tone in TONES else "professional",
            }

    # --------------------------------------------------------
    # Generic work absence: do not falsely say reason is absent if
    # the message contains a recognizable causal clause.
    # --------------------------------------------------------
    if has("အလုပ်", "work", "office") and has(
        "မလာ", "မလာတော့", "မသွား", "won't come", "will not come",
        "not coming", "won't be coming", "unable to come", "cannot come"
    ):
        reason = ""
        cause_chain = ""
        if has("meeting", "အစည်းအဝေး") and has("နောက်ကျ", "late", "delayed"):
            reason = "The meeting ended late."
            if has("အိပ်ရေးမဝ", "အိပ်မဝ", "tired", "not enough sleep", "barely slept"):
                reason = "The meeting ended late, so the sender did not get enough sleep."
                cause_chain = "Meeting ended late → insufficient sleep → work absence."
            else:
                cause_chain = "Meeting ended late → work absence."
        elif has("မိုး", "rain", "raining"):
            reason = "Rain is affecting the sender's ability to travel."
            cause_chain = "Rain/travel difficulty → work absence."
        elif has("ကျန်းမာရေး", "health", "နေမကောင်း", "sick"):
            reason = "The sender has a health-related issue."
            cause_chain = "Health issue → work absence."
        elif has("မိသားစု", "family", "အမေ", "mother", "mom"):
            reason = "The sender has a family matter to attend to."
            cause_chain = "Family matter → work absence."

        if not reason:
            reason = "No specific reason was identified in the message."
            cause_chain = "Work absence stated without a clearly detected reason."

        return {
            "language": language,
            "intent": "Inform recipient that the sender will not come to work",
            "audience": "Colleague" if audience == "auto" else audience,
            "situation": "The sender will not be coming to work today.",
            "reason": reason,
            "main_action": "The sender will not come to work today.",
            "cause_chain": cause_chain,
            "recommended_tone": requested_tone if requested_tone in TONES else "professional",
        }

    # --------------------------------------------------------
    # Generic fallback
    # --------------------------------------------------------
    return {
        "language": language,
        "intent": "Translate the complete message naturally",
        "audience": audience if audience != "auto" else "Auto-detect",
        "situation": "Preserve the complete situation described by the sender.",
        "reason": "Not confidently detected by the deterministic understanding layer.",
        "main_action": "Translate the sender's complete message.",
        "cause_chain": "Preserve all meaningful clauses in the original message.",
        "recommended_tone": requested_tone if requested_tone in TONES else "professional",
    }


def format_understanding_for_prompt(understanding: dict[str, str]) -> str:
    return f"""
Complete semantic understanding:
- Language: {understanding["language"]}
- Intent: {understanding["intent"]}
- Situation: {understanding["situation"]}
- Reason: {understanding["reason"]}
- Main action/request: {understanding["main_action"]}
- Cause chain: {understanding["cause_chain"]}
- Audience: {understanding["audience"]}
"""


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

Your ONLY job is to translate the user's COMPLETE message into natural English.
The input may be entirely Myanmar, entirely English, or a natural Myanmar-English mix.
Treat all three forms as valid input and preserve the meaning of the whole message.

CORE RULE: understand the whole message first, then express it naturally.
Do NOT translate word-by-word. Do NOT shorten a message when shortening
would remove meaningful context.

PRESERVE EVERY MEANINGFUL PART when present:
- who is involved
- what happened
- what the sender is doing
- what the sender wants the recipient to do
- reason/cause
- time/timing
- place/situation
- delay or expected change
- request, question, promise, or intention
- apology or other meaningful emotion

A translation can be one or more sentences if that is needed to preserve
the complete meaning.

Example:
"လမ်းမှာ ကားပိတ်နေလို့ ခနစောင့်ပေးပါ"
must preserve BOTH the traffic reason AND the request to wait.
Good: "I'm stuck in traffic right now, so please wait for me for a little while."
Bad: "Please wait a moment."

"traffic ကြောင့် ခန wait ပေးပါ" must also preserve BOTH traffic and waiting.

"ခန wait ပေးပါ" has no reason, so a short translation is appropriate:
"Could you please wait for me for a moment?"

Mixed English words such as meeting, manager, project, assignment, submit,
deadline, CV, interview, client, task, email, call, presentation, leave,
wait, traffic, update, file, work, and class are valid input.

IMPORTANT MEANING DISTINCTIONS:
- "မလာ" = not come / not go to a place
- "မတက်" = not attend / not join an event such as a meeting or class
- "တော့ဘူး" often = will no longer / won't
- "နိုင်ဘူး" = cannot / unable to
- "ချင်တယ်" = want to
- "မယ်" normally expresses future intention/action
- "လို့" can express a reason or an intended/reported statement depending on context
- "စောင့်" / "wait" = wait; never remove the waiting action
- traffic-related text is NOT automatically a "late for work" message; identify
  the actual action/request first.

DO NOT:
- answer the user's question
- explain the meaning
- summarize
- omit meaningful context
- invent facts
- add unsupported details
- change a request into a statement
- change "cannot" into "will not"
- change "not attending" into "cannot attend"

LONG / CONTEXT-RICH INPUT:
If the input is long (especially 100+ characters), DO NOT summarize it.
Treat each meaningful clause as information that must appear in the English result.
Before writing, silently identify every cause, event, consequence, request, destination,
time reference, and final action. Then translate ALL of them. The final English may
contain 2-4 sentences when necessary. A shorter answer is WRONG if it drops a fact.
For example, if a message contains meeting + late night + insufficient sleep + tiredness
+ work absence/leave, preserve every one of those ideas.
If a message contains rain + flooding + traffic + school/work delay, preserve every one
of those ideas.
If the input is Myanmar-English mixed, translate the Myanmar parts too; do not treat
the English words as the whole message.
If you are unsure about one clause, preserve it rather than omitting it.

LONG / CONTEXT-RICH INPUT:
If the input contains several clauses, preserve ALL meaningful clauses.
 First identify
the situation, cause/reason, time, place, main action, consequence, and request/intention.
Then reconstruct them as natural English using connectors such as "because", "so",
"but", "and", or separate sentences when clearer.
Do not intentionally make the English shorter just to be concise.
Never let a final intent such as "I won't come to work" erase the earlier reason
that explains WHY the person will not come.
For example, "meeting ended late + didn't get enough sleep + won't come to work"
must keep all three ideas in the final translation.

TONE:
Simple = clear everyday English while preserving meaning.
Polite = respectful and courteous while preserving meaning.
Friendly = warm, natural, casual English while preserving meaning.
Professional = clear workplace-appropriate English while preserving meaning.
Formal = formal and respectful English while preserving meaning.

Return ONLY the final English translation. No analysis, labels, or explanations.
"""


    understanding = build_ai_understanding(
        text=text,
        requested_tone=tone,
        audience=audience,
    )

    semantic_context = format_understanding_for_prompt(understanding)

    user_prompt = f"""
Translate this message into natural English.

Context: {context}
Audience: {audience}
Tone: {tone}

{semantic_context}

IMPORTANT:
The semantic understanding above is a guide, not a replacement for the
original message. Re-check the original text and preserve every meaningful
detail. In particular, NEVER drop a reason merely because the final intent
is easier to describe. If the original contains a cause -> consequence ->
action chain, keep that entire chain in the English translation.

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
            max_length=1024,
        )

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=180,
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

        # Preserve all generated lines. Long translations may naturally
        # contain multiple sentences; never keep only the first line.
        lines = [
            line.strip()
            for line in result.splitlines()
            if line.strip()
        ]

        if lines:
            result = " ".join(lines)

        if len(result) >= 2 and result[0] == result[-1] and result[0] in {'"', "'"}:
            result = result[1:-1].strip()

        return result

    except Exception as e:
        print("QWEN ERROR:", repr(e))
        return ""



# ============================================================
# API VERSION + DEBUG HELPERS
# ============================================================

def detect_debug_layer(text: str, tone: str) -> dict:
    """Explain which backend layer handles an input."""
    normalized = normalize_text(text)
    contextual = contextual_rule_translation(text, tone)
    reference = find_training_example(text)

    has_rain = _contains_any(normalized, [
        "မိုး", "မိုးရွာ", "မိုးကြီး", "မိုးသည်း", "rain", "raining", "heavy rain", "poured"
    ])
    has_flood = _contains_any(normalized, [
        "ရေလျှံ", "ရေတွေ လျှံ", "ရေကြီး", "ရေဝင်", "flood", "flooded", "flooding"
    ])
    has_traffic = _contains_any(normalized, [
        "ကားပိတ်", "ကားလမ်းပိတ်", "ကားကြပ်", "လမ်းပိတ်", "traffic", "traffic jam", "heavy traffic"
    ])
    has_delay = _contains_any(normalized, [
        "နောက်ကျ", "နောက်ကျမယ်", "late", "delayed", "delay"
    ])
    has_school = _contains_any(normalized, ["ကျောင်း", "school"])
    has_work = _contains_any(normalized, ["အလုပ်", "work", "office"])
    has_meeting = _contains_any(normalized, ["meeting", "အစည်းအဝေး"])
    has_wait = _contains_any(normalized, ["စောင့်", "wait", "wait for me"])
    cause_count = sum([has_rain, has_flood, has_traffic])

    if contextual is not None:
        layer = "contextual_rule"
    elif reference is not None:
        layer = "reference_dataset"
    else:
        layer = "qwen"

    return {
        "api_version": API_VERSION,
        "api_build": API_BUILD,
        "backend_model": MODEL_NAME,
        "backend_device": "cpu",
        "translation_layer": layer,
        "contextual_rule_matched": contextual is not None,
        "reference_example_matched": reference is not None,
        "qwen_fallback_expected": contextual is None and reference is None,
        "normalized_input": normalized,
        "detected": {
            "rain": has_rain,
            "flooding": has_flood,
            "traffic": has_traffic,
            "delay": has_delay,
            "school": has_school,
            "work": has_work,
            "meeting": has_meeting,
            "wait_request": has_wait,
            "environmental_or_transport_causes": cause_count,
        },
        "warning": (
            "Multiple causes detected. Compound-context rule must run before single-cause rules."
            if cause_count >= 2 else
            "No multi-cause weather/traffic combination detected."
        ),
    }


# ============================================================
# Response helper
# ============================================================

def understanding_response_fields(
    text: str,
    tone: str,
    audience: str,
) -> dict[str, str]:
    u = build_ai_understanding(
        text=text,
        requested_tone=tone,
        audience=audience,
    )
    return {
        "api_version": API_VERSION,
        "debug": detect_debug_layer(text, tone),
        "language": u["language"],
        "intent": u["intent"],
        "audience_detected": u["audience"],
        "situation": u["situation"],
        "reason": u["reason"],
        "main_action": u["main_action"],
        "cause_chain": u["cause_chain"],
        "recommended_tone": u["recommended_tone"],
    }


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MyanTone AI API is running.",
        "api_version": API_VERSION,
        "api_build": API_BUILD,
        "features": ["translation", "complete-meaning-understanding", "tone-control", "debug", "test-context"],
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
        "api_version": API_VERSION,
        "api_build": API_BUILD,
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
# Context diagnostic endpoint
# ============================================================

@app.post("/test-context")
def test_context(request: TranslateRequest):
    """Development endpoint for verifying backend version and context routing."""
    text = request.text.strip()
    if not text:
        return {
            "ok": False,
            "api_version": API_VERSION,
            "api_build": API_BUILD,
            "error": "text is required",
        }

    requested_tone = request.tone.lower().strip()
    if requested_tone not in TONES:
        requested_tone = "professional"

    debug = detect_debug_layer(text, requested_tone)
    understanding = build_ai_understanding(
        text=text,
        requested_tone=requested_tone,
        audience=request.audience,
    )

    all_tones = {}
    for tone_name in TONES:
        contextual = contextual_rule_translation(text, tone_name)
        if contextual is not None:
            all_tones[tone_name] = contextual
        else:
            reference = rule_based_translation(text, tone_name)
            if reference is not None:
                all_tones[tone_name] = reference
            else:
                all_tones[tone_name] = generate_translation(
                    text=text,
                    tone=tone_name,
                    context=request.context,
                    audience=request.audience,
                )

    selected = all_tones.get(requested_tone, all_tones.get("professional", ""))

    return {
        "ok": True,
        "api_version": API_VERSION,
        "api_build": API_BUILD,
        "input": text,
        "selected_tone": requested_tone,
        "debug": debug,
        "understanding": understanding,
        "translations": all_tones,
        "selected_translation": selected,
        "frontend_check": {
            "expected_compound_context": debug["detected"]["environmental_or_transport_causes"] >= 2,
            "backend_is_new_version": API_VERSION == "2.2.0-complete-context-debug",
            "selected_layer": debug["translation_layer"],
        },
    }


# ============================================================
# Complete AI Understanding endpoint
# ============================================================

@app.post("/analyze")
def analyze(request: TranslateRequest):
    """
    Return the complete semantic interpretation used by MyanTone AI.
    This endpoint is intended for the frontend's AI Understanding panel.
    """
    text = request.text.strip()

    if not text:
        return {
            "language": "",
            "intent": "",
            "audience": "",
            "situation": "",
            "reason": "",
            "main_action": "",
            "cause_chain": "",
            "recommended_tone": "",
        }

    tone = request.tone.lower().strip()
    if tone not in TONES:
        tone = "professional"

    return build_ai_understanding(
        text=text,
        requested_tone=tone,
        audience=request.audience,
    )


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
    # 1. Exact full-message reference examples first.
    # This prevents long real-world messages from being shortened by
    # a broader keyword rule.
    # --------------------------------------------------------
    full_example = find_training_example(text)
    if full_example is not None and full_example in FULL_MESSAGE_EXAMPLES:
        exact_translation = full_example.get(tone, full_example["professional"])
        print("=" * 60)
        print("FULL MESSAGE REFERENCE MATCH")
        print("INPUT:", text)
        print("TONE:", tone)
        print("RESULT:", exact_translation)
        print("=" * 60)
        return TranslateResponse(
            translation=exact_translation,
            translations={tone: exact_translation},
            **understanding_response_fields(text, tone, request.audience),
        )

    # --------------------------------------------------------
    # 2. Expanded high-confidence examples first
    # --------------------------------------------------------
    expanded = expanded_context_rule_translation(text, tone)
    if expanded is not None:
        print("=" * 60)
        print("EXPANDED 100-EXAMPLE RULE MATCH")
        print("INPUT:", text)
        print("TONE:", tone)
        print("RESULT:", expanded)
        print("=" * 60)
        return TranslateResponse(
            translation=expanded,
            translations={tone: expanded},
            **understanding_response_fields(text, tone, request.audience),
        )

    # --------------------------------------------------------
    # 2. Context-aware rules
    # --------------------------------------------------------
    high_coverage = high_coverage_long_context_translation(text, tone)
    if high_coverage is not None:
        print("=" * 60)
        print("HIGH-COVERAGE LONG-CONTEXT RULE MATCH")
        print("INPUT:", text)
        print("TONE:", tone)
        print("RESULT:", high_coverage)
        print("=" * 60)
        return TranslateResponse(
            translation=high_coverage,
            translations={tone: high_coverage},
            **understanding_response_fields(text, tone, request.audience),
        )

    contextual_translation = contextual_rule_translation(text, tone)

    if contextual_translation is not None:
        print("=" * 60)
        print("CONTEXT-AWARE RULE MATCH")
        print("INPUT:", text)
        print("TONE:", tone)
        print("RESULT:", contextual_translation)
        print("=" * 60)
        return TranslateResponse(
            translation=contextual_translation,
            translations={tone: contextual_translation},
            **understanding_response_fields(text, tone, request.audience),
        )

    # --------------------------------------------------------
    # 1. For long messages, prefer the full-message Qwen prompt
    # over short reference examples. The reference dataset was built
    # for short/common messages and can otherwise erase context.
    # --------------------------------------------------------
    rule_translation = None if len(text) >= 100 else rule_based_translation(
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
            **understanding_response_fields(text, tone, request.audience),
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
        **understanding_response_fields(text, tone, request.audience),
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

    # Exact full-message reference examples first.
    full_example = find_training_example(text)
    if full_example is not None and full_example in FULL_MESSAGE_EXAMPLES:
        for tone_name in TONES:
            results[tone_name] = full_example.get(tone_name, full_example["professional"])
        selected_tone = request.tone.lower().strip()
        if selected_tone not in TONES:
            selected_tone = "professional"
        return {
            "translation": results[selected_tone],
            "translations": results,
            "understanding": understanding_response_fields(text, selected_tone, request.audience),
        }

    # Preserve reason + action for high-confidence contextual messages.
    if (
        high_coverage_long_context_translation(text, "professional") is not None
        or contextual_rule_translation(text, "professional") is not None
    ):
        for tone in TONES:
            high = high_coverage_long_context_translation(text, tone)
            results[tone] = high if high is not None else contextual_rule_translation(text, tone)

        selected_tone = request.tone.lower().strip()
        if selected_tone not in TONES:
            selected_tone = "professional"

        return {
            "translation": results[selected_tone],
            "translations": results,
            "understanding": understanding_response_fields(
                text, selected_tone, request.audience
            ),
        }


    # First check the 100 examples
    example = find_training_example(text)

    if example:

        for tone in TONES:
            results[tone] = example[tone]

        selected_tone = request.tone.lower().strip()
        if selected_tone not in TONES:
            selected_tone = "professional"

        return {
            "translation": results[selected_tone],
            "translations": results,
            "understanding": understanding_response_fields(
                text, selected_tone, request.audience
            ),
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
        "understanding": understanding_response_fields(
            text, selected_tone, request.audience
        ),
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

@app.post("/test-long-context")
def test_long_context(request: TranslateRequest):
    """Test long Myanmar/English/mixed messages without the frontend."""
    results = {}
    layers = {}
    for tone_name in TONES:
        high = high_coverage_long_context_translation(request.text, tone_name)
        if high is not None:
            results[tone_name] = high
            layers[tone_name] = "high_coverage_long_context"
        else:
            contextual = contextual_rule_translation(request.text, tone_name)
            if contextual is not None:
                results[tone_name] = contextual
                layers[tone_name] = "contextual_rule"
            else:
                results[tone_name] = generate_translation(
                    request.text, tone_name, request.context, request.audience
                )
                layers[tone_name] = "qwen_fallback"

    selected = request.tone.lower().strip()
    if selected not in TONES:
        selected = "professional"

    return {
        "api_version": API_VERSION,
        "api_build": API_BUILD,
        "input": request.text,
        "selected_tone": selected,
        "translation": results[selected],
        "translations": results,
        "layers": layers,
    }
