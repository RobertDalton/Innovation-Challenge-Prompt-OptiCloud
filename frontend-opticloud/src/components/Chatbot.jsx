import { useState } from "react";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import VoiceBox from "./VoiceBox";
import audioService from "../services/audioService";
import fineTunedModelService from "../services/fineTunedModelService";
import textSecurityService from "../services/textSecurityService";
import "../styles/colors.css";
import SpectralModeComponent from "./SpectralModeComponent";
import SecurityPipelineComponent from "./SecurityPipelineComponent";

const Chatbot = ({ isSpeechMode }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isGiberlinkMode, setIsGiberlinkMode] = useState(false);
  const [isSecurityPipelineMode, setIsSecurityPipelineMode] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [spectralData, setSpectralData] = useState(null);
  const [securityData, setSecurityData] = useState(null);

  const checkTextSecurity = async (text) => {
    const securityResult = await textSecurityService.analyzeText(text);
    setSecurityData(securityResult);
    return securityResult.safe;
  };

  const analyzeSpectralData = async (text) => {
    const spectralResult = await spectralShieldService.analyzeText(text);
    setSpectralData(spectralResult);
    return spectralResult;
  };

  const handleSendMessage = async (e, message) => {
    e.preventDefault();
    const msg = message || inputMessage;
    if (msg.trim() === "") return;

    setMessages([...messages, { text: msg, sender: "user" }]);

    if (isGiberlinkMode) {
      try {
        setIsPlaying(true);
        const { durationMs, promise } = await audioService.sendAudio(msg);

        setMessages((prev) => [
          ...prev,
          {
            text: "Converting signal patterns... Transmitting via audio frequencies",
            sender: "bot",
          },
        ]);

        // Wait for audio to complete playing
        await promise;
        setIsPlaying(false);
      } catch (error) {
        console.error("Audio transmission failed:", error);
        setIsPlaying(false);
        setMessages((prev) => [
          ...prev,
          {
            text: "Failed to transmit audio signal. Please try again.",
            sender: "bot",
          },
        ]);
      }
    } else {
      try {
        setMessages((prev) => [
          ...prev,
          {
            text: "Thinking...",
            sender: "bot",
            isTyping: true,
          },
        ]);

        const isSecure = await checkTextSecurity(msg);

        if (isSecure) {
          await analyzeSpectralData(msg);

          const modelResponse = await fineTunedModelService.generateResponse(
            msg
          );

          setMessages((prev) => {
            const filtered = prev.filter((m) => !m.isTyping);
            return [
              ...filtered,
              {
                text: fineTunedModelService.isHighQualityResponse(modelResponse)
                  ? modelResponse.response
                  : "I apologize, but I'm not confident about providing an answer to that.",
                sender: "bot",
                confidence: modelResponse.confidence,
              },
            ];
          });
        } else {
          setMessages((prev) => {
            const filtered = prev.filter((m) => !m.isTyping);
            return [
              ...filtered,
              {
                text: "I apologize, but I cannot process potentially unsafe content.",
                sender: "bot",
                error: true,
              },
            ];
          });
        }
      } catch (error) {
        console.error("Model response failed:", error);
        setMessages((prev) => {
          const filtered = prev.filter((m) => !m.isTyping);
          return [
            ...filtered,
            {
              text: "I apologize, but I'm having trouble processing your request right now.",
              sender: "bot",
              error: true,
            },
          ];
        });
      }
    }

    setInputMessage("");
  };

  const handleVoiceResult = (text) => {
    if (text) {
      setMessages((prev) => [...prev, { text, sender: "user" }]);
      // Process the voice input as a regular message
      handleSendMessage(new Event("submit"), text);
    }
  };
  const handleModeChange = (mode, value) => {
    if (mode === "giberlink") {
      setIsGiberlinkMode(value);
      if (value) {
        setIsSecurityPipelineMode(false);
      }
    } else if (mode === "security") {
      setIsSecurityPipelineMode(value);
      if (value) {
        setIsGiberlinkMode(false);
      }
    }
  };
  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-primary-bg">
      {!isSpeechMode ? (
        <>
          <div className="flex-1 flex md:flex-row flex-col overflow-hidden">
            {isGiberlinkMode ? (
              <SpectralModeComponent
                isGiberlinkMode={isGiberlinkMode}
                spectralData={spectralData}
                messages={messages}
                isPlaying={isPlaying}
              />
            ) : isSecurityPipelineMode ? (
              <SecurityPipelineComponent
                isSecurityPipelineMode={isSecurityPipelineMode}
                securityData={securityData}
                messages={messages}
                isPlaying={isPlaying}
              />
            ) : null}

            {/* Message list container with updated width handling */}
            <div
              className={`
                order-2 md:order-1
                flex-1 transition-all duration-300 ease-in-out relative bg-primary-bg
                ${
                  isGiberlinkMode || isSecurityPipelineMode
                    ? "h-[60vh] md:h-full md:w-1/2"
                    : "h-full md:w-full"
                }
              `}
            >
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
            onGiberlinkModeChange={(value) =>
              handleModeChange("giberlink", value)
            }
            onSecurityPipelineChange={(value) =>
              handleModeChange("security", value)
            }
          />
        </>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center">
          <MessageList messages={messages} />
          <VoiceBox isActive={isSpeechMode} onVoiceResult={handleVoiceResult} />
        </div>
      )}
    </div>
  );
};

export default Chatbot;
