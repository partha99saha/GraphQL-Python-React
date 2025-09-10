import React, { useState } from "react";
import { ApolloProvider } from "@apollo/client";
// import client from "@apollo/client/react";
import client from "./apollo/client";
import Login from "./components/Login";
import Register from "./components/Register";
import Chat from "./components/Chat";
import { Container, Typography, Button } from "@mui/material";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <ApolloProvider client={client}>
      <Container>
        <Typography variant="h4" gutterBottom>HeyBro Chat App</Typography>

        {!token ? (
          <>
            <Login setToken={setToken} />
            <Register setToken={setToken} />
          </>
        ) : (
          <>
            <Button variant="contained" color="secondary" onClick={handleLogout}>
              Logout
            </Button>
            <Chat token={token} />
          </>
        )}
      </Container>
    </ApolloProvider>
  );
}

export default App;
