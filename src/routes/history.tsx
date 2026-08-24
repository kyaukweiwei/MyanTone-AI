import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { history, type HistoryItem } from "@/lib/store";
import { Copy, Star, Trash2 } from "lucide-react";

export const Route = createFileRoute("/history")({
  head: () => ({
    meta: [
      { title: "My History — Saved Translations & Emails | MyanTone AI" },
      {
        name: "description",
        content:
          "Revisit every Myanmar message you translated and every English email you generated with MyanTone AI.",
      },
      { property: "og:title", content: "My History — MyanTone AI" },
      { property: "og:description", content: "Your translations, emails and saved drafts in one place." },
    ],
  }),
  component: HistoryPage,
});

function useHistory() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  useEffect(() => {
    const sync = () => setItems(history.all());
    sync();
    window.addEventListener("myantone:history", sync);
    return () => window.removeEventListener("myantone:history", sync);
  }, []);
  return items;
}

function List({ items }: { items: HistoryItem[] }) {
  if (items.length === 0)
    return (
      <p className="card-soft p-10 text-center text-sm text-muted-foreground">
        Nothing here yet — your translations and emails will be listed here.
      </p>
    );
  return (
    <ul className="space-y-4">
      {items.map((i) => (
        <li key={i.id} className="card-soft p-5">
          <div className="flex flex-wrap items-center gap-2 text-[11px] font-semibold uppercase tracking-widest">
            <span className="rounded-full bg-teal-soft px-2.5 py-1 text-accent-foreground">
              {i.kind}
            </span>
            <span className="rounded-full bg-secondary px-2.5 py-1 text-muted-foreground">{i.tone}</span>
            {i.audience && (
              <span className="rounded-full bg-secondary px-2.5 py-1 text-muted-foreground">
                {i.audience}
              </span>
            )}
            <span className="ml-auto font-normal normal-case tracking-normal text-muted-foreground">
              {new Date(i.createdAt).toLocaleString()}
            </span>
          </div>
          {i.subject && <p className="mt-3 font-semibold text-primary">{i.subject}</p>}
          <p className="font-my mt-2 text-sm text-muted-foreground">{i.original}</p>
          <p className="mt-2 whitespace-pre-wrap text-[15px] leading-relaxed text-primary">{i.output}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={async () => {
                await navigator.clipboard.writeText(i.output);
                toast.success("Copied");
              }}
            >
              <Copy /> Copy
            </Button>
            <Button size="sm" variant="outline" onClick={() => history.toggleSave(i.id)}>
              <Star className={i.saved ? "fill-amber text-amber" : ""} /> {i.saved ? "Saved" : "Save"}
            </Button>
            <Button size="sm" variant="ghost" onClick={() => history.remove(i.id)}>
              <Trash2 /> Delete
            </Button>
          </div>
        </li>
      ))}
    </ul>
  );
}

function HistoryPage() {
  const items = useHistory();
  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">My History</p>
          <h1 className="mt-2 text-3xl sm:text-4xl">Everything you've written</h1>
        </div>
        {items.length > 0 && (
          <Button variant="ghost" size="sm" onClick={() => history.clear()}>
            Clear all
          </Button>
        )}
      </header>

      <Tabs defaultValue="all">
        <TabsList className="mb-6">
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="translations">Translations</TabsTrigger>
          <TabsTrigger value="emails">Emails</TabsTrigger>
          <TabsTrigger value="saved">Saved</TabsTrigger>
        </TabsList>
        <TabsContent value="all">
          <List items={items} />
        </TabsContent>
        <TabsContent value="translations">
          <List items={items.filter((i) => i.kind === "translation")} />
        </TabsContent>
        <TabsContent value="emails">
          <List items={items.filter((i) => i.kind === "email")} />
        </TabsContent>
        <TabsContent value="saved">
          <List items={items.filter((i) => i.saved)} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
