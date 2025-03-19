import { useState, useEffect, useRef } from 'react';

const Header = ({ setColorMode, currentMode }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleColorModeChange = (mode) => {
    setColorMode(mode);
    setIsMenuOpen(false);
  };

  return (
    <header style={{ 
      backgroundColor: 'var(--color-primaryBackground)',
      borderColor: 'var(--color-element)'
    }} className="shadow-md fixed top-0 left-0 right-0 z-10 border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold" style={{ color: 'var(--color-primary)' }}>
          OptiCloud
        </h1>
        
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            style={{ 
              backgroundColor: 'var(--color-element)',
              color: 'var(--color-primaryText)'
            }}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
            <span className="hidden sm:inline">
              {currentMode.charAt(0).toUpperCase() + currentMode.slice(1)} Mode
            </span>
          </button>

          {isMenuOpen && (
            <div 
              style={{ backgroundColor: 'var(--color-secondaryBackground)' }}
              className="absolute right-0 mt-2 w-48 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5"
            >
              <div className="py-1">
                {['normal', 'deuteranopia', 'protanopia', 'tritanopia'].map((mode) => (
                  <button
                    key={mode}
                    onClick={() => handleColorModeChange(mode)}
                    style={{ 
                      backgroundColor: currentMode === mode ? 'var(--color-element)' : 'transparent',
                      color: 'var(--color-primaryText)'
                    }}
                    className="w-full text-left px-4 py-2 text-sm hover:opacity-90"
                  >
                    {mode.charAt(0).toUpperCase() + mode.slice(1)} Vision
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
