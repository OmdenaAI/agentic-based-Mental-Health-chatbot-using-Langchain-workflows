import React, { useState, useRef } from "react";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";
import Input from "./ui/Input";
import axios from "axios";

const ChatPage = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        message: input,
        history: messages.map((msg) => `${msg.sender}: ${msg.text}`),
      });

      const reply = res.data.response?.raw || res.data.response || "No response";
      const botMsg = { sender: "bot", text: reply };
      setMessages((prev) => [...prev, botMsg]);
      speakText(reply);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  const speakText = (text) => {
    if (!synthRef.current) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "en-US";
    synthRef.current.speak(utter);
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support speech recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.onerror = (e) => console.error("STT Error:", e);

    recognition.start();
    recognitionRef.current = recognition;
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <Card className="max-w-4xl mx-auto mt-10 p-6 h-[75vh] flex flex-col">
      <h2 className="text-2xl font-bold text-green-700 mb-4">MindfulChat 🤖</h2>

      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg max-w-[70%] ${
              msg.sender === "user" ? "bg-green-100 ml-auto text-right" : "bg-gray-100 text-left"
            }`}
          >
            <span className="block font-semibold mb-1">{msg.sender === "user" ? "You" : "Bot"}:</span>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex items-center gap-2">
        <Input
          className="flex-1"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <Button onClick={sendMessage}>Send</Button>
        <Button onClick={startListening}>🎤</Button>
      </div>
    </Card>
  );
};

export default ChatPage;
