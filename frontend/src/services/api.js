import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadDocument = async (file, patientData) => {
  const formData = new FormData();
  formData.append('file', file);
  
  if (patientData.name) formData.append('patient_name', patientData.name);
  if (patientData.age) formData.append('patient_age', patientData.age);
  if (patientData.gender) formData.append('patient_gender', patientData.gender);

  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const performOCR = async (visitId) => {
  const response = await api.post(`/ocr/${visitId}`);
  return response.data;
};

export const cleanText = async (visitId) => {
  const response = await api.post(`/clean/${visitId}`);
  return response.data;
};

export const generateSummary = async (visitId) => {
  const response = await api.post(`/summarize/${visitId}`);
  return response.data;
};

export const getSummary = async (visitId) => {
  const response = await api.get(`/summarize/${visitId}`);
  return response.data;
};

export const getVisits = async () => {
  const response = await api.get('/visits/');
  return response.data;
};

export const getVisitDetails = async (visitId) => {
  const response = await api.get(`/visits/${visitId}`);
  return response.data;
};

export default api;
