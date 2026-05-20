import apiClient from './client.ts'

interface LoginCredentials {
    email: string
    password: string
}

interface AuthResponse {
    access_token: string
    token_type: string
}

const response = await apiClient.post<AuthResponse>('/login', data)
return response.data

const response = await apiClient.post<LoginCredentials>('/register', data)
return response.data