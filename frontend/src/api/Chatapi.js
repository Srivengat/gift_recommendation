import axios from "axios";

const API_URL = "http://localhost:8000";

export const startChat = async () => {
  return axios.post(`${API_URL}/start-chat`);
};

export const sendChatMessage = async (sessionId, message) => {
  return axios.post(`${API_URL}/chat`, {
    session_id: sessionId,
    message: message,
  });
};

export const restartChat = async (sessionId) => {
  return axios.post(`${API_URL}/restart-chat`, null, {
    params: { session_id: sessionId },
  });
};
