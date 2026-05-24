import apiClient from './client'

export interface TaskResponse {
    id: number
    title: string
    status: string
    priority: string
    assignee_id: number
    due_date: string
}

export interface TaskMessage {
    message: string
}

export interface TaskCreate {
    title: string
    priority: string
    status?: string
    due_date?: string
    assignee_id?: number
}

export const getTasks = async(project_id: number): Promise<TaskResponse[]> => {
    const response = await apiClient.get<TaskResponse[]>(`/api/projects/${project_id}/tasks`)
    return response.data
}

export const getTask = async(project_id: number, id: number): Promise<TaskResponse> => {
    const response = await apiClient.get<TaskResponse>(`/api/projects/${project_id}/tasks/${id}`)
    return response.data
}

export const createTask = async(project_id: number, data:TaskCreate): Promise<TaskResponse> => {
    const response = await apiClient.post<TaskResponse>(`/api/projects/${project_id}/tasks`, data)
    return response.data
}

export const updateTask = async(project_id: number, id: number, data:TaskCreate): Promise<TaskMessage> => {
    const response = await apiClient.put<TaskMessage>(`/api/projects/${project_id}/tasks/${id}`, data)
    return response.data
}

export const deleteTask = async(project_id:number, id: number): Promise<TaskMessage> => {
    const response = await apiClient.delete<TaskMessage>(`/api/projects/${project_id}/tasks/${id}`)
    return response.data
}