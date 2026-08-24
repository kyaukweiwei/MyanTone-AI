import type { AIFallbackReason } from "@/lib/myantone-engine";
import { AlertTriangle } from "lucide-react";

const MESSAGES: Record<AIFallbackReason, string> = {
  missing_key:
    "AI model is not connected (LOVABLE_API_KEY is missing). Showing basic offline results — see README.md for local setup.",
  rate_limit: "AI model is rate limited right now. Showing basic offline results — try again shortly.",
  credits: "AI credits are exhausted for this workspace. Showing basic offline results.",
  upstream: "The AI model could not be reached. Showing basic offline results.",
  bad_output: "The AI model returned an unusable response. Showing basic offline results.",
};

export function OfflineModeNotice({ reason }: { reason?: AIFallbackReason }) {
  if (!reason) return null;
  return (
    <div
      role="status"
      className="flex items-start gap-3 rounded-2xl border border-amber/40 bg-amber/10 p-4 text-sm text-primary"
    >
      <AlertTriangle className="mt-0.5 size-4 shrink-0 text-amber" aria-hidden />
      <p>{MESSAGES[reason]}</p>
    </div>
  );
}
