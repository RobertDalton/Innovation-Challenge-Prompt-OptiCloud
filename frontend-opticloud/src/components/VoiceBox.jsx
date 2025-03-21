import { useState, useEffect, useCallback } from 'react';
import voiceService from '../services/voiceService';

const VoiceBox = ({ onVoiceResult, isActive }) => {
    const [isListening, setIsListening] = useState(false);
    const [error, setError] = useState(null);

    const startListening = useCallback(() => {
        setError(null);
        if (!isListening) {
            const started = voiceService.startListening(
                async (text) => {
                    try {
                        const result = await voiceService.sendToApi(text);
                        onVoiceResult(result);
                        setIsListening(false);
                    } catch (err) {
                        setError('Failed to process voice input');
                        setIsListening(false);
                    }
                },
                (error) => {
                    setError(error);
                    setIsListening(false);
                }
            );

            if (started) {
                setIsListening(true);
            }
        }
    }, [isListening, onVoiceResult]);

    const stopListening = useCallback(() => {
        voiceService.stopListening();
        setIsListening(false);
    }, []);

    useEffect(() => {
        if (isActive && !isListening) {
            startListening();
        } else if (!isActive && isListening) {
            stopListening();
        }

        return () => {
            if (isListening) {
                voiceService.stopListening();
            }
        };
    }, [isActive, isListening, startListening, stopListening]);

    if (!isActive) return null;

    return (
        <div 
            style={{
                backgroundColor: 'var(--color-primaryBackground)',
                borderColor: 'var(--color-element)'
            }}
            className="fixed bottom-24 left-1/2 transform -translate-x-1/2 
                       p-4 rounded-lg shadow-lg border flex flex-col items-center 
                       space-y-2 min-w-[200px]"
        >
            <div className="relative">
                <div 
                    className={`w-12 h-12 rounded-full flex items-center justify-center
                              ${isListening ? 'animate-pulse' : ''}`}
                    style={{ 
                        backgroundColor: isListening ? 'var(--color-primary)' : 'var(--color-element)'
                    }}
                >
                    <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-6 w-6" 
                        style={{ color: 'var(--color-primaryText)' }}
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                    >
                        <path fillRule="evenodd" 
                              d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" 
                              clipRule="evenodd" 
                        />
                    </svg>
                </div>
            </div>
            <p style={{ color: 'var(--color-primaryText)' }} className="text-sm font-medium">
                {isListening ? 'Listening...' : 'Speech Mode is on'}
            </p>
            {error && (
                <p style={{ color: 'var(--color-primary)' }} className="text-xs text-center">
                    {error}
                </p>
            )}
        </div>
    );
};

export default VoiceBox;