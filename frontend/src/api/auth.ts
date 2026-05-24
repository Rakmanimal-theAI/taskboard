import apiClient from './client'
export interface LoginCredentials {
    email: string
    password: string
}
export interface Registration {
    name: string,
    email: string
    password: string
}
export interface AuthResponse {
    access_token: string
    token_type: string
}
export interface UserResponse {
    id: number
    name: string
    email: string
    created_at: string
}

export const login = async(credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>(`/auth/login`, credentials)
    return response.data
}

export const register = async(registration: Registration): Promise<UserResponse> => {
    const response = await apiClient.post<UserResponse>(`/auth/register`, registration)
    return response.data
}