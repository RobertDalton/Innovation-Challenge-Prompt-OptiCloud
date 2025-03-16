import { useEffect, useRef, useState } from "react";
//TODO: implement ggwave
import ggwaveModule from "ggwave/ggwave.js";

export default function GgWaveExample() {
  const [ggwave, setGgwave] = useState(null);
  const [instance, setInstance] = useState(null);
  const [txData, setTxData] = useState("Hello React");
  const [rxData, setRxData] = useState("");
  const [listening, setListening] = useState(false);
  const contextRef = useRef(null);
  const recorderRef = useRef(null);
  const mediaStreamRef = useRef(null);

  useEffect(() => {
    ggwaveModule().then((ggwave) => {
      setGgwave(ggwave);
    });
  }, []);

  const init = () => {
    if (!contextRef.current && ggwave) {
      const context = new AudioContext({ sampleRate: 48000 });
      contextRef.current = context;
      const parameters = ggwave.getDefaultParameters();
      parameters.sampleRateInp = context.sampleRate;
      parameters.sampleRateOut = context.sampleRate;
      setInstance(ggwave.init(parameters));
    }
  };

  const convertTypedArray = (src, type) => {
    const buffer = new ArrayBuffer(src.byteLength);
    new src.constructor(buffer).set(src);
    return new type(buffer);
  };

  const onSend = () => {
    init();
    stopCapture();
    if (!instance) return;

    const waveform = ggwave.encode(instance, txData, ggwave.ProtocolId.GGWAVE_PROTOCOL_AUDIBLE_FAST, 10);
    const buf = convertTypedArray(waveform, Float32Array);
    const buffer = contextRef.current.createBuffer(1, buf.length, contextRef.current.sampleRate);
    buffer.getChannelData(0).set(buf);
    const source = contextRef.current.createBufferSource();
    source.buffer = buffer;
    source.connect(contextRef.current.destination);
    source.start(0);
  };

  const startCapture = async () => {
    init();
    if (!instance) return;

    const constraints = {
      audio: {
        echoCancellation: false,
        autoGainControl: false,
        noiseSuppression: false,
      },
    };

    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      mediaStreamRef.current = contextRef.current.createMediaStreamSource(stream);
      const recorder = contextRef.current.createScriptProcessor(1024, 1, 1);
      recorder.onaudioprocess = (e) => {
        const res = ggwave.decode(instance, convertTypedArray(new Float32Array(e.inputBuffer.getChannelData(0)), Int8Array));
        if (res && res.length > 0) {
          setRxData(new TextDecoder("utf-8").decode(res));
        }
      };
      mediaStreamRef.current.connect(recorder);
      recorder.connect(contextRef.current.destination);
      recorderRef.current = recorder;
      setListening(true);
    } catch (err) {
      console.error(err);
    }
  };

  const stopCapture = () => {
    if (recorderRef.current) {
      recorderRef.current.disconnect(contextRef.current.destination);
      mediaStreamRef.current.disconnect(recorderRef.current);
      recorderRef.current = null;
    }
    setListening(false);
  };

  return (
    <div className="p-4 max-w-lg mx-auto bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold mb-4">GgWave React Example</h2>
      <div>
        <label className="block mb-2">Tx Data:</label>
        <textarea
          className="w-full p-2 border rounded"
          value={txData}
          onChange={(e) => setTxData(e.target.value)}
        />
      </div>
      <button className="mt-2 px-4 py-2 bg-blue-500 text-white rounded cursor-pointer" onClick={onSend}>
        Send
      </button>
      <div className="mt-4">
        <label className="block mb-2">Rx Data:</label>
        <textarea className="w-full p-2 border rounded" value={rxData} disabled />
      </div>
      <button
        className={`mt-2 px-4 py-2 ${listening ? "bg-red-500" : "bg-green-500"} text-white rounded`}
        onClick={listening ? stopCapture : startCapture}
      >
        {listening ? "Stop Capturing" : "Start Capturing"}
      </button>
    </div>
  );
}