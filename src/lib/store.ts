export type HistoryItem = {
  id: string;
  kind: "translation" | "email";
  original: string;
  output: string;
  subject?: string;
  tone: string;
  audience?: string;
  createdAt: number;
  saved?: boolean;
};

const KEY = "myantone.history.v1";

function read(): HistoryItem[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(window.localStorage.getItem(KEY) ?? "[]") as HistoryItem[];
  } catch {
    return [];
  }
}

function write(items: HistoryItem[]) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, JSON.stringify(items));
  window.dispatchEvent(new Event("myantone:history"));
}

export const history = {
  all: read,
  add(item: Omit<HistoryItem, "id" | "createdAt">) {
    const items = read();
    items.unshift({ ...item, id: crypto.randomUUID(), createdAt: Date.now() });
    write(items.slice(0, 100));
  },
  remove(id: string) {
    write(read().filter((i) => i.id !== id));
  },
  toggleSave(id: string) {
    write(read().map((i) => (i.id === id ? { ...i, saved: !i.saved } : i)));
  },
  clear() {
    write([]);
  },
};
