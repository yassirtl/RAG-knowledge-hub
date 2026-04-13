import { FileText, Globe, File, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";
import type { SourceReference } from "@/types";

interface SourceCardProps {
  source: SourceReference;
  index: number;
}

const SOURCE_ICONS = {
  pdf: FileText,
  web: Globe,
  markdown: File,
} as const;

export function SourceCard({ source, index }: SourceCardProps) {
  const [expanded, setExpanded] = useState(false);
  const Icon = SOURCE_ICONS[source.source_type as keyof typeof SOURCE_ICONS] ?? File;
  const scorePercent = Math.round(source.score * 100);

  return (
    <div className="rounded-lg border border-border bg-card/50 text-xs overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center gap-2 px-3 py-2 hover:bg-accent/30 transition-colors text-left"
      >
        <span className="font-mono text-muted-foreground w-4 shrink-0">
          [{index}]
        </span>
        <Icon className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
        <span className="flex-1 font-medium truncate">{source.label}</span>
        <span
          className={`
            shrink-0 font-mono px-1.5 py-0.5 rounded text-[10px] font-semibold
            ${scorePercent >= 75 ? "bg-green-500/10 text-green-600" : ""}
            ${scorePercent >= 50 && scorePercent < 75 ? "bg-yellow-500/10 text-yellow-600" : ""}
            ${scorePercent < 50 ? "bg-red-500/10 text-red-500" : ""}
          `}
        >
          {scorePercent}%
        </span>
        {expanded ? (
          <ChevronUp className="w-3 h-3 text-muted-foreground shrink-0" />
        ) : (
          <ChevronDown className="w-3 h-3 text-muted-foreground shrink-0" />
        )}
      </button>
      {expanded && (
        <div className="px-3 pb-3 pt-1 border-t border-border">
          <p className="text-muted-foreground leading-relaxed line-clamp-4">
            {source.excerpt}
          </p>
        </div>
      )}
    </div>
  );
}
