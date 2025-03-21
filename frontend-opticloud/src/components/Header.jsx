import { useState, useEffect, useRef } from "react";

const Header = ({ setColorMode, currentMode, onSpeechModeChange }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSpeechMode, setIsSpeechMode] = useState(false);
  const [getResponse, setGetResponse] = useState(''); // Estado para la respuesta del GET
  const [isFetching, setIsFetching] = useState(false); // Nuevo estado
  const menuRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleColorModeChange = (mode) => {
    setColorMode(mode);
    setIsMenuOpen(false);
  };

  const toggleSpeechMode = () => {
    setIsSpeechMode(!isSpeechMode);
    onSpeechModeChange(!isSpeechMode);
  };

  const handleGetRequest = async () => {
    if (isFetching) return;

    setIsFetching(true);
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/speech/speech-translate"
      );
      const data = await response.json();
      setGetResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error("Error en la petición GET:", error);
      setGetResponse("Error al obtener los datos.");
    } finally {
      setIsFetching(false);
    }
  };

  return (
    <header
      style={{
        backgroundColor: "var(--color-primaryBackground)",
        borderColor: "var(--color-element)",
      }}
      className="shadow-md fixed top-0 left-0 right-0 z-10 border-b"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <h1
          className="text-2xl font-bold"
          style={{ color: "var(--color-primary)" }}
        >
          OptiCloud
        </h1>

        <div className="flex items-center gap-3">
          {/* Speech Mode Button */}
          <button
            onClick={() => { toggleSpeechMode(); handleGetRequest(); }}
            style={{
              backgroundColor: isSpeechMode
                ? "var(--color-primary)"
                : "var(--color-element)",
              color: "var(--color-primaryText)",
            }}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
            aria-label="Toggle Speech Mode"
            title="Toggle Speech Mode"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z"
                clipRule="evenodd"
              />
            </svg>
            <span className="hidden sm:inline">Speech Mode</span>
          </button>

          {/* Existing Color Mode Button */}
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              style={{
                backgroundColor: "var(--color-element)",
                color: "var(--color-primaryText)",
              }}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
              <span className="hidden sm:inline">
                {currentMode.charAt(0).toUpperCase() + currentMode.slice(1)}{" "}
                Mode
              </span>
            </button>

            {isMenuOpen && (
              <div
                style={{ backgroundColor: "var(--color-secondaryBackground)" }}
                className="absolute right-0 mt-2 w-48 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5"
              >
                <div className="py-1">
                  {["normal", "deuteranopia", "protanopia", "tritanopia"].map(
                    (mode) => (
                      <button
                        key={mode}
                        onClick={() => handleColorModeChange(mode)}
                        style={{
                          backgroundColor:
                            currentMode === mode
                              ? "var(--color-element)"
                              : "transparent",
                          color: "var(--color-primaryText)",
                        }}
                        className="w-full text-left px-4 py-2 text-sm hover:opacity-90"
                      >
                        {mode.charAt(0).toUpperCase() + mode.slice(1)} Vision
                      </button>
                    )
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
