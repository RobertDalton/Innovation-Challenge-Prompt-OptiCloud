import { useState } from 'react'
import Chatbot from './components/Chatbot'
import Header from './components/Header'
import './App.css'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 pt-16">
        <Chatbot />
      </main>
    </div>
  )
}

export default App
