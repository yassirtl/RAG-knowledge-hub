import axios from "axios";
import type { IngestResponse, QueryRequest, QueryResponse } from "@/types";

const http = axios.create({
  baseURL: "/api/v1",
  timeout: 60_000,
});

export const api = {
  ingest: {
    pdf: (file: File, label?: string): Promise<IngestResponse> => {
      const form = new FormData();
      form.append("file", file);
      if (label) form.append("label", label);
      return http.post<IngestResponse>("/ingest/pdf", form).then((r) => r.data);
    },

    url: (url: string, sourceLabel?: string): Promise<IngestResponse> =>
      http
        .post<IngestResponse>("/ingest/url", { url, source_label: sourceLabel })
        .then((r) => r.data),

    file: (file: File, label?: string): Promise<IngestResponse> => {
      const form = new FormData();
      form.append("file", file);
      if (label) form.append("label", label);
      return http
        .post<IngestResponse>("/ingest/file", form)
        .then((r) => r.data);
    },

    deleteSource: (sourceId: string): Promise<void> =>
      http.delete("/ingest/source", { data: { source_id: sourceId } }),

    getChunkCount: (
      sourceId: string
    ): Promise<{ source_id: string; chunk_count: number }> =>
      http
        .get<{ source_id: string; chunk_count: number }>(
          `/ingest/source/${sourceId}/chunks`
        )
        .then((r) => r.data),
  },

  query: {
    ask: (payload: QueryRequest): Promise<QueryResponse> =>
      http.post<QueryResponse>("/query/", payload).then((r) => r.data),
  },

  health: (): Promise<{ status: string; version: string }> =>
    http.get("/health").then((r) => r.data),
};
