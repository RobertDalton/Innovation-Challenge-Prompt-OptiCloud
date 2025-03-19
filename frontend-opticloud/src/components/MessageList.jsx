import MessageBubble from './MessageBubble';

const MessageList = ({ messages }) => (
  <div className="h-full p-4 overflow-y-auto max-w-7xl">
    {messages.map((message, index) => (
      <div
        key={index}
        className={`mb-4 ${message.sender === 'user' ? 'text-right' : 'text-left'}`}
      >
        <div
          style={{ 
            backgroundColor: message.sender === 'user' ? 'var(--color-primary)' : 'var(--color-element)',
            color: 'var(--color-primaryText)'
          }}
          className="inline-block rounded-lg px-4 py-2 max-w-[80%]"
        >
          {message.text}
        </div>
      </div>
    ))}
  </div>
);

export default MessageList;