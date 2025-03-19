import { useState, useEffect } from "react";
import audioService from "../services/audioService";

export default function GgWaveExample() {
  const [txData, setTxData] = useState("Hello React");
  const [rxData, setRxData] = useState("");
  const [listening, setListening] = useState(false);
  const [audioMeaning, setAudioMeaning] = useState("");

  useEffect(() => {
    // Check if GGWave is available
    if (typeof window.ggwave_factory === 'undefined') {
      console.error('GGWave library not loaded');
    }
  }, []);

  const onSend = async () => {
    if (listening) {
      audioService.stopListening();
    }
    await audioService.sendAudio(txData);
  };

  const startCapture = async () => {
    const success = await audioService.startListening((text) => {
      setRxData(text);
    });
    if (success) {
      setListening(true);
    }
  };

  const stopCapture = () => {
    const success = audioService.stopListening();
    if (success) {
      setListening(false);
    }
  };

  const playAudioSample = async () => {
    try {
      setListening(true);
      const audio = new Audio('/audioWaveSample.mp3');

      const response = await fetch('/audioWaveSample.mp3');
      const blob = await response.blob();
      const audioFile = new File([blob], 'audioWaveSample.mp3', { type: 'audio/mp3' });

      setAudioMeaning("Listening for encoded message...");

      audio.onplay = () => {
        setTimeout(async () => {
          try {
            const decodedText = await audioService.decodeAudioFile(audioFile);
            if (decodedText) {
              setAudioMeaning(decodedText);
            } else {
              setAudioMeaning("No encoded message found in audio");
            }
          } catch (decodeError) {
            console.error('Failed to decode audio:', decodeError);
            setAudioMeaning("Failed to decode audio message");
          }
        }, 3000);
      };

      audio.onended = () => {
        setListening(false);
      };

      await audio.play();
    } catch (error) {
      console.error('Failed to play audio:', error);
      setListening(false);
      setAudioMeaning("Failed to play audio file");
    }
  };

  return (
    <div className="p-4 my-20 max-w-lg mx-auto bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold mb-4">GgWave React Example</h2>
      <div>
        <label className="block mb-2">Tx Data:</label>
        <textarea
          className="w-full p-2 border rounded"
          value={txData}
          onChange={(e) => setTxData(e.target.value)}
        />
      </div>
      <button 
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded cursor-pointer" 
        onClick={onSend}
      >
        Send
      </button>
      {/* <div className="mt-4">
        <label className="block mb-2">Rx Data:</label>
        <textarea 
          className="w-full p-2 border rounded" 
          value={rxData} 
          disabled 
        />
      </div>
      <button
        className={`mt-2 px-4 py-2 ${listening ? "bg-red-500" : "bg-green-500"} text-white rounded`}
        onClick={listening ? stopCapture : startCapture}
      >
        {listening ? "Stop Capturing" : "Start Capturing"}
      </button> */}
      <div className="mt-4">
        <label className="block mb-2">Audio Interpretation:</label>
        <textarea 
          className="w-full p-2 border rounded bg-gray-50" 
          value={audioMeaning}
          readOnly
          placeholder="Audio meaning will appear here..."
        />
      </div>
      <button
        className={`mt-2 px-4 py-2 ${listening ? "bg-red-500" : "bg-green-500"} text-white rounded`}
        onClick={playAudioSample}
        disabled={listening}
      >
        {listening ? "Playing Audio..." : "Play Sample Audio"}
      </button>
    </div>
  );
}