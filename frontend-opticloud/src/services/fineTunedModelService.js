class FineTunedModelService {
    constructor() {
        this.baseUrl = import.meta.env.VITE_FINE_TUNED_MODEL;
    }

    async generateResponse(text) {
        try {
            const response = await fetch(`${this.baseUrl}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${import.meta.env.VITE_API_KEY}`
                },
                body: JSON.stringify({
                    prompt: text,
                    max_tokens: 150,
                    temperature: 0.7,
                    top_p: 1.0,
                    frequency_penalty: 0.0,
                    presence_penalty: 0.0
                })
            });

            if (!response.ok) {
                throw new Error(`Fine-tuned model API error: ${response.status}`);
            }

            const data = await response.json();
            return {
                response: data.generated_text,
                confidence: data.confidence_score,
                model_version: data.model_version,
                processing_time: data.processing_time,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error('Fine-tuned model service error:', error);
            throw {
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    // Helper method to check response quality
    isHighQualityResponse(response) {
        return response.confidence && response.confidence > 0.8;
    }
}

export default new FineTunedModelService();