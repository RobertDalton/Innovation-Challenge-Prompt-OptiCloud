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
          <span style={{ color: "var(--color-primaryText)" }}>Status:</span>
          <span
            style={{
              color: securityData.safe ? "var(--color-primary)" : "#ff4444",
            }}
            className="font-medium"
          >
            {securityData.safe ? "Safe" : "Unsafe"}
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Original Language:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.original_language
              ? securityData.original_language
              : "Unknown"}
          </span>
        </div>

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Is translated? :
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.translated ? "Yes" : "No"}
          </span>
        </div>

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Cleaned Text:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.cleanedText ? securityData.cleanedText : "No"}
          </span>
        </div>

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Characters Removed:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.charactersRemoved
              ? securityData.charactersRemoved
              : 0}
          </span>
        </div>

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Personal Information Detected?:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.pii_detected ? "Yes" : "No"}
          </span>
        </div>
        {securityData.pii_detected ? (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg">
            <p className="font-semibold">Clear the next information:</p>
            <ul className="list-disc pl-5">
              {securityData.pii_results.entities.map((e, index) => (
                <li key={index} className="text-sm font-medium">
                  {e.text}
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Hate Severity:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.contentSafetyResults?.hateSeverity ?? 0}
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Self Harm Severity:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.contentSafetyResults?.selfHarmSeverity ?? 0}
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Sexual Severity:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.contentSafetyResults?.sexualSeverity ?? 0}
          </span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Violence Severity:
          </span>
          <span
            style={{ color: "var(--color-primaryText)" }}
            className="font-medium"
          >
            {securityData.contentSafetyResults?.violenceSeverity ?? 0}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SecurityStats;
