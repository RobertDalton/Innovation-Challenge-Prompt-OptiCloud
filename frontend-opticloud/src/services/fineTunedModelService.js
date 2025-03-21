class FineTunedModelService {
  constructor() {
    this.baseUrl = import.meta.env.VITE_FINE_TUNED_MODEL;
  }

  async generateResponse(text) {
    try {
      const response = await fetch(
        "https://opticloud-http-streaming.azurewebsites.net/generate-text",
        {
          method: "POST", // Cambiado a POST para enviar datos
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ prompt: text }), // Enviamos el mensaje del usuario
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
  }

  // Helper method to check response quality
  isHighQualityResponse(response) {
    return response.confidence && response.confidence > 0.8;
  }
}

export default new FineTunedModelService();
