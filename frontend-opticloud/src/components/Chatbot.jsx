import { useState } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import GiberlinkVisualizer from './GiberlinkVisualizer';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isGiberlinkMode, setIsGiberlinkMode] = useState(false);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim() === '') return;

    setMessages([...messages, { text: inputMessage, sender: 'user' }]);
    setInputMessage('');

    // Simulate bot response
    setTimeout(() => {
      if (isGiberlinkMode) {
        setMessages(prev => [...prev, { 
          text: "Converting signal patterns... Detected frequency variations in ultrasonic range", 
          sender: 'bot' 
        }]);
      } else {
        setMessages(prev => [...prev, { 
          text: "Thanks for your message! I'm a demo chatbot.", 
          sender: 'bot' 
        }]);
      }
    }, 1000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-900">
      <div className="flex-1 flex md:flex-row flex-col overflow-hidden">
        {/* Giberlink Visualizer - shows at top on mobile, right on desktop */}
        <div className={`
          order-1 md:order-2
          transition-all duration-300 ease-in-out
          ${isGiberlinkMode 
            ? 'opacity-100 h-[40vh] md:h-full md:w-1/2 translate-x-0' 
            : 'opacity-0 h-0 md:w-0 md:translate-x-full'}
          md:border-l md:border-gray-700
          transform
        `}>
          <GiberlinkVisualizer messages={messages} />
        </div>

        {/* Message List - below visualizer on mobile, left on desktop */}
        <div className={`
          order-2 md:order-1
          flex-1 transition-all duration-300 ease-in-out relative
          ${isGiberlinkMode ? 'h-[60vh] md:h-full md:w-1/2' : 'h-full md:w-full'}
        `}>
          <MessageList messages={messages} />
        </div>
      </div>

      <ChatInput 
        inputMessage={inputMessage}
        setInputMessage={setInputMessage}
        onSendMessage={handleSendMessage}
        onGiberlinkModeChange={setIsGiberlinkMode}
      />
    </div>
  );
};

export default Chatbot; 