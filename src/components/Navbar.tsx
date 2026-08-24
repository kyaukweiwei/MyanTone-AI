import { Link } from "@tanstack/react-router";
import { Globe, HelpCircle, Languages, LayoutGrid, Mail, Clock, User, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Logo } from "./Logo";

export const TABS = [
  { to: "/translate", label: "Translate", icon: Languages },
  { to: "/email", label: "Email Studio", icon: Mail },
  { to: "/templates", label: "Templates", icon: LayoutGrid },
  { to: "/history", label: "History", icon: Clock },
] as const;

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/70 bg-background/85 backdrop-blur-xl">
      <nav
        aria-label="Main navigation"
        className="mx-auto flex h-16 max-w-7xl items-center gap-6 px-4 sm:px-6"
      >
        <Link to="/" className="shrink-0" aria-label="MyanTone AI home">
          <Logo />
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {TABS.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className="rounded-full px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-primary"
              activeProps={{ className: "bg-secondary text-primary" }}
            >
              {label}
            </Link>
          ))}
        </div>

        <div className="ml-auto flex items-center gap-1">
          <Button variant="ghost" size="icon" aria-label="Language" className="hidden sm:inline-flex">
            <Globe className="size-4" />
          </Button>
          <Button variant="ghost" size="icon" aria-label="Help" className="hidden sm:inline-flex">
            <HelpCircle className="size-4" />
          </Button>
          <Button variant="ghost" size="icon" aria-label="Profile" className="hidden sm:inline-flex">
            <User className="size-4" />
          </Button>
          <Button asChild variant="teal" size="sm" className="ml-1">
            <Link to="/translate">
              <Sparkles className="size-4" /> Try AI
            </Link>
          </Button>
        </div>
      </nav>
    </header>
  );
}

export function MobileTabBar() {
  return (
    <nav
      aria-label="Mobile navigation"
      className="fixed inset-x-0 bottom-0 z-40 border-t border-border bg-card/95 backdrop-blur md:hidden"
    >
      <ul className="mx-auto flex max-w-md">
        {TABS.map(({ to, label, icon: Icon }) => (
          <li key={to} className="flex-1">
            <Link
              to={to}
              className="flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium text-muted-foreground"
              activeProps={{ className: "text-teal" }}
            >
              <Icon className="size-5" aria-hidden />
              {label === "Email Studio" ? "Email" : label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
