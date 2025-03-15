const MessageBubble = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div 
        className={`${
          isUser 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-700 text-gray-100'
        } rounded-lg p-4 max-w-[80%] shadow-sm break-words whitespace-pre-wrap overflow-hidden`}
      >
        <p className="text-sm sm:text-base">{message.text}</p>
      </div>
    </div>
  );
};

export default MessageBubble; 