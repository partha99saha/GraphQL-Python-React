import React, { useState } from "react";
import { gql } from "@apollo/client/core";
import { useMutation } from "@apollo/client/react/hooks";
import { TextField, Button, Box } from "@mui/material";

const REGISTER_MUTATION = gql`
  mutation register($username: String!, $display_name: String!, $password: String!) {
    register(username: $username, display_name: $display_name, password: $password) {
      success
      token
      user { id username display_name }
    }
  }
`;

export default function Register({ setToken }) {
    const [username, setUsername] = useState("");
    const [displayName, setDisplayName] = useState("");
    const [password, setPassword] = useState("");

    const [register, { loading }] = useMutation(REGISTER_MUTATION, {
        onCompleted: (data) => {
            if (data.register.success) {
                localStorage.setItem("token", data.register.token);
                setToken(data.register.token);
            } else alert("Registration failed");
        },
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        register({ variables: { username, display_name: displayName, password } });
    };

    return (
        <Box component="form" onSubmit={handleSubmit}>
            <TextField
                label="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                fullWidth
                margin="normal"
            />
            <TextField
                label="Display Name"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                fullWidth
                margin="normal"
            />
            <TextField
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                fullWidth
                margin="normal"
            />
            <Button type="submit" variant="contained" disabled={loading}>Register</Button>
        </Box>
    );
}
