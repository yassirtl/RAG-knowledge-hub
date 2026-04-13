import { useChat } from "@/hooks/useChat";
import { useIngest } from "@/hooks/useIngest";
import { Header } from "@/components/Layout/Header";
import { Sidebar } from "@/components/Layout/Sidebar";
import { ChatInterface } from "@/components/Chat/ChatInterface";

export default function App() {
  const {
    sources,
    isLoading: ingestLoading,
    error: ingestError,
    ingestPdf,
    ingestUrl,
    ingestFile,
    deleteSource,
    clearError: clearIngestError,
  } = useIngest();

  const {
    messages,
    isLoading: chatLoading,
    error: chatError,
    sendMessage,
    clearMessages,
    clearError: clearChatError,
  } = useChat();

  const combinedError = ingestError || chatError;
  if (combinedError) {
    setTimeout(() => {
      clearIngestError();
      clearChatError();
    }, 5000);
  }

  return (
    <div className="flex flex-col h-screen bg-background overflow-hidden">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          sources={sources}
          isLoading={ingestLoading}
          onIngestPdf={ingestPdf}
          onIngestUrl={ingestUrl}
          onIngestFile={ingestFile}
          onDeleteSource={deleteSource}
        />
        <main className="flex-1 overflow-hidden">
          <ChatInterface
            messages={messages}
            isLoading={chatLoading}
            error={combinedError}
            sources={sources}
            onSend={sendMessage}
            onClear={clearMessages}
          />
        </main>
      </div>
    </div>
  );
}
