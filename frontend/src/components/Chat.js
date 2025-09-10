import React, { useEffect, useState } from "react";
import { Box, Typography, Paper } from "@mui/material";
import Conversations from "./Conversation";
import MessageInput from "./MessageInput";
import { io } from "socket.io-client";

export default function Chat({ token }) {
    const [selectedConv, setSelectedConv] = useState(null);
    const [messages, setMessages] = useState([]);
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const newSocket = io("http://localhost:5000", {
            auth: { token },
        });
        setSocket(newSocket);

        newSocket.on("new_message", (msg) => {
            if (selectedConv && msg.conversation_id === selectedConv.id) {
                setMessages((prev) => [...prev, msg]);
            }
        });

        return () => newSocket.disconnect();
    }, [token, selectedConv]);

    // Load messages when conversation changes
    useEffect(() => {
        if (!selectedConv) return;

        fetch(`http://localhost:5000/conversations/${selectedConv.id}/messages`, {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((res) => res.json())
            .then((data) => setMessages(data));
    }, [selectedConv, token]);

    return (
        <Box sx={{ display: "flex", gap: 2 }}>
            <Box sx={{ flex: 1 }}>
                <Conversations selected={selectedConv} setSelected={setSelectedConv} />
            </Box>
            <Box sx={{ flex: 3 }}>
                <Paper sx={{ height: 400, overflowY: "auto", p: 2 }}>
                    {selectedConv ? (
                        messages.map((msg) => (
                            <Box key={msg.id} sx={{ mb: 1 }}>
                                <Typography variant="subtitle2">{msg.sender_id}</Typography>
                                <Typography>{msg.content}</Typography>
                                <Typography variant="caption">{msg.created_at}</Typography>
                            </Box>
                        ))
                    ) : (
                        <Typography>Select a conversation</Typography>
                    )}
                </Paper>
                {selectedConv && <MessageInput conversationId={selectedConv.id} />}
            </Box>
        </Box>
    );
}
