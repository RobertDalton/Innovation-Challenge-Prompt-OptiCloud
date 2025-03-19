import { useState } from 'react'
import Chatbot from './components/Chatbot'
import Header from './components/Header'
import GgWaveExample from './components/AudioListener'
import './App.css'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 pt-16">
        <Chatbot />
        <GgWaveExample />
      </main>
    </div>
  )
}

export default App
