
import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [ponds, setPonds] = useState([])
  const [selectedPond, setSelectedPond] = useState('pond_1')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchPonds()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchPonds = async () => {
    try {
      const response = await fetch(`${API_BASE}/ponds`)
      const data = await response.json()
      setPonds(data)
    } catch (error) {
      console.error('Failed to fetch ponds:', error)
    }
  }

  const getStatusClass = (sensor) => {
    if (!sensor) return 'safe'

    if (
      sensor.dissolved_oxygen < 5 ||
      sensor.ammonia_ppm > 0.5 ||
      sensor.ph < 6.5 ||
      sensor.ph > 8.5
    ) {
      return 'risk'
    }

    return 'safe'
  }

  const sendMessage = async (customMessage = null) => {
    const messageToSend = customMessage || input

    if (!messageToSend.trim()) return

    const userMessage = {
      role: 'user',
      text: messageToSend
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          pond_id: selectedPond,
          session_id: sessionId
        })
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data = await response.json()

      setSessionId(data.session_id)

      const botMessage = {
        role: 'bot',
        text: data.reply,
        sensor: data.sensor_snapshot,
        latency: data.latency_ms,
        tokens: data.token_usage
      }

      setMessages(prev => [...prev, botMessage])

    } catch (error) {
      console.error('Error:', error)

      const errorMessage = {
        role: 'bot',
        text: '⚠️ Unable to process request. Please try again.'
      }

      setMessages(prev => [...prev, errorMessage])

    } finally {
      setLoading(false)
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  const quickQuestions = [
    'Is this pond safe for feeding?',
    'What is the current oxygen level?',
    'Is ammonia dangerous right now?',
    'Do you detect algae bloom risk?',
  ]

  return (
    <div className="app-shell">

      <div className="sidebar">
        <h2>AquaBot</h2>
        <p className="subtitle">AI Pond Monitoring Assistant</p>

        <div className="pond-selector">
          <label>Select Pond</label>

          <select
            value={selectedPond}
            onChange={(e) => setSelectedPond(e.target.value)}
          >
            {ponds.map((pond) => (
              <option key={pond.pond_id} value={pond.pond_id}>
                {pond.pond_name}
              </option>
            ))}
          </select>
        </div>

        <div className="quick-actions">
          <h4>Quick Questions</h4>

          {quickQuestions.map((q, index) => (
            <button
              key={index}
              className="quick-btn"
              onClick={() => sendMessage(q)}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <div className="main-chat">

        <div className="topbar">
          <div>
            <h1>Fish Pond AI Chatbot</h1>
            <p>AI-assisted aquaculture monitoring</p>
          </div>

          <button
            className="refresh-btn"
            onClick={fetchPonds}
          >
            Refresh Sensors
          </button>
        </div>

        <div className="sensor-grid">
          {ponds
            .filter(p => p.pond_id === selectedPond)
            .map((pond) => (
              <div
                key={pond.pond_id}
                className={`sensor-card ${getStatusClass(pond)}`}
              >
                <div className="sensor-header">
                  <h3>{pond.pond_name}</h3>
                  <span className={`status-badge ${getStatusClass(pond)}`}>
                    {getStatusClass(pond).toUpperCase()}
                  </span>
                </div>

                <div className="metrics">
                  <div className="metric">
                    <span>pH</span>
                    <strong>{pond.ph}</strong>
                  </div>

                  <div className="metric">
                    <span>Oxygen</span>
                    <strong>{pond.dissolved_oxygen} mg/L</strong>
                  </div>

                  <div className="metric">
                    <span>Temperature</span>
                    <strong>{pond.temperature_c}°C</strong>
                  </div>

                  <div className="metric">
                    <span>Ammonia</span>
                    <strong>{pond.ammonia_ppm} ppm</strong>
                  </div>
                </div>
              </div>
            ))}
        </div>

        <div className="chat-container">

          <div className="messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message-row ${msg.role}`}
              >

                <div className={`message-bubble ${msg.role}`}>

                  <div className="message-header">
                    {msg.role === 'user' ? 'You' : 'AquaBot'}
                  </div>

                  <div className="message-text">
                    {msg.text}
                  </div>

                  {msg.sensor && (
                    <div className="meta-panel">
                      <span>⚡ {msg.latency} ms</span>
                      <span>🧠 {msg.tokens?.total_tokens} tokens</span>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row bot">
                <div className="message-bubble bot typing">
                  AquaBot is analyzing pond conditions...
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask about pond health, oxygen, algae, feeding..."
              disabled={loading}
            />

            <button
              onClick={() => sendMessage()}
              disabled={loading}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
