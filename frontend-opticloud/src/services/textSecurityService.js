class TextSecurityService {
    constructor() {
        this.baseUrl = import.meta.env.VITE_TEXT_SECURITY_PIPELINE;
    }

    async analyzeText(text) {
        try {
            const response = await fetch(`${this.baseUrl}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error(`Text Security API error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Text Security service error:', error);
            throw {
                safe: false,
                error: error.message,
                original_language: null,
                translated: false,
                pii_detected: false,
                pii_results: {},
                content_safety_results: {},
                prompt_shield_results: {}
            };
        }
    }

    // Helper method to check if response indicates safety
    isSafe(response) {
        return response.safe && !response.pii_detected;
    }
}

export default new TextSecurityService();