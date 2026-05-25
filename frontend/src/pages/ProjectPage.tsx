import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getProject, summariseProject } from '../api/projects'
import { getTasks, updateTask, createTask, deleteTask } from '../api/tasks'
import type { TaskResponse, TaskCreate } from '../api/tasks'

import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import type {
  DragEndEvent, DragStartEvent
} from '@dnd-kit/core'
import { useDroppable, useDraggable } from '@dnd-kit/core'

// --- Types ---
type TaskStatus = 'todo' | 'in_progress' | 'done'

const COLUMNS: { id: TaskStatus; label: string }[] = [
  { id: 'todo', label: 'To Do' },
  { id: 'in_progress', label: 'In Progress' },
  { id: 'done', label: 'Done' },
]

// --- TaskCard component ---
const TaskCard = ({ task, onDelete }: { task: TaskResponse; onDelete: (id: number) => void }) => {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({ id: task.id })

  const style = transform
    ? { transform: `translate(${transform.x}px, ${transform.y}px)`, opacity: isDragging ? 0.4 : 1 }
    : undefined

  const priorityColor: Record<string, string> = {
    low: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-red-100 text-red-700',
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="bg-white rounded-lg border border-gray-200 p-3 shadow-sm cursor-grab active:cursor-grabbing flex flex-col gap-2"
    >
      <p className="text-sm font-medium text-gray-800">{task.title}</p>
      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${priorityColor[task.priority] ?? 'bg-gray-100 text-gray-600'}`}>
          {task.priority}
        </span>
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(task.id) }}
          className="text-gray-300 hover:text-red-400 text-xs transition-colors"
        >
          ✕
        </button>
      </div>
      {task.due_date && (
        <p className="text-xs text-gray-400">Due {new Date(task.due_date).toLocaleDateString()}</p>
      )}
    </div>
  )
}

// --- Column component ---
const Column = ({
  id, label, tasks, onDelete
}: {
  id: TaskStatus
  label: string
  tasks: TaskResponse[]
  onDelete: (id: number) => void
}) => {
  const { setNodeRef, isOver } = useDroppable({ id })

  return (
    <div className={`flex flex-col gap-3 bg-gray-100 rounded-xl p-4 transition-colors ${isOver ? 'bg-blue-50' : ''}`}>
      <div className="flex items-center justify-between mb-1">
        <h2 className="font-semibold text-gray-700 text-sm">{label}</h2>
        <span className="text-xs bg-gray-200 text-gray-500 rounded-full px-2 py-0.5">{tasks.length}</span>
      </div>
      {/* This div is the actual droppable zone — must always take up space */}
      <div ref={setNodeRef} className="flex flex-col gap-3 flex-1 min-h-[300px]">
        {tasks.map(task => (
          <TaskCard key={task.id} task={task} onDelete={onDelete} />
        ))}
      </div>
    </div>
  )
}

// --- New Task Form ---
const NewTaskForm = ({ onSubmit, loading }: { onSubmit: (data: TaskCreate) => void; loading: boolean }) => {
  const [title, setTitle] = useState('')
  const [priority, setPriority] = useState('medium')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return
    onSubmit({ title, priority })
    setTitle('')
    setPriority('medium')
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-center">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task title..."
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
        className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors disabled:opacity-50"
      >
        {loading ? 'Adding...' : '+ Add Task'}
      </button>
    </form>
  )
}

// --- Main ProjectPage ---
const ProjectPage = () => {
  const { id } = useParams<{ id: string }>()
  const projectId = Number(id)
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [activeTask, setActiveTask] = useState<TaskResponse | null>(null)

  const [summary, setSummary] = useState<string | null>(null)
  const [summarising, setSummarising] = useState(false)

  const sensors = useSensors(useSensor(PointerSensor, {
    activationConstraint: { distance: 5 }
  }))

  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => getProject(projectId)
  })

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks', projectId],
    queryFn: () => getTasks(projectId)
  })

  const updateMutation = useMutation({
    mutationFn: ({ taskId, data }: { taskId: number; data: TaskCreate }) =>
      updateTask(projectId, taskId, data),
    onSuccess: () => {
      console.log('update success')
      queryClient.invalidateQueries({ queryKey: ['tasks', projectId] })
    },
    onError: (error) => {
      console.log('update error:', error)
    }
  })
  
  const createMutation = useMutation({
    mutationFn: (data: TaskCreate) => createTask(projectId, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tasks', projectId] })
  })

  const deleteMutation = useMutation({
    mutationFn: (taskId: number) => deleteTask(projectId, taskId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tasks', projectId] })
  })

  const handleDragStart = (event: DragStartEvent) => {
    const task = tasks.find(t => t.id === event.active.id)
    if (task) setActiveTask(task)
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    console.log('drag end:', { activeId: active.id, overId: over?.id })
    setActiveTask(null)
    if (!over) return
  
    const task = tasks.find(t => t.id === active.id)
    console.log('found task:', task)
  
    if (!task) return
  
    const validStatuses: TaskStatus[] = ['todo', 'in_progress', 'done']
    let newStatus: TaskStatus
  
    if (validStatuses.includes(over.id as TaskStatus)) {
      newStatus = over.id as TaskStatus
    } else {
      const overTask = tasks.find(t => t.id === over.id)
      if (!overTask) return
      newStatus = overTask.status as TaskStatus
    }
  
    console.log('status change:', { from: task.status, to: newStatus })
  
    //if (task.status === newStatus) return
  
    console.log('calling updateMutation')
    updateMutation.mutate({
      taskId: task.id,
      data: { title: task.title, priority: task.priority, status: newStatus }
    })
  }

  const handleSummarise = async () => {
    setSummarising(true)
    setSummary(null)
    try {
      const result = await summariseProject(projectId)
      setSummary(result.summary)
    } catch (error: any) {
      const detail = error?.response?.data?.detail
      setSummary(`Error: ${detail ?? error?.message ?? 'Unknown error'}`)
    } finally {
      setSummarising(false)
    }
  }

  const tasksByStatus = (status: TaskStatus) => tasks.filter(t => t.status === status)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-8 py-4">
        <div className="flex items-center gap-4 justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-500 hover:text-gray-800 transition-colors"
            >
              ← Back
            </button>
            <div>
              <h1 className="text-xl font-semibold text-gray-800">{project?.title}</h1>
              {project?.description && (
                <p className="text-sm text-gray-500">{project.description}</p>
              )}
            </div>
          </div>
          <button
            onClick={handleSummarise}
            disabled={summarising}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {summarising ? 'Summarising...' : '✨ Summarise project'}
          </button>
        </div>
        {summary && (
          <div className="mt-3 bg-purple-50 border border-purple-200 rounded-lg px-4 py-3 text-sm text-gray-700">
            {summary}
          </div>
        )}
      </header>

      <main className="px-8 py-6 flex flex-col gap-6">
        <NewTaskForm onSubmit={(data) => createMutation.mutate(data)} loading={createMutation.isPending} />

        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-3 gap-4">
            {COLUMNS.map(col => (
              <Column
                key={col.id}
                id={col.id}
                label={col.label}
                tasks={tasksByStatus(col.id)}
                onDelete={(taskId) => deleteMutation.mutate(taskId)}
              />
            ))}
          </div>
          <DragOverlay>
            {activeTask && (
              <div className="bg-white rounded-lg border border-blue-300 p-3 shadow-lg text-sm font-medium text-gray-800">
                {activeTask.title}
              </div>
            )}
          </DragOverlay>
        </DndContext>
      </main>
    </div>
  )
}

export default ProjectPage