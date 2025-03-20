import React from "react";
import SecurityStats from "./SecurityStats";
import GiberlinkVisualizer from "./GiberlinkVisualizer";

const SecurityPipelineComponent = ({
  isSecurityPipelineMode,
  securityData,
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
          isSecurityPipelineMode
            ? "opacity-100 h-[40vh] md:h-full md:w-1/2 translate-x-0"
            : "opacity-0 h-0 md:w-0 md:translate-x-full"
        }
        border-element
        transform
        bg-gray-800 text-white
      `}
    >
      <h3 className="text-lg font-semibold p-4">Security Pipeline Mode</h3>
      {/* Security Stats - Only show when Security Pipeline mode is active */}
      {isSecurityPipelineMode && securityData && (
        <div className="px-4 pt-4 mb-4 flex-shrink-0">
          <SecurityStats securityData={securityData} />
        </div>
      )}

      {/* Giberlink Visualizer */}
      <div className="flex-1 overflow-hidden">
        <GiberlinkVisualizer messages={messages} isPlaying={isPlaying} />
      </div>
    </div>
  );
};

export default SecurityPipelineComponent;
