import React, { useState } from "react";
import { gql } from "@apollo/client/core"; 
import { useMutation } from "@apollo/client/react/hooks";  
import { TextField, Button, Box } from "@mui/material";

const LOGIN_MUTATION = gql`
  mutation login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      success
      token
      user { id username display_name }
    }
  }
`;

export default function Login({ setToken }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [login, { loading }] = useMutation(LOGIN_MUTATION, {
        onCompleted: (data) => {
            if (data.login.success) {
                localStorage.setItem("token", data.login.token);
                setToken(data.login.token);
            } else alert("Invalid credentials");
        },
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        login({ variables: { username, password } });
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 2 }}>
            <TextField
                label="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
            <Button type="submit" variant="contained" disabled={loading}>Login</Button>
        </Box>
    );
}
