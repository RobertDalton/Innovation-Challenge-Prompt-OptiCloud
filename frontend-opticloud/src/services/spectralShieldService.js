class SpectralShieldService {
    constructor() {
        this.baseUrl = import.meta.env.VITE_SPECTRAL_SHIELD;
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
                throw new Error(`Spectral Shield API error: ${response.status}`);
            }

            const data = await response.json();
            return {
                toxic: data.toxic,
                safe: data.safe,
                audioUrl: data.audio_url,
                spectogramUrl: data.spectogram_url
            };
        } catch (error) {
            console.error('Spectral Shield service error:', error);
            throw error;
        }
    }
}

export default new SpectralShieldService();