import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("=" * 60)
print("MyanTone AI - Local Qwen Test")
print("=" * 60)

print(f"PyTorch: {torch.__version__}")
print("Device: CPU")

# ---------------------------------------------------------
# Load tokenizer
# ---------------------------------------------------------

print("\n[1/3] Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Tokenizer loaded.")

# ---------------------------------------------------------
# Load model
# ---------------------------------------------------------

print("\n[2/3] Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
)

model.eval()

print("Qwen model loaded.")

# ---------------------------------------------------------
# MyanTone prompt
# ---------------------------------------------------------

prompt = """
You are MyanTone AI, a Myanmar-first English communication assistant.

Convert the Myanmar message below into natural English.

Myanmar:
ဒီနေ့ meeting မတက်နိုင်ဘူးလို့ အလုပ်ကလူကို ပြောချင်တယ်။

Tone:
Professional

Rules:
- Preserve the original meaning.
- Do not translate word-for-word.
- Use natural English.
- Make it appropriate for communicating with a colleague.
- Return only the final English sentence.
"""

messages = [
    {
        "role": "user",
        "content": prompt,
    }
]

# ---------------------------------------------------------
# Prepare input
# ---------------------------------------------------------

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

inputs = tokenizer(
    text,
    return_tensors="pt",
)

# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

print("\n[3/3] Generating MyanTone response...")
print("CPU inference may take some time.\n")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False,
    )

generated_tokens = outputs[
    0,
    inputs["input_ids"].shape[-1]:
]

result = tokenizer.decode(
    generated_tokens,
    skip_special_tokens=True,
)

print("=" * 60)
print("MYANTONE RESULT")
print("=" * 60)
print(result.strip())
print("=" * 60)