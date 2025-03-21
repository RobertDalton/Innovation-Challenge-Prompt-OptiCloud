import React from "react";

const SecurityStats = ({ securityData }) => {
  if (!securityData) return null;

  return (
    <div className="space-y-2">
      <h3
        style={{ color: "var(--color-primary)" }}
        className="text-lg font-medium mb-2"
      >
        Security Check
      </h3>

      <div className="space-y-1">
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Status:
          </span>
          <span
            style={{
              color: securityData.safe
                ? "var(--color-primary)"
                : "#ff4444",
            }}
            className="font-medium"
          >
            {securityData.safe ? "Safe" : "Unsafe"}
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            PII Detected:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.pii_detected ? "Yes" : "No"}
          </span>
        </div>
        {securityData.translated && (
          <div className="flex justify-between">
            <span style={{ color: "var(--color-primaryText)" }}>
              Original Language:
            </span>
            <span
              style={{ color: "var(--color-primaryText)" }}
              className="font-medium"
            >
              {securityData.original_language}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default SecurityStats;