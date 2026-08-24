# Why local (GitHub) runs give generic translations

## အကြောင်းရင်း

Publish လုပ်ထားတဲ့ site မှာ Lovable က server-side secret `LOVABLE_API_KEY` ကို အလိုအလျောက် ထည့်ပေးထားလို့ တကယ့် AI model နဲ့ translate ဖြစ်ပါတယ်။

GitHub ကနေ download လုပ်ပြီး ကိုယ့်စက်မှာ run တဲ့အခါ အဲ့ key မပါလာဘူး (secret တွေက repo ထဲ မဝင်ဘူး)။ ဒါကြောင့် `src/lib/ai.functions.ts` က `missing_key` ပြန်ပေးပြီး၊ `myantone-engine.ts` က တိတ်တဆိတ် rule-based fallback ကို သုံးလိုက်တယ် — အဲ့ဒါက "I wanted to let you know about this." လိုမျိုး generic စာသားတွေ ထွက်ရတဲ့ အကြောင်းရင်းပါ။

Bug မဟုတ်ပါဘူး၊ configuration ပြဿနာပါ။

## Fix အစီအစဉ်

1. **Local key support** — root မှာ `.env` ဖိုင် (Vite က server-side ဖတ်တယ်) ကနေ `LOVABLE_API_KEY` ဖတ်နိုင်အောင် လုပ်မယ်။ `.env.example` ဖိုင် ထည့်ပေးမယ်။
2. **တိတ်တဆိတ် fallback မဖြစ်အောင်** — AI မရလျှင် UI မှာ သတိပေးချက် ပြမယ်: "AI unavailable — showing basic offline result" (missing key / rate limit / credits အလိုက် message ကွဲပြားစေမယ်)၊ ဒါမှ ဘယ်တုန်းက mock ဖြစ်နေလဲ ချက်ချင်း သိမယ်။
3. **README setup section** — GitHub clone ပြီး run ဖို့ အဆင့်တွေ: `bun install`, `.env` ထဲ key ထည့်၊ `bun run dev`. Lovable AI key ကို ဘယ်ကရမလဲ (Lovable project settings) နဲ့ key မထည့်ရင် offline mode နဲ့ပဲ အလုပ်လုပ်မယ်ဆိုတာ ရှင်းပြမယ်။

## Technical notes

- `src/lib/ai.functions.ts`: handler ထဲမှာ `process.env.LOVABLE_API_KEY` ဖတ်နေတာ မှန်ပါတယ်; error code (`missing_key` / `rate_limit` / `credits` / `upstream`) ကို caller ဆီ ဆက်ပို့မယ်။
- `src/lib/myantone-engine.ts`: `askJSON` က `null` ပြန်တဲ့အခါ error reason ကိုပါ ယူဆောင်လာနိုင်အောင် return shape ကို `{ data, error }` အဖြစ် ချဲ့မယ်; `translate()` / email / improve results မှာ optional `degraded` flag ထည့်မယ်။
- `src/routes/translate.tsx`, `src/routes/email.tsx`, `src/components/ImproveEmailPanel.tsx`: `degraded` ဖြစ်ရင် banner ပြမယ် (design tokens သုံးမယ်)။
- `.env` က `.gitignore` ထဲ `*.local` နဲ့ မကာမိလို့ `.env` entry ထပ်ထည့်မယ်။
- Engine logic/prompts တွေ မပြောင်းဘူး — publish မှာ ရနေတဲ့ အရည်အသွေး အတိုင်းပဲ ရှိမယ်။
