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
      {isGiberlinkMode ? (
        <GiberlinkVisualizer messages={messages} />
      ) : (
        <MessageList messages={messages} />
      )}
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