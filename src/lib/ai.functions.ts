import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

const schema = z.object({
  system: z.string(),
  user: z.string(),
});

/**
 * Thin wrapper over the Lovable AI Gateway. Returns the raw assistant text.
 * The caller is responsible for parsing (we always ask for JSON).
 */
export const aiComplete = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => schema.parse(data))
  .handler(async ({ data }) => {
    const apiKey = process.env["LOVABLE_API_KEY"];
    if (!apiKey) return { ok: false as const, error: "missing_key", text: "" };

    const res = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "google/gemini-3-flash",
        messages: [
          { role: "system", content: data.system },
          { role: "user", content: data.user },
        ],
        response_format: { type: "json_object" },
      }),
    });

    if (!res.ok) {
      const detail = await res.text();
      return {
        ok: false as const,
        error: res.status === 429 ? "rate_limit" : res.status === 402 ? "credits" : "upstream",
        text: detail.slice(0, 300),
      };
    }

    const json = (await res.json()) as {
      choices?: { message?: { content?: string } }[];
    };
    return { ok: true as const, error: "", text: json.choices?.[0]?.message?.content ?? "" };
  });
