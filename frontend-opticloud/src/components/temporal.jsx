const handleSecurityPipeline = async (message) => {
    try {
      // 1. Perform security analysis on the message first.
      const securityResult = await textSecurityService.analyzeText(message);
      console.log("Security analysis result:", securityResult);

      // 2. If the content is unsafe, stop the process early.
      if (!securityResult.safe) {
        setMessages((prev) => [
          ...prev,
          {
            text: "Security check detected potential issues. Cannot proceed.",
            sender: "bot",
            securityData: securityResult,
            error: true,
          },
        ]);
        return;
      }

      // 3. Make the request to the streaming API.
      const response = await fetch(
        "https://opticloud-http-streaming.azurewebsites.net/generate-text",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ prompt: message }), // Send the user message
        }
      );

      if (!response.body) {
        console.error("No response body");
        setMessages((prev) => [
          ...prev,
          {
            text: "Failed to receive a response from the server.",
            sender: "bot",
            error: true,
          },
        ]);
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
      }
      // Update the messages in real-time
      setMessages((prev) => [
        ...prev,
        {
          text: result,
          sender: "bot",
          isTyping: true,
        },
      ]);

      // 4. After receiving the response, finalize the result with the content.
      setMessages((prev) => [
        ...prev,
        {
          text: result,
          sender: "bot",
          isTyping: false,
        },
      ]);
    } catch (error) {
      console.error("Error during security pipeline:", error);
      setMessages((prev) => [
        ...prev,
        {
          text: "An error occurred during the security check or processing. Please try again.",
          sender: "bot",
          error: true,
        },
      ]);
    }
  };