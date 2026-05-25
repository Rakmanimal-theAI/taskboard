import axios from 'axios';
import useAuthStore from '../store/authStore'

const API_URL = import.meta.env.VITE_API_URL || '';
console.log('🔍 API Client - Base URL:', API_URL); // Add this line

const apiClient = axios.create({
    baseURL: '',
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json'
    }
});

console.log('🔍 API Client - Final config:', apiClient.defaults); // Add this line

apiClient.interceptors.request.use(
    (config) => {
        const token = useAuthStore.getState().token
        console.log('🔍 Request URL:', (config.baseURL ?? '') + (config.url ?? '')); // Add this line
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
)

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
        useAuthStore.getState().logout()
        window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)  

export default apiClient;