import { Brain, Github } from "lucide-react";

export function Header() {
  return (
    <header className="flex items-center justify-between h-14 px-6 border-b border-border bg-card shrink-0">
      <div className="flex items-center gap-2">
        <Brain className="w-5 h-5 text-primary" />
        <span className="font-semibold text-sm tracking-tight">
          Knowledge Hub
        </span>
        <span className="text-xs text-muted-foreground bg-muted px-1.5 py-0.5 rounded font-mono">
          RAG
        </span>
      </div>
      <a
        href="https://github.com"
        target="_blank"
        rel="noopener noreferrer"
        className="text-muted-foreground hover:text-foreground transition-colors"
        aria-label="View on GitHub"
      >
        <Github className="w-4 h-4" />
      </a>
    </header>
  );
}
