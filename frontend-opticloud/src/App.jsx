import { useState, useEffect } from "react";
import Chatbot from "./components/Chatbot";
import Header from "./components/Header";
import GgWaveExample from "./components/AudioListener";
import "./App.css";

const App = () => {
  const [colorMode, setColorMode] = useState(() => {
    // Initialize from localStorage if available
    return localStorage.getItem("colorblind-mode") || "normal";
  });

  const [isSpeechMode, setIsSpeechMode] = useState(false);

  useEffect(() => {
    // Save to localStorage when mode changes
    localStorage.setItem("colorblind-mode", colorMode);

    // Set the custom properties based on the color mode
    const root = document.documentElement;
    if (colorMode === "normal") {
      root.style.setProperty("--color-primary", "#51a2ff"); // Blue
      root.style.setProperty("--color-element", "#364153"); // Gray
      root.style.setProperty("--color-primaryText", "#e5e7eb"); // White
      root.style.setProperty("--color-secondaryText", "#99a1af"); // Gray
      root.style.setProperty("--color-primaryBackground", "#101828"); // Dark Blue
      root.style.setProperty("--color-secondaryBackground", "#1e2939"); // Gray Blue
    } else if (colorMode === "deuteranopia") {
      // Set colors for Deuteranopia mode
      root.style.setProperty("--color-primary", "#51a2ff"); // Adjusted color for deuteranopia
      root.style.setProperty("--color-element", "#364153"); // Adjusted color for deuteranopia
      root.style.setProperty("--color-primaryText", "#ffffff");
      root.style.setProperty("--color-secondaryText", "#d1d5db");
      root.style.setProperty("--color-primaryBackground", "#1c1f25");
      root.style.setProperty("--color-secondaryBackground", "#293744");
    } else if (colorMode === "protanopia") {
      // Set colors for Protanopia mode
      root.style.setProperty("--color-primary", "#8c54e0"); // Adjusted color for protanopia
      root.style.setProperty("--color-element", "#6f7376");
      root.style.setProperty("--color-primaryText", "#ffffff");
      root.style.setProperty("--color-secondaryText", "#b1b5ba");
      root.style.setProperty("--color-primaryBackground", "#171c1f");
      root.style.setProperty("--color-secondaryBackground", "#2b353f");
    } else if (colorMode === "tritanopia") {
      // Set colors for Tritanopia mode
      root.style.setProperty("--color-primary", "#72a7c7"); // Adjusted color for tritanopia
      root.style.setProperty("--color-element", "#5c6469");
      root.style.setProperty("--color-primaryText", "#ffffff");
      root.style.setProperty("--color-secondaryText", "#a1abb2");
      root.style.setProperty("--color-primaryBackground", "#121c21");
      root.style.setProperty("--color-secondaryBackground", "#27313d");
    }
  }, [colorMode]);

  return (
    <div className="min-h-screen flex flex-col">
      <Header 
        setColorMode={setColorMode} 
        currentMode={colorMode} 
        onSpeechModeChange={setIsSpeechMode}
      />
      <main className="flex-1 pt-16">
        <Chatbot isSpeechMode={isSpeechMode} />
      </main>
    </div>
  );
}

export default App;
