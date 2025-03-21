"use client";

import React, { useState } from "react";

export default function SampleComponent() {
  const [input, setInput] = useState(""); // Estado para el mensaje del usuario
  const [responseText, setResponseText] = useState(""); // Estado para la respuesta en streaming

  const handleClick = async () => {
    setResponseText(""); // Limpiar respuesta anterior

    if (!input.trim()) {
      alert("Por favor, ingresa un mensaje.");
      return;
    }

    try {
      const response = await fetch(
        "https://opticloud-http-streaming.azurewebsites.net/generate-text",
        {
          method: "POST", // Cambiado a POST para enviar datos
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ prompt: input }), // Enviamos el mensaje del usuario
        }
      );

      if (!response.body) {
        console.error("No response body");
        return;
      }

      const reader = response.body
        .pipeThrough(new TextDecoderStream())
        .getReader();

      let result = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done || !value) break;
        console.log("Received:", value);
        result += value;
        setResponseText(result); // Actualizar estado en tiempo real
      }
    } catch (error) {
      console.error("Error fetching stream:", error);
      setResponseText("Error al obtener respuesta.");
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h3>Streaming Response</h3>

      {/* Textbox para escribir el mensaje */}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Escribe tu mensaje aquí..."
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      />

      {/* Botón para enviar */}
      <button
        onClick={handleClick}
        style={{
          padding: "10px",
          backgroundColor: "green",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Enviar
      </button>

      <br />
      <br />

      {/* Área donde se muestra la respuesta en streaming */}
      <div
        style={{
          whiteSpace: "pre-wrap",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "5px",
          minHeight: "50px",
        }}
      >
        {responseText || "Esperando respuesta..."}
      </div>
    </div>
  );
}
