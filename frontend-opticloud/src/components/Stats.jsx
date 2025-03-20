import React from "react";
import SpectralStats from "./SpectralStats";
import SecurityStats from "./SecurityStats";

const Stats = ({ spectralData, securityData }) => {
  return (
    <div
      style={{
        backgroundColor: "var(--color-secondaryBackground)",
        borderColor: "var(--color-element)",
      }}
      className="p-4 rounded-lg border mb-4"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SpectralStats spectralData={spectralData} />
        <SecurityStats securityData={securityData} />
      </div>
    </div>
  );
};

export default Stats;
