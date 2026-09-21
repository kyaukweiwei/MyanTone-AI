import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";

/**
 * MyanTone AI Backend
 *
 * FastAPI + Qwen backend:
 * http://127.0.0.1:8000
 */

const BACKEND_URL = "http://127.0.0.1:8000";

/* =========================================================
   SHARED SCHEMA
========================================================= */

const schema = z.object({
  system: z.string().optional(),
  user: z.string().optional(),

  // Translation fields
  text: z.string().optional(),
  tone: z.string().optional(),
  context: z.string().optional(),
  audience: z.string().optional(),
});

/* =========================================================
   AI COMPLETE
   Kept for compatibility with the existing frontend.
========================================================= */

export const aiComplete = createServerFn({ method: "POST" })
  .validator((data: unknown) => schema.parse(data))
  .handler(async ({ data }) => {
    /*
     * If this function is called by existing AI-analysis code,
     * we currently return a safe local response instead of
     * depending on LOVABLE_API_KEY.
     */

    if (!data.text) {
      return {
        ok: false as const,
        error: "missing_text",
        text: "",
      };
    }

    try {
      const response = await fetch(`${BACKEND_URL}/translate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          text: data.text,
          tone: data.tone ?? "professional",
          context: data.context ?? "General",
          audience: data.audience ?? "Auto-detect",
        }),
      });

      if (!response.ok) {
        const detail = await response.text();

        console.error(
          "MyanTone backend error:",
          response.status,
          detail,
        );

        return {
          ok: false as const,
          error: "backend_error",
          text: detail.slice(0, 500),
        };
      }

      const json = (await response.json()) as {
        translation?: string;
        translations?: Record<string, string>;
      };

      return {
        ok: true as const,
        error: "",
        text: json.translation ?? "",
        translations: json.translations ?? {},
      };
    } catch (error) {
      console.error("Could not connect to MyanTone backend:", error);

      return {
        ok: false as const,
        error: "connection_error",
        text: "",
      };
    }
  });

/* =========================================================
   DIRECT TRANSLATION FUNCTION
========================================================= */

const translateSchema = z.object({
  text: z.string(),
  tone: z.enum([
    "simple",
    "polite",
    "friendly",
    "professional",
    "formal",
  ]),
  context: z.string().default("General"),
  audience: z.string().default("Auto-detect"),
});

export const translateWithBackend = createServerFn({ method: "POST" })
  .validator((data: unknown) => translateSchema.parse(data))
  .handler(async ({ data }) => {
    try {
      console.log("========================================");
      console.log("MyanTone AI FRONTEND → BACKEND");
      console.log("Text:", data.text);
      console.log("Tone:", data.tone);
      console.log("Context:", data.context);
      console.log("Audience:", data.audience);
      console.log("Backend:", `${BACKEND_URL}/translate`);
      console.log("========================================");

      const response = await fetch(`${BACKEND_URL}/translate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({
          text: data.text,
          tone: data.tone,
          context: data.context,
          audience: data.audience,
        }),
      });

      if (!response.ok) {
        const detail = await response.text();

        console.error(
          `MyanTone backend returned ${response.status}:`,
          detail,
        );

        return {
          ok: false as const,
          error: "backend_error",
          translation: "",
          translations: {},
        };
      }

      const json = (await response.json()) as {
        translation?: string;
        translations?: Record<string, string>;
      };

      console.log("Backend response:", json);

      return {
        ok: true as const,
        error: "",
        translation: json.translation ?? "",
        translations: json.translations ?? {},
      };
    } catch (error) {
      console.error(
        "MyanTone backend connection failed:",
        error,
      );

      return {
        ok: false as const,
        error: "connection_error",
        translation: "",
        translations: {},
      };
    }
  });

/* =========================================================
   BACKEND HEALTH CHECK
========================================================= */

export const checkBackendHealth = createServerFn({
  method: "GET",
}).handler(async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/health`, {
      method: "GET",
    });

    if (!response.ok) {
      return {
        ok: false as const,
        status: response.status,
      };
    }

    const data = await response.json();

    return {
      ok: true as const,
      status: 200,
      data,
    };
  } catch (error) {
    console.error("MyanTone backend health check failed:", error);

    return {
      ok: false as const,
      status: 0,
    };
  }
});
