import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import type { ChatMessage } from "@/types";
import { SourceCard } from "./SourceCard";

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      <div
        className={`
          w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5
          ${isUser ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}
        `}
      >
        {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
      </div>

      <div className={`flex flex-col gap-2 max-w-[75%] ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`
            px-4 py-2.5 rounded-2xl text-sm leading-relaxed
            ${isUser
              ? "bg-primary text-primary-foreground rounded-tr-sm"
              : "bg-muted text-foreground rounded-tl-sm"
            }
          `}
        >
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-1 last:mb-0">{children}</p>,
                code: ({ children }) => (
                  <code className="font-mono text-xs bg-black/10 rounded px-1 py-0.5">
                    {children}
                  </code>
                ),
                pre: ({ children }) => (
                  <pre className="font-mono text-xs bg-black/10 rounded p-2 mt-1 overflow-x-auto">
                    {children}
                  </pre>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="flex flex-col gap-1.5 w-full">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-muted-foreground px-1">
              Sources
            </p>
            {message.sources.map((source, i) => (
              <SourceCard key={source.source_id} source={source} index={i + 1} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
