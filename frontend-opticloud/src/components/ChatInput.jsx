import { useRef, useEffect, useState } from "react";
import "../styles/colors.css";

const ChatInput = ({
  inputMessage,
  setInputMessage,
  onSendMessage,
  onGiberlinkModeChange,
  onSecurityPipelineChange,
}) => {
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [isGiberlinkMode, setIsGiberlinkMode] = useState(false);
  const [isSecurityPipelineMode, setIsSecurityPipelineMode] = useState(false);
  const textareaRef = useRef(null);

  // Auto-resize textarea as content grows
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "44px"; // Reset height
      const scrollHeight = textareaRef.current.scrollHeight;
      // Limit maximum height to 100px
      textareaRef.current.style.height = Math.min(scrollHeight, 100) + "px";
    }
  }, [inputMessage]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSendMessage(e);
    }
  };

  const toggleVoiceMode = () => {
    setIsVoiceMode(!isVoiceMode);
    setIsSecurityPipelineMode(false);
    setIsGiberlinkMode(false);
    onGiberlinkModeChange(false);
    onSecurityPipelineChange(false);
  };

  const toggleGiberlinkMode = () => {
    const newMode = !isGiberlinkMode;
    setIsVoiceMode(false);
    setIsSecurityPipelineMode(false);
    setIsGiberlinkMode(newMode);
    onGiberlinkModeChange(newMode);
  };

  const toggleSecurityPipelineMode = () => {
    const newMode = !isSecurityPipelineMode;
    setIsVoiceMode(false);
    setIsSecurityPipelineMode(newMode);
    setIsGiberlinkMode(false);
    onSecurityPipelineChange(newMode);
  };

  return (
    <div
      style={{
        backgroundColor: "var(--color-secondaryBackground)",
        borderColor: "var(--color-element)",
      }}
      className="fixed bottom-0 left-0 right-0 border-t shadow-lg"
    >
      <div className="max-w-3xl mx-auto p-4">
        <form onSubmit={onSendMessage}>
          <div className="flex gap-3 items-center">
            {/* Mode toggle buttons */}
            <button
              type="button"
              onClick={toggleVoiceMode}
              style={{
                backgroundColor: isVoiceMode
                  ? "var(--color-primary)"
                  : "var(--color-element)",
                color: "var(--color-primaryText)",
              }}
              className="cursor-pointer px-4 py-2 rounded-lg transition-colors hover:opacity-90 text-sm font-medium whitespace-nowrap"
              title="Voice Mode"
            >
              Voice Mode
            </button>

            <button
              type="button"
              onClick={toggleGiberlinkMode}
              style={{
                backgroundColor: isGiberlinkMode
                  ? "var(--color-primary)"
                  : "var(--color-element)",
                color: "var(--color-primaryText)",
              }}
              className="cursor-pointer px-4 py-2 rounded-lg transition-colors hover:opacity-90 text-sm font-medium whitespace-nowrap"
              title="Spectral Shield Analysis"
            >
              Spectral Shield
            </button>

            <button
              type="button"
              onClick={toggleSecurityPipelineMode}
              style={{
                backgroundColor: isSecurityPipelineMode
                  ? "var(--color-primary)"
                  : "var(--color-element)",
                color: "var(--color-primaryText)",
              }}
              className="cursor-pointer px-4 py-2 rounded-lg transition-colors hover:opacity-90 text-sm font-medium whitespace-nowrap"
              title="Security Pipeline Analysis"
            >
              Security Pipeline
            </button>

            {/* Textarea */}
            <textarea
              ref={textareaRef}
              rows="1"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                isVoiceMode
                  ? "Voice mode enabled - Click to speak"
                  : "Type your message..."
              }
              style={{
                backgroundColor: "var(--color-element)",
                color: "var(--color-primaryText)",
                borderColor: "var(--color-element)",
                scrollbarColor:
                  "var(--color-secondaryText) var(--color-element)",
              }}
              className="flex-1 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary 
                resize-none min-h-[44px] max-h-[100px] overflow-y-auto
                scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
            />

            {/* Send button */}
            <button
              type="submit"
              style={{
                backgroundColor: "var(--color-primary)",
                color: "var(--color-primaryText)",
              }}
              className="px-6 py-3 rounded-lg hover:opacity-90 transition-colors font-medium h-[44px]"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatInput;
