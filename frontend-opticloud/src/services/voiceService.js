class VoiceService {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            // Add onend handler to update state
            this.recognition.onend = () => {
                this.isListening = false;
            };
        }
    }

    startListening(onResult, onError) {
        if (!this.recognition) {
            onError('Speech recognition is not supported in this browser');
            return false;
        }

        // Prevent starting if already listening
        if (this.isListening) {
            return true;
        }

        try {
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                onResult(transcript);
            };

            this.recognition.onerror = (event) => {
                this.isListening = false;
                onError(event.error);
            };

            this.recognition.start();
            this.isListening = true;
            return true;
        } catch (error) {
            console.error('Error starting recognition:', error);
            onError(error.message);
            this.isListening = false;
            return false;
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            try {
                this.recognition.stop();
                this.isListening = false;
            } catch (error) {
                console.error('Error stopping recognition:', error);
            }
        }
    }

    async sendToApi(text) {
        try {
            const response = await fetch('your-api-endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending voice data:', error);
            throw error;
        }
    }
}

export default new VoiceService();