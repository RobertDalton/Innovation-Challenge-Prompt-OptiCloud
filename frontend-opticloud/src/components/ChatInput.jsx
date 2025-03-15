import { useRef, useEffect } from 'react';

const ChatInput = ({ inputMessage, setInputMessage, onSendMessage }) => {
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

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 shadow-lg">
      <div className="max-w-3xl mx-auto p-4">
        <form onSubmit={onSendMessage}>
          <div className="flex gap-3">
            <textarea
              ref={textareaRef}
              rows="1"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="flex-1 p-3 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 bg-gray-700 text-white placeholder-gray-400 resize-none min-h-[44px] max-h-[100px] overflow-y-auto
              scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-700 scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
              style={{
                scrollbarWidth: 'thin',
                scrollbarColor: '#4B5563 #374151'
              }}
            />
            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium h-[44px]"
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