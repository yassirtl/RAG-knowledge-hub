import { useRef, useState } from "react";
import { Upload, Loader2 } from "lucide-react";

interface FileUploadProps {
  accept: string;
  label: string;
  onUpload: (file: File, label?: string) => Promise<void>;
  isLoading: boolean;
}

export function FileUpload({
  accept,
  label,
  onUpload,
  isLoading,
}: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = async (file: File) => {
    await onUpload(file);
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => !isLoading && inputRef.current?.click()}
      onKeyDown={(e) => e.key === "Enter" && !isLoading && inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={`
        flex items-center gap-2 px-3 py-2 rounded-lg border border-dashed text-xs
        cursor-pointer transition-colors select-none
        ${isDragging
          ? "border-primary bg-primary/5 text-primary"
          : "border-border text-muted-foreground hover:border-primary/50 hover:text-foreground"
        }
        ${isLoading ? "opacity-50 pointer-events-none" : ""}
      `}
    >
      {isLoading ? (
        <Loader2 className="w-3.5 h-3.5 animate-spin shrink-0" />
      ) : (
        <Upload className="w-3.5 h-3.5 shrink-0" />
      )}
      <span>{label}</span>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={handleChange}
        disabled={isLoading}
      />
    </div>
  );
}
