import React from "react";
import SpectralStats from "./SpectralStats";
import GiberlinkVisualizer from "./GiberlinkVisualizer";

const SpectralModeComponent = ({
  isGiberlinkMode,
  spectralData,
  messages,
  isPlaying,
}) => {
  return (
    <div
      className={`
        order-1 md:order-2
        transition-all duration-300 ease-in-out
        flex flex-col
        ${
          isGiberlinkMode
            ? "opacity-100 h-[40vh] md:h-full md:w-1/2 translate-x-0"
            : "opacity-0 h-0 md:w-0 md:translate-x-full"
        }
        border-element
        transform
        bg-gray-800 text-white
      `}
    >
       <h3 className="text-lg font-semibold p-4 text-center">Spectral Shield Mode</h3>
      {/* Spectral Stats - Only show when Giberlink mode is active */}
      {isGiberlinkMode && spectralData && (
        <div className="px-4 pt-4 mb-4 flex-shrink-0">
          <SpectralStats spectralData={spectralData} />
        </div>
      )}

      {/* Giberlink Visualizer */}
      <div className="flex-1 overflow-hidden">
        <GiberlinkVisualizer messages={messages} isPlaying={isPlaying} />
      </div>
    </div>
  );
};

export default SpectralModeComponent;
