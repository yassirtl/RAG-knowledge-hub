import { useState } from "react";
import { api } from "@/lib/api";
import type { IngestResponse, SourceInfo, SourceType } from "@/types";

export interface UseIngestReturn {
  sources: SourceInfo[];
  isLoading: boolean;
  error: string | null;
  ingestPdf: (file: File, label?: string) => Promise<void>;
  ingestUrl: (url: string, label?: string) => Promise<void>;
  ingestFile: (file: File, label?: string) => Promise<void>;
  deleteSource: (sourceId: string) => Promise<void>;
  clearError: () => void;
}

function responseToSourceInfo(r: IngestResponse): SourceInfo {
  return {
    source_id: r.source_id,
    source_type: r.source_type as SourceType,
    label: r.label,
    chunk_count: r.chunk_count,
  };
}

export function useIngest(): UseIngestReturn {
  const [sources, setSources] = useState<SourceInfo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleIngest = async (ingestFn: () => Promise<IngestResponse>) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await ingestFn();
      setSources((prev) => {
        const exists = prev.some((s) => s.source_id === result.source_id);
        if (exists) return prev;
        return [...prev, responseToSourceInfo(result)];
      });
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Ingestion failed. Please retry.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const ingestPdf = (file: File, label?: string) =>
    handleIngest(() => api.ingest.pdf(file, label));

  const ingestUrl = (url: string, label?: string) =>
    handleIngest(() => api.ingest.url(url, label));

  const ingestFile = (file: File, label?: string) =>
    handleIngest(() => api.ingest.file(file, label));

  const deleteSource = async (sourceId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.ingest.deleteSource(sourceId);
      setSources((prev) => prev.filter((s) => s.source_id !== sourceId));
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Deletion failed. Please retry.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    sources,
    isLoading,
    error,
    ingestPdf,
    ingestUrl,
    ingestFile,
    deleteSource,
    clearError: () => setError(null),
  };
}
