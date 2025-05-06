import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { LuAudioLines } from "react-icons/lu";
import { FaStopCircle } from "react-icons/fa";
import { FaCircleStop, FaMicrophone } from "react-icons/fa6";
import { v4 as uuidv4 } from "uuid";

// import ReactAudioPlayer from 'react-audio-player';

function Chat() {
  const now = new Date();
  const hour = now.getHours();
  const minutes = now.getMinutes();

  const [messages, setMessages] = useState([
    {
      id: uuidv4(),
      text: "Hi there! I'm GreenLife. How may I help your mental health?",
      sender: "bot",
      timestamp: `${hour}:${minutes}`,
    },
  ]);

  // state variable to store input from the User
  const [input, setInput] = useState("");

  //state variable to store the state of the send button
  const [loading, setLoading] = useState(false);

  // state varibale to store if the user wants to use voice control or not
  const [voiceEnabled, setVoiceEnabled] = useState(false);

  // // Reference for the messages container to scroll it
  const messagesEndRef = useRef(null);

  // Scroll to the bottom whenever messages change
  // useEffect(() => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // }, [messages]);

  //////////////code-testing//////////////////////////////////////////

  const [isRecording, setIsRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [uploadStatus, setUploadStatus] = useState("");

  const mediaStream = useRef(null);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    setSeconds(0);
    setUploadStatus("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStream.current = stream;
      mediaRecorder.current = new MediaRecorder(stream);

      mediaRecorder.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.current.push(e.data);
        }
      };

      const timer = setInterval(() => {
        setSeconds((prev) => prev + 1);
      }, 1000);

      mediaRecorder.current.onstop = async () => {
        clearInterval(timer);
        const recordedBlob = new Blob(chunks.current, { type: "audio/webm" });
        chunks.current = [];

        // Upload recorded audio to backend
        const formData = new FormData();
        formData.append("audio", recordedBlob, `${uuidv4()}.webm`);

        try {
          const response = await fetch("http://localhost:8000/store/audio", {
            method: "POST",
            body: formData,
          });

          if (!response.ok) {
            throw new Error("Failed to upload");
          }

          const data = await response.json();
          // updating messages with text from audio
          const text_from_audio_message = {
            id: uuidv4(),
            text: data.text_from_audio,
            sender: "user",
            timestamp: `${hour}:${minutes}`,
          };

          setMessages((prevMessages) => [
            ...prevMessages,
            text_from_audio_message,
          ]); // updating all messages

          setUploadStatus("Upload successful!");
          console.log("Server response:", data);

          // use the text_from_audio to generate a text response from the llm
          const text_audio_llm_message = await fetch("http://localhost:8000/chat", {
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
              query: data.text_from_audio,
              docs: [],
              next: "string",
            }),
          });
      
          // retrieve bot response
          const getting_message = await text_audio_llm_message.json();
      
          // Update state of messages with llm_response
          const message_text_audio_format = {
            id: uuidv4(),
            text: getting_message.reply,
            sender: "bot",
            timestamp: `${hour}:${minutes}`,
          };
          setMessages((prevMessages) => [...prevMessages, message_text_audio_format]);
      

        } catch (err) {
          setUploadStatus("Upload failed.");
          console.error("Upload error:", err);
        }
      };
      mediaRecorder.current.start();
    } catch (err) {
      console.error("Error starting recording:", err);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      mediaStream.current.getTracks().forEach((track) => track.stop());
    }
  };

  const formatTime = (totalSeconds) => {
    const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
    const seconds = String(totalSeconds % 60).padStart(2, "0");
    return `${minutes}:${seconds}`;
  };

  ////////////////////////////////////////////////////////

  const handleToggle = () => {
    /*
    function to handle toggling of button for voice control - 
    it toggles between the true and false state of the useState variable
    }
    */
    setVoiceEnabled((prev) => !prev);
    if (!voiceEnabled) {
      // Start voice control logic here
      console.log("Voice control enabled");
    } else {
      // Stop voice control logic here
      console.log("Voice control disabled");
    }
  };

  const handleAudioButtonClick = async (e) => {
    /*
    function to handle retrieving the text from the textbox and sending it
     to the backend to convert to an audio_file - 
     
    it returns the filename of the audio_file
    }
    */
    // set send button to true to identify that a message was sent to the backend

    const divText = e.target.closest("div").textContent;
    console.log(divText);

    const audio_id = await fetch("http://localhost:8000/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: divText,
      }),
    });

    const filename = await audio_id.json();
    console.log("filename_id", filename.id);

    // if filename exists then retrieve the audio_filename property, which is the filename of the audio file
    if (filename) {
      console.log("Yes filename");
      new Audio(`http://localhost:8000/storage/${filename.id}.wav`).play();
    }
  };

  const handleSend = async () => {
    /*
    function to handle all the sending and retrieval of messages
     - this function is run when the send button is clicked
    }
    */
    // set send button to true to identify that a message was sent to the backend
    setLoading(true);

    // Update messages with user messsage
    const userMessage = {
      id: uuidv4(),
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
      id: uuidv4(),
      text: llm_response.reply,
      sender: "bot",
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
          // box holding messages text
          <div
            key={msg.id}
            className={`max-w-[70%] items-center px-4 py-3 rounded-lg mt-4 ${
              msg.sender === "user"
                ? "bg-green-400 text-black ml-auto"
                : "bg-gray-300 text-gray-900"
            } md:flex md:justify-between`}
          >
            {/* Message Text */}
            <div className="items-center">
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              <span className="cursor-pointer" onClick={handleAudioButtonClick}>
                <LuAudioLines size={25} />{" "}
              </span>
              {/* <span className="cursor-pointer">
                <FaStopCircle size={25} />{" "}
              </span> */}
            </div>

            {/* Timestamp */}
            <div className="text-xs text-right">{msg.timestamp}</div>
          </div>
        ))}
      </div>

      {/* Input*/}
      <div className="p-4 border-t bg-white flex gap-2">
        {/* voice control button */}
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-700">Voice Control</label>
          <button
            onClick={handleToggle}
            className={`px-4 py-2 rounded-full text-white font-semibold transition ${
              voiceEnabled ? "bg-green-500" : "bg-gray-400"
            }`}
          >
            {voiceEnabled ? "ON" : "OFF"}
          </button>
        </div>

        {/* if not voiceEnabled (that is if voiceEnabled is false) use input  else use the mic to record your audio*/}
        {!voiceEnabled ? (
          <>
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
          </>
        ) : (
          <div>
            {/* copied record audio code */}
            <>
              <div className="w-full">

                {/* microphone = off and on */}
                <div className="flex">
                  <div>
                    {isRecording ? (
                      <button
                        onClick={stopRecording}
                        className="flex items-center justify-center text-[30px] bg-red-500 rounded-full p-4 text-white w-[100px] h-[100px]"
                      >
                        <FaCircleStop />
                      </button>
                    ) : (
                      <button
                        onClick={startRecording}
                        className="flex items-center justify-center text-[30px] bg-blue-500 rounded-full p-4 text-white w-[50px] h-[70px]"
                      >
                        <FaMicrophone />
                      </button>
                    )}

                    {uploadStatus && (
                      <p className="text-white mt-4">{uploadStatus}</p>
                    )}
                  </div>

                  {/* audio visual */}
                  <div className="text-sm text-white bg-black px-8 py-4 rounded-lg">
                    {formatTime(seconds)}
                  </div>
                </div>
              </div>
            </>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;
