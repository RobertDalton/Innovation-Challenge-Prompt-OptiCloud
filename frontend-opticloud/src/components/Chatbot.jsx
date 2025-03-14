import { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim() === '') return;

    setMessages([...messages, { text: inputMessage, sender: 'user' }]);
    setInputMessage('');

    // Simulate bot response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "Thanks for your message! I'm a demo chatbot.", 
        sender: 'bot' 
      }]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-900">
      {/* Messages area with padding bottom to account for fixed input */}
      <div className="flex-1 overflow-y-auto pb-24">
        <div className="max-w-3xl mx-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`${
                  message.sender === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-100'
                } rounded-lg p-4 max-w-[80%] shadow-sm`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Fixed input area at bottom */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 shadow-lg">
        <div className="max-w-3xl mx-auto p-4">
          <form onSubmit={handleSendMessage}>
            <div className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 p-3 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 bg-gray-700 text-white placeholder-gray-400"
              />
              <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Send
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chatbot; 