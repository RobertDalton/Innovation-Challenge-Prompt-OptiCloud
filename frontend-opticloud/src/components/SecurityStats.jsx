import React from "react";

const SecurityStats = ({ securityData }) => {
  if (!securityData) return null;

  return (
    <div className="space-y-4">
      <h3
        style={{ color: "var(--color-primary)" }}
        className="text-lg font-semibold mb-4"
      >
        Security Check
      </h3>

      <div className="space-y-3">
        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>Status:</span>
          <span
            style={{
              color: securityData.safe ? "#03bf4d" : "#ff4444",
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

        {securityData.pii_detected && (
          <div
            className="border-l-4 border-red-500 p-4 rounded-lg shadow-md"
            style={{
              backgroundColor: "var(--color-primaryBackground)",
              color: "var(--color-primaryText)",
              borderColor: "var(--color-primary)",
            }}
          >
            <p className="font-semibold">
              Found the next personal information:
            </p>
            <ul className="list-disc pl-5">
              {securityData.pii_results.entities.map((e, index) => (
                <li key={index} className="text-sm font-medium">
                  {e.text}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-4">
          <h3 className="pb-2" style={{ color: "var(--color-primaryText)" }}>
            Content Safety Results:
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              {
                label: "Hate Severity",
                value: securityData.content_safety_results?.hate_severity ?? 0,
              },
              {
                label: "Self Harm Severity",
                value:
                  securityData.content_safety_results?.self_harm_severity ?? 0,
              },
              {
                label: "Sexual Severity",
                value:
                  securityData.content_safety_results?.sexual_severity ?? 0,
              },
              {
                label: "Violence Severity",
                value:
                  securityData.content_safety_results?.violence_severity ?? 0,
              },
            ].map((item, index) => (
              <div
                key={index}
                className="bg-gray-100 p-4 rounded-lg shadow-md"
                style={{
                  backgroundColor: "var(--color-primaryBackground)",
                }}
              >
                <div className="flex justify-between items-center">
                  <span
                    className="font-medium"
                    style={{ color: "var(--color-primaryText)" }}
                  >
                    {item.label}:
                  </span>
                  <span
                    className={`font-semibold ${
                      item.value > 3 ? "text-red-500" : "text-green-500"
                    }`}
                  >
                    {item.value}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-between">
          <span style={{ color: "var(--color-primaryText)" }}>
            Attack Detected:
          </span>
          <span
            style={
              securityData.prompt_shield_results.userPromptAnalysis
                .attackDetected
                ? { color: "#ff4444" }
                : { color: "#03bf4d" }
            }
            className="font-medium text-green-500"
          >
            {securityData.prompt_shield_results.userPromptAnalysis
              .attackDetected
              ? "Yes"
              : "No"}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SecurityStats;
