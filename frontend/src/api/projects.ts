import apiClient from './client'

interface ProjectCreate {
    title: string
}
interface ProjectResponse {
    id: number
    title: string
    owner_id: number
}

interface ProjectMessage {
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

export const updateProject = async(id: number, data:ProjectCreate): Promise<ProjectMessage> => {
    const response = await apiClient.put<ProjectMessage>(`/api/projects/${id}`, data)
    return response.data
}

export const deleteProject = async(id: number): Promise<ProjectMessage> => {
    const response = await apiClient.delete<ProjectMessage>(`/api/projects/${id}`)
    return response.data
}