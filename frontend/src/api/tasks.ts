import apiClient from './client'

interface TaskResponse {
    id: number
    title: string
    status: string
    priority: string
    assignee_id: number
    due_date: string,
    project_id: number
}

interface TaskMessage {
    message: string
}

interface TaskCreate {
    title: string
    priority: string
    due_date?: string
    assignee_id?: number
}

export const getTasks = async(project_id: number): Promise<TaskResponse[]> => {
    const response = await apiClient<TaskResponse[]>(`api/projects/${project_id}/tasks`)
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