import { useState, useEffect } from 'react';

const GiberlinkVisualizer = ({ messages }) => {
  const [barHeights, setBarHeights] = useState([30, 50, 70, 50, 30]);

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
    <div className="h-full w-full bg-gray-900 border-l border-gray-700 md:animate-slide-in">
      <div className="h-full flex items-center justify-center p-4">
        {latestBotMessage && (
          <div className="flex flex-col items-center space-y-8">
            {/* Sound interpretation text */}
            <div className="text-gray-200 text-xl font-medium text-center">
              {latestBotMessage.text}
            </div>

            {/* Sound visualization bars */}
            <div className="flex items-end justify-center gap-3 h-40 w-full max-w-md">
              {barHeights.map((height, i) => (
                <div
                  key={i}
                  className="w-10 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg transition-all duration-200 ease-in-out"
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