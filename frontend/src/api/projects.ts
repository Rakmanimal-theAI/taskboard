import apiClient from './client'

export interface ProjectCreate {
    title: string
    description?: string
}
export interface ProjectResponse {
    id: number
    title: string
    description?: string
    owner_id: number
}

export interface ProjectMessage {
    message: string
}

export const getProjects = async(): Promise<ProjectResponse[]> => {
    const response = await apiClient.get<ProjectResponse[]>(`/api/projects`)
    return response.data
}

export const getProject = async(id: number): Promise<ProjectResponse> => {
    const response = await apiClient.get<ProjectResponse>(`/api/projects/${id}`)
    return response.data
}

export const createProject = async(data: ProjectCreate): Promise<ProjectResponse> => {
    const response = await apiClient.post<ProjectResponse>(`/api/projects`, data)
    return response.data
}

export const updateProject = async(id: number, data:ProjectCreate): Promise<ProjectResponse> => {
    const response = await apiClient.put<ProjectResponse>(`/api/projects/${id}`, data)
    return response.data
}

export const deleteProject = async(id: number): Promise<ProjectMessage> => {
    const response = await apiClient.delete<ProjectMessage>(`/api/projects/${id}`)
    return response.data
}

export async function summariseProject(projectId: number) {
    const response = await apiClient.post(`/api/projects/${projectId}/summary`, {}, {
        timeout: 120000 // 2 minutes — Ollama can be slow, especially on first load
    })
    return response.data
  }