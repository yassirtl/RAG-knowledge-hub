import { useState } from "react";
import { api } from "@/lib/api";
import type { ChatMessage } from "@/types";

export interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (question: string, sourceIds?: string[]) => Promise<void>;
  clearMessages: () => void;
  clearError: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (question: string, sourceIds?: string[]) => {
    const userMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    const history = messages.map(({ role, content }) => ({ role, content }));

    try {
      const response = await api.query.ask({
        question,
        history,
        source_ids: sourceIds ?? null,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Query failed. Please retry.";
      setError(msg);
      setMessages((prev) => prev.filter((m) => m !== userMessage));
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages: () => setMessages([]),
    clearError: () => setError(null),
  };
}
