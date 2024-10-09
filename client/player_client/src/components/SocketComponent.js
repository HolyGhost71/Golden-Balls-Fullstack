import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import Box from "@mui/material/Box";
import { Button } from "@mui/material";

const SocketComponent = () => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const [ballValues, setBallValues] = useState([]);

  useEffect(() => {
    // Establish a connection to the Flask-SocketIO server
    const newSocket = io("http://localhost:5000", {
      transports: ["websocket"], // Use WebSocket transport
      withCredentials: true, // Include credentials (cookies, etc.)
    });
    setSocket(newSocket);

    // Handle incoming messages
    newSocket.on("ball_values", (val) => {
      setBallValues((prevValues) => [...prevValues, val]);
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
      <h1 className=".title">Golden Balls</h1>
      <h4>Player 1 Balls:</h4>
      <Box>
        {ballValues[0].map((val, index) => (
          <Button>{val}</Button>
        ))}
      </Box>
      <h4>Player 2 Balls:</h4>
      <Box>
        {ballValues[1].map((val, index) => (
          <Button>{val}</Button>
        ))}
      </Box>
      <h4>Player 3 Balls:</h4>
      <Box>
        {ballValues[2].map((val, index) => (
          <Button>{val}</Button>
        ))}
      </Box>
      <h4>Player 4 Balls:</h4>
      <Box>
        {ballValues[3].map((val, index) => (
          <Button>{val}</Button>
        ))}
      </Box>
    </div>
  );
};

export default SocketComponent;
