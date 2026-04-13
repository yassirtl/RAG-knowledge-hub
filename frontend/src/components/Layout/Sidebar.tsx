import { FileText, Globe, File, Trash2, Database } from "lucide-react";
import type { SourceInfo } from "@/types";
import { FileUpload } from "@/components/Ingestion/FileUpload";
import { UrlInput } from "@/components/Ingestion/UrlInput";

interface SidebarProps {
  sources: SourceInfo[];
  isLoading: boolean;
  onIngestPdf: (file: File, label?: string) => Promise<void>;
  onIngestUrl: (url: string, label?: string) => Promise<void>;
  onIngestFile: (file: File, label?: string) => Promise<void>;
  onDeleteSource: (sourceId: string) => Promise<void>;
}

const SOURCE_ICONS: Record<string, React.ElementType> = {
  pdf: FileText,
  web: Globe,
  markdown: File,
};

export function Sidebar({
  sources,
  isLoading,
  onIngestPdf,
  onIngestUrl,
  onIngestFile,
  onDeleteSource,
}: SidebarProps) {
  return (
    <aside className="flex flex-col w-72 shrink-0 border-r border-border bg-card h-full overflow-hidden">
      <div className="p-4 border-b border-border">
        <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-3">
          Add Sources
        </p>
        <div className="flex flex-col gap-3">
          <FileUpload
            accept=".pdf"
            label="Upload PDF"
            onUpload={onIngestPdf}
            isLoading={isLoading}
          />
          <FileUpload
            accept=".md,.txt"
            label="Upload Markdown / Text"
            onUpload={onIngestFile}
            isLoading={isLoading}
          />
          <UrlInput onSubmit={onIngestUrl} isLoading={isLoading} />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex items-center gap-1.5 mb-3">
          <Database className="w-3.5 h-3.5 text-muted-foreground" />
          <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
            Knowledge Base
          </p>
          {sources.length > 0 && (
            <span className="ml-auto text-xs bg-primary/10 text-primary font-medium px-1.5 py-0.5 rounded-full">
              {sources.length}
            </span>
          )}
        </div>

        {sources.length === 0 ? (
          <p className="text-xs text-muted-foreground text-center py-8">
            No sources yet. Add a PDF, URL, or Markdown file to get started.
          </p>
        ) : (
          <ul className="flex flex-col gap-2">
            {sources.map((source) => {
              const Icon = SOURCE_ICONS[source.source_type] ?? File;
              return (
                <li
                  key={source.source_id}
                  className="flex items-start gap-2 group rounded-lg p-2 hover:bg-accent/50 transition-colors"
                >
                  <Icon className="w-4 h-4 text-muted-foreground mt-0.5 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{source.label}</p>
                    <p className="text-xs text-muted-foreground">
                      {source.chunk_count} chunks &middot;{" "}
                      <span className="capitalize">{source.source_type}</span>
                    </p>
                  </div>
                  <button
                    onClick={() => onDeleteSource(source.source_id)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-destructive p-1 rounded"
                    aria-label={`Delete ${source.label}`}
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </aside>
  );
}
