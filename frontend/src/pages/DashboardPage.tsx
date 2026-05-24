import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProjects } from '../api/projects'

const Dashboard = () => {
    const navigate = useNavigate()
    const { data: projects, isLoading, isError } = useQuery({
      queryKey: ['projects'],
      queryFn: getProjects
    })
  
    if (isLoading) return (
      <div className="flex items-center justify-center h-screen text-gray-500">
        Loading projects...
      </div>
    )
  
    if (isError) return (
      <div className="flex items-center justify-center h-screen text-red-500">
        Failed to load projects. Is the backend running?
      </div>
    )
  
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-800">Projects</h1>
          <button
            onClick={() => navigate('/projects/new')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors"
          >
            + New Project
          </button>
        </header>
  
        <main className="px-8 py-6">
          {projects.length === 0 ? (
            <div className="text-center py-20 text-gray-400">
              <p className="text-lg">No projects yet</p>
              <p className="text-sm mt-1">Create one to get started</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project: Project) => (
                <div
                  key={project.id}
                  onClick={() => navigate(`/projects/${project.id}`)}
                  className="bg-white rounded-xl border border-gray-200 p-5 cursor-pointer hover:shadow-md hover:border-blue-300 transition-all"
                >
                  <h2 className="font-medium text-gray-800">{project.title}</h2>
                  {project.description && (
                    <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                      {project.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    )
  }

export default Dashboard