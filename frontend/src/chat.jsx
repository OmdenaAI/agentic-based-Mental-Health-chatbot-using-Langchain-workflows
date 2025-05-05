import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

function Chat() {
  const now = new Date();
  const hour = now.getHours();
  const minutes = now.getMinutes();

  const [messages, setMessages] = useState([
    {
      id: Date.now(),
      text: "Hi there! I'm GreenLife. How may I help your mental health?",
      sender: "bot",
      timestamp: `${hour}:${minutes}`,
    },
  ]);

  const [input, setInput] = useState(""); // input from the User

  const [loading, setLoading] = useState(false); //state variable to store the state of the send button

  // // Reference for the messages container to scroll it
  const messagesEndRef = useRef(null);

  // // Scroll to the bottom whenever messages change
  // useEffect(() => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // }, [messages]);

  // function to handle all the sending and retrieval of messages - this function is run when the send button is clicked
  const handleSend = async () => {
    // set send button to true to identify that a message was sent to the backend
    setLoading(true);

    // Update messages with user messsage
    const userMessage = {
      id: Date.now(),
      text: input,
      sender: "user",
      timestamp: `${hour}:${minutes}`,
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]); // updating all messages
    setInput("");

    // send message to backend
    const user_message = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: [],
        age: 50,
        emotion: "stress",
        gender: "female",
        language: "english",
        query: input,
        docs: [],
        next: "string",
      }),
    });

    // retrieve bot response
    const llm_response = await user_message.json();

    // Update state of messages with llm_response
    const botMessage = {
      id: Date.now(),
      text: llm_response.reply,
      sender: "them",
      timestamp: `${hour}:${minutes}`,
    };
    setMessages((prevMessages) => [...prevMessages, botMessage]);

    // remove any value stored in
    if (input.trim() === "") return;

    setLoading(false);
  };

  return (
    <div className="flex flex-col p-10 w-full h-screen border rounded-lg shadow-lg bg-gray-200">
      {/* Header */}
      <div className="p-4 text-lg font-semibold text-center text-black">
        GreenLife
      </div>

      {/* Chat messages (scrollable) */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`max-w-[70%] px-4 py-3 rounded-lg mt-4 ${
              msg.sender === "user"
                ? "bg-green-400 text-black ml-auto"
                : "bg-gray-300 text-gray-900"
            } md:flex md:justify-between md:items-end`}
          >
            {/* Message Text */}
            <div className="md:max-w-[90%]">
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>

            {/* Timestamp */}
            <div
              className="text-xs text-right"
            >
              {msg.timestamp}
            </div>
          </div>
        ))}
      </div>

      {/* Input always at bottom */}
      <div className="p-4 border-t bg-white flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message"
          className="flex-1 px-4 py-2 border text-black rounded-full outline-none focus:ring-2 focus:ring-green-400"
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-green-500 text-white rounded-full hover:bg-green-600 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;
