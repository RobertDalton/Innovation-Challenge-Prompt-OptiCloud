import { useRef, useEffect, useState } from 'react';
import '../styles/colors.css';

const ChatInput = ({ inputMessage, setInputMessage, onSendMessage, onGiberlinkModeChange }) => {
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [isGiberlinkMode, setIsGiberlinkMode] = useState(false);
  const textareaRef = useRef(null);

  // Auto-resize textarea as content grows
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '44px'; // Reset height
      const scrollHeight = textareaRef.current.scrollHeight;
      // Limit maximum height to 100px
      textareaRef.current.style.height = Math.min(scrollHeight, 100) + 'px';
    }
  }, [inputMessage]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSendMessage(e);
    }
  };

  const toggleVoiceMode = () => {
    setIsVoiceMode(!isVoiceMode);
    setIsGiberlinkMode(false);
    onGiberlinkModeChange(false);
  };

  const toggleGiberlinkMode = () => {
    const newMode = !isGiberlinkMode;
    setIsGiberlinkMode(newMode);
    setIsVoiceMode(false);
    onGiberlinkModeChange(newMode);
  };

  return (
    <div style={{
      backgroundColor: 'var(--color-secondaryBackground)',
      borderColor: 'var(--color-element)'
    }} className="fixed bottom-0 left-0 right-0 border-t shadow-lg">
      <div className="max-w-3xl mx-auto p-4">
        <form onSubmit={onSendMessage}>
          <div className="flex gap-3 items-center">
            {/* Mode toggle buttons */}
            <button
              type="button"
              onClick={toggleVoiceMode}
              style={{ 
                backgroundColor: isVoiceMode ? 'var(--color-primary)' : 'var(--color-element)',
                color: 'var(--color-primaryText)'
              }}
              className={`p-2 rounded-lg transition-colors hover:opacity-90`}
              title="Voice Mode"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
            <button
              type="button"
              onClick={toggleGiberlinkMode}
              style={{ 
                backgroundColor: isGiberlinkMode ? 'var(--color-primary)' : 'var(--color-element)',
                color: 'var(--color-primaryText)'
              }}
              className={`p-2 rounded-lg transition-colors hover:opacity-90`}
              title="Giberlink Mode"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
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
                  : isGiberlinkMode 
                    ? "Giberlink mode enabled - Enter your link" 
                    : "Type your message..."
              }
              style={{
                backgroundColor: 'var(--color-element)',
                color: 'var(--color-primaryText)',
                borderColor: 'var(--color-element)',
                scrollbarColor: 'var(--color-secondaryText) var(--color-element)'
              }}
              className="flex-1 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary 
                resize-none min-h-[44px] max-h-[100px] overflow-y-auto
                scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
            />

            {/* Send button */}
            <button
              type="submit"
              style={{ 
                backgroundColor: 'var(--color-primary)',
                color: 'var(--color-primaryText)'
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