import axios from 'axios';

// Use environment variable if provided, otherwise use localhost
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth services
export const authService = {
  register: async (email, password, fullName) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

// CV services
export const cvService = {
  uploadCV: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('token');
    const response = await axios.post(`${API_URL}/cv/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      },
    });
    return response.data;
  },

  getHistory: async () => {
    const response = await api.get('/cv/history');
    return response.data;
  },

  getCVDetails: async (cvId) => {
    const response = await api.get(`/cv/${cvId}`);
    return response.data;
  },

  deleteCV: async (cvId) => {
    const response = await api.delete(`/cv/${cvId}`);
    return response.data;
  },
};

// Job services
export const jobService = {
  searchJobs: async (page = 1, perPage = 10) => {
    const response = await api.get('/jobs/search', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/jobs/stats');
    return response.data;
  },
};

export default api;
