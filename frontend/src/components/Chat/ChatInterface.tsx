import { useEffect, useRef, useState } from "react";
import { Send, Loader2, Trash2 } from "lucide-react";
import type { SourceInfo } from "@/types";
import { MessageBubble } from "./MessageBubble";

interface ChatInterfaceProps {
  messages: ReturnType<typeof import("@/hooks/useChat").useChat>["messages"];
  isLoading: boolean;
  error: string | null;
  sources: SourceInfo[];
  onSend: (question: string, sourceIds?: string[]) => Promise<void>;
  onClear: () => void;
}

export function ChatInterface({
  messages,
  isLoading,
  error,
  sources,
  onSend,
  onClear,
}: ChatInterfaceProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    setInput("");
    await onSend(trimmed);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="flex flex-col flex-1 h-full overflow-hidden">
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-5">
        {isEmpty && (
          <div className="flex flex-col items-center justify-center h-full gap-3 text-center">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Send className="w-5 h-5 text-primary" />
            </div>
            <p className="text-sm font-medium">Ask anything about your knowledge base</p>
            <p className="text-xs text-muted-foreground max-w-xs">
              {sources.length === 0
                ? "Add at least one source from the sidebar to get started."
                : `${sources.length} source${sources.length > 1 ? "s" : ""} loaded. Start typing below.`}
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <div className="w-7 h-7 rounded-full bg-muted flex items-center justify-center shrink-0 mt-0.5">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-muted-foreground" />
            </div>
            <div className="bg-muted px-4 py-2.5 rounded-2xl rounded-tl-sm">
              <div className="flex gap-1 items-center h-5">
                <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:0ms]" />
                <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:150ms]" />
                <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/50 animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
            {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="border-t border-border px-4 py-3 bg-card shrink-0">
        {!isEmpty && (
          <div className="flex justify-end mb-2">
            <button
              onClick={onClear}
              className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              <Trash2 className="w-3 h-3" />
              Clear chat
            </button>
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex gap-2 items-end">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder="Ask a question… (Enter to send, Shift+Enter for newline)"
            disabled={isLoading}
            className="
              flex-1 resize-none rounded-xl border border-border bg-background
              px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground
              focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
              disabled:opacity-50 min-h-[42px] max-h-32
            "
            style={{ height: "auto" }}
            onInput={(e) => {
              const el = e.currentTarget;
              el.style.height = "auto";
              el.style.height = `${Math.min(el.scrollHeight, 128)}px`;
            }}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="
              h-[42px] w-[42px] flex items-center justify-center rounded-xl
              bg-primary text-primary-foreground
              hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed
              transition-colors shrink-0
            "
            aria-label="Send message"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
