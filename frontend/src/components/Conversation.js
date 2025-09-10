import React, { useEffect, useState } from "react";
import { gql } from "@apollo/client/core"; 
import { useQuery } from "@apollo/client/react/hooks"; 
// import { ApolloProvider, useQuery, useMutation, gql } from "@apollo/client";
import { List, ListItem, ListItemText, Paper } from "@mui/material";

const GET_CONVERSATIONS = gql`
  query {
    conversations {
      id
      title
      is_group
    }
  }
`;

export default function Conversations({ selected, setSelected }) {
    const { data, loading, error, refetch } = useQuery(GET_CONVERSATIONS);
    const [conversations, setConversations] = useState([]);

    useEffect(() => {
        if (data && data.conversations) setConversations(data.conversations);
    }, [data]);

    if (loading) return <p>Loading conversations...</p>;
    if (error) return <p>Error loading conversations</p>;

    return (
        <Paper sx={{ maxHeight: 400, overflow: "auto", mb: 2 }}>
            <List>
                {conversations.map((conv) => (
                    <ListItem
                        button
                        key={conv.id}
                        selected={selected?.id === conv.id}
                        onClick={() => setSelected(conv)}
                    >
                        <ListItemText
                            primary={conv.title}
                            secondary={conv.is_group ? "Group" : "Direct"}
                        />
                    </ListItem>
                ))}
            </List>
        </Paper>
    );
}
