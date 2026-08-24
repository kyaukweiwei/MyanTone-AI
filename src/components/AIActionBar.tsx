import { Button } from "@/components/ui/button";
import type { ImproveAction } from "@/lib/myantone-engine";
import { Copy, RefreshCw, Scissors, Sparkles } from "lucide-react";

export type BarAction = ImproveAction | "regenerate" | "copy";

const ACTIONS: { id: BarAction; label: string; emoji?: string }[] = [
  { id: "improve", label: "Improve", emoji: "✨" },
  { id: "shorten", label: "Shorten", emoji: "✂" },
  { id: "polite", label: "Make Polite", emoji: "🙏" },
  { id: "professional", label: "Make Professional", emoji: "💼" },
  { id: "friendly", label: "Make Friendly", emoji: "😊" },
  { id: "formal", label: "Make Formal", emoji: "📚" },
  { id: "regenerate", label: "Regenerate", emoji: "🔄" },
  { id: "copy", label: "Copy", emoji: "📋" },
];

export function AIActionBar({
  onAction,
  busy,
  only,
}: {
  onAction: (a: BarAction) => void;
  busy?: boolean;
  only?: BarAction[];
}) {
  const items = only ? ACTIONS.filter((a) => only.includes(a.id)) : ACTIONS;
  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label="AI actions">
      {items.map((a) => (
        <Button
          key={a.id}
          size="sm"
          variant="outline"
          disabled={busy}
          onClick={() => onAction(a.id)}
          aria-label={a.label}
        >
          {a.id === "regenerate" ? (
            <RefreshCw className={busy ? "animate-spin" : ""} />
          ) : a.id === "copy" ? (
            <Copy />
          ) : a.id === "shorten" ? (
            <Scissors />
          ) : (
            <Sparkles />
          )}
          {a.label}
        </Button>
      ))}
    </div>
  );
}
