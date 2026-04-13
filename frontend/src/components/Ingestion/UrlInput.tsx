import { useState } from "react";
import { Globe, Loader2, Plus } from "lucide-react";

interface UrlInputProps {
  onSubmit: (url: string, label?: string) => Promise<void>;
  isLoading: boolean;
}

export function UrlInput({ onSubmit, isLoading }: UrlInputProps) {
  const [url, setUrl] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = url.trim();
    if (!trimmed) return;
    await onSubmit(trimmed);
    setUrl("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-1.5">
      <div className="relative flex-1">
        <Globe className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground pointer-events-none" />
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste a URL…"
          disabled={isLoading}
          className="
            w-full h-8 pl-7 pr-2 text-xs rounded-lg border border-border bg-background
            text-foreground placeholder:text-muted-foreground
            focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
            disabled:opacity-50
          "
        />
      </div>
      <button
        type="submit"
        disabled={isLoading || !url.trim()}
        className="
          h-8 w-8 flex items-center justify-center rounded-lg
          bg-primary text-primary-foreground
          hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors shrink-0
        "
        aria-label="Add URL"
      >
        {isLoading ? (
          <Loader2 className="w-3.5 h-3.5 animate-spin" />
        ) : (
          <Plus className="w-3.5 h-3.5" />
        )}
      </button>
    </form>
  );
}
