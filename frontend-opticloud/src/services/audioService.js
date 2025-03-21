import ggwave from 'ggwave';

class AudioService {
    constructor() {
        this.context = null;
        this.recorder = null;
        this.mediaStream = null;
        this.ggwave = null;
        this.parameters = null;
        this.instance = null;
        
        // Initialize ggwave when service is created
        ggwave().then((obj) => {
            this.ggwave = obj;
        }).catch(err => {
            console.error('Failed to initialize GGWave:', err);
        });
    }

    async initialize() {
        // Wait for ggwave to be available
        if (!this.ggwave) {
            try {
                this.ggwave = await ggwave();
            } catch (err) {
                throw new Error('Failed to initialize GGWave: ' + err.message);
            }
        }

        if (!this.context) {
            this.context = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 48000 });
            this.parameters = this.ggwave.getDefaultParameters();
            this.parameters.sampleRateInp = this.context.sampleRate;
            this.parameters.sampleRateOut = this.context.sampleRate;
            this.instance = this.ggwave.init(this.parameters);
        }
    }

    convertTypedArray(src, type) {
        const buffer = new ArrayBuffer(src.byteLength);
        new src.constructor(buffer).set(src);
        return new type(buffer);
    }

    async sendAudio(text) {
        await this.initialize();
        
        // Generate audio waveform
        const waveform = this.ggwave.encode(
            this.instance,
            text,
            this.ggwave.ProtocolId.GGWAVE_PROTOCOL_AUDIBLE_FAST,
            10
        );

        // Convert to audio buffer
        const buf = this.convertTypedArray(waveform, Float32Array);
        const buffer = this.context.createBuffer(1, buf.length, this.context.sampleRate);
        buffer.getChannelData(0).set(buf);
        
        // Calculate duration in milliseconds
        const durationMs = (buffer.length / buffer.sampleRate) * 1000;

        // Play audio
        const source = this.context.createBufferSource();
        source.buffer = buffer;
        source.connect(this.context.destination);
        source.start(0);

        return {
            durationMs,
            promise: new Promise(resolve => {
                source.onended = resolve;
            })
        };
    }

    async startListening(onDataReceived) {
        await this.initialize();

        const constraints = {
            audio: {
                echoCancellation: false,
                autoGainControl: false,
                noiseSuppression: false,
            },
        };

        try {
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.mediaStream = this.context.createMediaStreamSource(stream);
            this.recorder = this.context.createScriptProcessor(1024, 1, 1);

            this.recorder.onaudioprocess = (e) => {
                const source = e.inputBuffer;
                const res = this.ggwave.decode(
                    this.instance,
                    this.convertTypedArray(
                        new Float32Array(source.getChannelData(0)),
                        Int8Array
                    )
                );

                if (res && res.length > 0) {
                    const text = new TextDecoder("utf-8").decode(res);
                    onDataReceived(text);
                }
            };

            this.mediaStream.connect(this.recorder);
            this.recorder.connect(this.context.destination);
            return true;
        } catch (err) {
            console.error('Error starting audio capture:', err);
            return false;
        }
    }

    async decodeAudioFile(audioFile) {
        await this.initialize();

        try {
            const arrayBuffer = await audioFile.arrayBuffer();
            const audioBuffer = await this.context.decodeAudioData(arrayBuffer);
            const audioData = audioBuffer.getChannelData(0);
            const convertedData = this.convertTypedArray(audioData, Int8Array);
            const decodedData = this.ggwave.decode(this.instance, convertedData);
            if (decodedData && decodedData.length > 0) {
                return new TextDecoder("utf-8").decode(decodedData);
            }
            
            return null;
        } catch (error) {
            console.error('Error decoding audio file:', error);
            throw new Error('Failed to decode audio file: ' + error.message);
        }
    }

    stopListening() {
        if (this.recorder) {
            this.recorder.disconnect(this.context.destination);
            this.mediaStream.disconnect(this.recorder);
            this.recorder = null;
            return true;
        }
        return false;
    }
}

export default new AudioService();