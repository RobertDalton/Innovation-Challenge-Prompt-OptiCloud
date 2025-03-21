import React from "react";

const SpectralStats = ({ spectralData }) => {
  if (!spectralData) return null;

  return (
    <div className="space-y-2">
      <h3
        style={{ color: "var(--color-primary)" }}
        className="text-lg font-medium mb-2"
      >
        Spectral Analysis
      </h3>

      <div className="space-y-1">
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Safe Score:
          </span>
          <span
            style={{
              color: spectralData.safe > 0.5
                ? "var(--color-primary)"
                : "#ff4444",
            }}
            className="font-medium"
          >
            {(spectralData.safe * 100).toFixed(1)}%
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Toxic Score:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {(spectralData.toxic * 100).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default SpectralStats;