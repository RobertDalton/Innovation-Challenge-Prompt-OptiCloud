import { useState } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import GiberlinkVisualizer from './GiberlinkVisualizer';
import VoiceBox from './VoiceBox';
import audioService from '../services/audioService';
import '../styles/colors.css';

const Chatbot = ({isSpeechMode}) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isGiberlinkMode, setIsGiberlinkMode] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  // const [isSpeechMode, setIsSpeechMode] = useState(false);

  const handleSendMessage = async (e, message) => {
    e.preventDefault();
    const msg = message || inputMessage;
    if (msg.trim() === '') return;

    setMessages([...messages, { text: msg, sender: 'user' }]);
    
    if (isGiberlinkMode) {
      try {
        setIsPlaying(true);
        const { durationMs, promise } = await audioService.sendAudio(msg);
        
        setMessages(prev => [...prev, { 
          text: "Converting signal patterns... Transmitting via audio frequencies", 
          sender: 'bot' 
        }]);

        // Wait for audio to complete playing
        await promise;
        setIsPlaying(false);

      } catch (error) {
        console.error('Audio transmission failed:', error);
        setIsPlaying(false);
        setMessages(prev => [...prev, { 
          text: "Failed to transmit audio signal. Please try again.", 
          sender: 'bot' 
        }]);
      }
    } else {
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          text: "Thanks for your message! I'm a demo chatbot.", 
          sender: 'bot' 
        }]);
      }, 1000);
    }

    setInputMessage('');
  };

  const handleVoiceResult = (text) => {
    if (text) {
      setMessages(prev => [...prev, { text, sender: 'user' }]);
      // Process the voice input as a regular message
      handleSendMessage(new Event('submit'), text);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-primary-bg">
      {!isSpeechMode ? (
        <>
          <div className="flex-1 flex md:flex-row flex-col overflow-hidden">
            {/* Giberlink Visualizer */}
            <div className={`
              order-1 md:order-2
              transition-all duration-300 ease-in-out
              ${isGiberlinkMode 
                ? 'opacity-100 h-[40vh] md:h-full md:w-1/2 translate-x-0' 
                : 'opacity-0 h-0 md:w-0 md:translate-x-full'}
              border-element
              transform
            `}>
              <GiberlinkVisualizer 
                messages={messages} 
                isPlaying={isPlaying}
              />
            </div>
            {/* Message list container - Fixed width and scroll issues */}
            <div className={`
              order-2 md:order-1
              flex-1 transition-all duration-300 ease-in-out relative bg-primary-bg
              ${isGiberlinkMode ? 'h-[60vh] md:h-full md:w-1/2' : 'h-full md:w-full'}
            `}>
              <div className="h-full flex justify-center">
                <div className="w-full max-w-3xl px-4 overflow-hidden">
                  <MessageList messages={messages} />
                </div>
              </div>
            </div>
          </div>

          <ChatInput 
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            onSendMessage={handleSendMessage}
            onGiberlinkModeChange={setIsGiberlinkMode}
          />
        </>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center">
          <MessageList messages={messages} />
          <VoiceBox 
            isActive={isSpeechMode}
            onVoiceResult={handleVoiceResult}
          />
        </div>
      )}
    </div>
  );
};

export default Chatbot;