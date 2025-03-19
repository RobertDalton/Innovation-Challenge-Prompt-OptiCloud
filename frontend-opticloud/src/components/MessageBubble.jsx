import '../styles/colors.css';

const MessageBubble = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div 
        style={{ 
          backgroundColor: isUser ? 'var(--color-primary)' : 'var(--color-element)',
          color: 'var(--color-primaryText)'
        }}
        className="rounded-lg p-4 max-w-[80%] shadow-sm break-words whitespace-pre-wrap overflow-hidden"
      >
        <p className="text-sm sm:text-base">{message.text}</p>
      </div>
    </div>
  );
};

export default MessageBubble;