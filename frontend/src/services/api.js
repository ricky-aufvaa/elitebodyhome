import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // No timeout - let the RAG system take as long as it needs
});

export const sendMessage = async (message, sessionId = null) => {
  try {
    const requestData = {
      message: message
    };
    
    // Add session_id if provided
    if (sessionId) {
      requestData.session_id = sessionId;
    }
    
    const response = await api.post('/chat', requestData);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    if (error.response) {
      // Server responded with error status
      throw new Error(`Server error: ${error.response.status} - ${error.response.data.detail || 'Unknown error'}`);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Cannot connect to the AI service. Please make sure the backend is running.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default api;
