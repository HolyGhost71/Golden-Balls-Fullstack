import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const SocketComponent = () => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Establish a connection to the Flask-SocketIO server
    const newSocket = io("http://localhost:5000", {
      transports: ["websocket"], // Use WebSocket transport
      withCredentials: true, // Include credentials (cookies, etc.)
    });
    setSocket(newSocket);

    // Handle incoming messages
    newSocket.on("ball_values", (msg) => {
      setMessages((prevMessages) => [...prevMessages, msg]);
    });

    // Handle incoming messages
    newSocket.on("vote_1", (msg) => {
      setMessages((prevMessages) => [...prevMessages, "Time to vote"]);
    });

    // Handle connection events
    newSocket.on("connect", () => {
      console.log("Connected to server");
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected from server");
    });

    // Cleanup on unmount
    return () => {
      newSocket.disconnect();
    };
  }, []);

  const sendMessage = () => {
    if (socket && message) {
      socket.send(message);
      setMessage(""); // Clear input
    }
  };

  return (
    <div>
      <h1>SocketIO Client</h1>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message"
      />
      <button onClick={sendMessage}>Send</button>
      <h2>Messages:</h2>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default SocketComponent;
