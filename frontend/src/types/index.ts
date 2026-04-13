export type SourceType = "pdf" | "web" | "markdown";

export interface SourceInfo {
  source_id: string;
  source_type: SourceType;
  label: string;
  chunk_count: number;
}

export interface IngestResponse {
  source_id: string;
  source_type: SourceType;
  chunk_count: number;
  label: string;
}

export interface SourceReference {
  source_id: string;
  label: string;
  source_type: SourceType;
  excerpt: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceReference[];
  isStreaming?: boolean;
}

export interface QueryRequest {
  question: string;
  history: { role: "user" | "assistant"; content: string }[];
  source_ids?: string[] | null;
}

export interface QueryResponse {
  answer: string;
  sources: SourceReference[];
}
