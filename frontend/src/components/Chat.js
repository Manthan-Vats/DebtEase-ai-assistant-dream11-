import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Avatar,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import axios from 'axios';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/v1/chat/history', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessages(response.data);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    fetchChatHistory();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const userMessage = {
      content: newMessage,
      message_type: 'user',
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setNewMessage('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        '/api/v1/chat/message',
        { content: newMessage },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const assistantMessage = {
        content: response.data.content,
        message_type: 'assistant',
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        content: 'Sorry, I encountered an error. Please try again.',
        message_type: 'assistant',
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        height: 'calc(100vh - 200px)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Chat Messages */}
      <Paper
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 2,
          mb: 2,
          bgcolor: 'background.paper',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              justifyContent: message.message_type === 'user' ? 'flex-end' : 'flex-start',
              mb: 2,
            }}
          >
            <Box
              sx={{
                display: 'flex',
                flexDirection: message.message_type === 'user' ? 'row-reverse' : 'row',
                alignItems: 'flex-start',
                maxWidth: '70%',
              }}
            >
              <Avatar
                sx={{
                  bgcolor: message.message_type === 'user' ? 'primary.main' : 'secondary.main',
                  ml: message.message_type === 'user' ? 1 : 0,
                  mr: message.message_type === 'user' ? 0 : 1,
                }}
              >
                {message.message_type === 'user' ? 'U' : 'AI'}
              </Avatar>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: message.message_type === 'user' ? 'primary.main' : 'background.paper',
                  color: message.message_type === 'user' ? 'white' : 'text.primary',
                  borderRadius: 2,
                }}
              >
                <Typography variant="body1">{message.content}</Typography>
                <Typography variant="caption" color="text.secondary">
                  {new Date(message.created_at).toLocaleTimeString()}
                </Typography>
              </Paper>
            </Box>
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </Paper>

      {/* Message Input */}
      <Paper
        component="form"
        onSubmit={handleSendMessage}
        sx={{
          p: 2,
          bgcolor: 'background.paper',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            disabled={loading}
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.1)',
                },
                '&:hover fieldset': {
                  borderColor: 'primary.main',
                },
              },
            }}
          />
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !newMessage.trim()}
            sx={{ minWidth: '100px' }}
          >
            {loading ? <CircularProgress size={24} /> : <SendIcon />}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default Chat; 