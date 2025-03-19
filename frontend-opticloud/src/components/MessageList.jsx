import MessageBubble from './MessageBubble';
import '../styles/colors.css';

const MessageList = ({ messages }) => (
  <div 
    style={{
      scrollbarColor: 'var(--color-element) var(--color-primaryBackground)',
      scrollbarWidth: 'thin'
    }}
    className="h-full p-4 pb-25 overflow-y-auto max-w-7xl
      scrollbar-thin scrollbar-thumb-rounded-full scrollbar-track-rounded-full
      hover:scrollbar-thumb-element scrollbar-track-primary-bg"
  >
    {messages.map((message, index) => (
      <div
        key={index}
        className={`mb-4 ${message.sender === 'user' ? 'text-right' : 'text-left'}`}
      >
        <MessageBubble message={message} />
      </div>
    ))}
  </div>
);

export default MessageList;