import React, { useState } from "react";
import { gql } from "@apollo/client/core";
import { useMutation } from "@apollo/client/react/hooks";
import { Box, TextField, Button } from "@mui/material";

const SEND_MESSAGE = gql`
  mutation sendMessage($input: MessageInput!) {
    sendMessage(input: $input) {
      success
      message {
        id
        content
        attachment_url
        created_at
      }
    }
  }
`;

export default function MessageInput({ conversationId }) {
  const [content, setContent] = useState("");
  const [file, setFile] = useState(null);
  const [sendMessage] = useMutation(SEND_MESSAGE);

  const handleSubmit = async (e) => {
    e.preventDefault();
    let attachmentFilename = null;

    if (file) attachmentFilename = file.name; // backend expects file name

    await sendMessage({
      variables: {
        input: { conversation_id: conversationId, content, attachment_filename: attachmentFilename },
      },
      context: {
        hasUpload: !!file,
        files: file ? { [file.name]: file } : {}
      },
    });

    setContent("");
    setFile(null);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", gap: 1 }}>
      <TextField
        fullWidth
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Type a message..."
      />
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <Button type="submit" variant="contained">Send</Button>
    </Box>
  );
}
