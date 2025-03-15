import MessageBubble from './MessageBubble';

const MessageList = ({ messages }) => {
  return (
    <div className="flex-1 overflow-y-auto pb-24 scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-800 scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
      style={{
        scrollbarWidth: 'thin',
        scrollbarColor: '#4B5563 #1F2937'
      }}>
      <div className="max-w-3xl mx-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
      </div>
    </div>
  );
};

export default MessageList; 