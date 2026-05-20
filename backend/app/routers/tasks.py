from ..dependencies import get_current_user, get_db
from ..schemas.task import TaskCreateSchema, TaskResponseSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import Task, Project

router = APIRouter(
    prefix="/api", 
    tags=["api"]
)

# Get all tasks of a project
@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponseSchema])
async def get_all(project_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks

# Get a single task
@router.get("/projects/{project_id}/tasks/{id}", response_model=TaskResponseSchema)
async def get(project_id: int, id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = db.query(Task).filter(Task.id == id, Task.project_id == project_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Create a task
@router.post("/projects/{project_id}/tasks", response_model=TaskResponseSchema)
async def create(project_id: int, task: TaskCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    new_task = Task(
        title = task.title,
        priority = task.priority,
        due_date = task.due_date,
        assignee_id=current_user.id,
        project_id = project_id,
        status = "todo"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Update a task
@router.put("/projects/{project_id}/tasks/{id}")
async def update(project_id: int, id: int, task:TaskCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task_updated = db.query(Task).filter(Task.id == id, Task.project_id == project_id).first()
    if not task_updated:
        raise HTTPException(status_code=404, detail="Task not found")
    task_updated.title = task.title
    task_updated.priority = task.priority
    task_updated.due_date = task.due_date
    db.commit()
    db.refresh(task_updated)
    return {"message": "Task updated"}
    

# Delete a task
@router.delete("/projects/{project_id}/tasks/{id}")
async def delete(project_id: int, id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = db.query(Task).filter(Task.id == id, Task.project_id == project_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}