import { useEffect, useState, useRef } from 'react';
import axios from 'axios';

export default function Chat() {
  const userId = localStorage.getItem('user_id');
  const mode = localStorage.getItem('mode');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const recognitionRef = useRef(null);

  // TTS
  const speak = (text) => {
    if ('speechSynthesis' in window && mode === 'voice') {
      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthesis.speak(utterance);
    }
  };

  // STT
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech Recognition not supported in this browser');
      return;
    }
    const SpeechRecognition = window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      sendMessage(spokenText);
    };
    recognition.onerror = (event) => {
      alert('STT error: ' + event.error);
    };
    recognition.start();
    recognitionRef.current = recognition;
  };

  const sendMessage = async (textToSend) => {
    if (!textToSend) return;

    setMessages(prev => [...prev, { from: 'user', text: textToSend }]);
    setInput('');

    try {
      const res = await axios.post('http://localhost:8000/chat', {
        user_id: userId,
        user_input: textToSend,
      });

      const botReply = res.data.response;
      setMessages(prev => [...prev, { from: 'bot', text: botReply }]);
      speak(botReply);
    } catch (err) {
      alert('Error communicating with backend.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>🧠 Mental Health Chatbot</h2>
      <div style={{ height: '300px', overflowY: 'auto', border: '1px solid gray', padding: '1rem', marginBottom: '1rem' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.from === 'user' ? 'right' : 'left' }}>
            <strong>{msg.from === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {mode === 'text' ? (
        <>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message"
          />
          <button onClick={() => sendMessage(input)}>Send</button>
        </>
      ) : (
        <button onClick={startListening}>🎙️ Speak</button>
      )}
    </div>
  );
}
