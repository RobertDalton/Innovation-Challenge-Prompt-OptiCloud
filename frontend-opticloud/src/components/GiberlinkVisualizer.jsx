import { useState, useEffect } from 'react';

const GiberlinkVisualizer = ({ messages }) => {
  const [barHeights, setBarHeights] = useState([30, 50, 70, 50, 30, 20]);

  // Get the latest bot message
  const latestBotMessage = messages.length > 0 
    ? messages.filter(msg => msg.sender === 'bot').pop()
    : null;

  // Simulate sound animation
  useEffect(() => {
    const interval = setInterval(() => {
      setBarHeights(prevHeights => 
        prevHeights.map(() => Math.random() * 100)
      );
    }, 200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex-1 overflow-y-auto pb-24 scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-800 scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
      style={{
        scrollbarWidth: 'thin',
        scrollbarColor: '#4B5563 #1F2937'
      }}>
      <div className="max-w-3xl mx-auto p-4 h-full flex items-center justify-center">
        {latestBotMessage && (
          <div className="flex flex-col items-center space-y-8">
            {/* Sound interpretation text */}
            <div className="text-gray-200 text-xl font-medium text-center">
              {latestBotMessage.text}
            </div>

            {/* Sound visualization bars */}
            <div className="flex items-end justify-center gap-1 h-40 w-full max-w-md">
              {barHeights.map((height, i) => (
                <div
                  key={i}
                  className="w-8 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg transition-all duration-200 ease-in-out"
                  style={{ height: `${height}%` }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GiberlinkVisualizer; 