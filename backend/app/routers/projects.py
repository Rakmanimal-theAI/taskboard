from ..dependencies import get_current_user, get_db
from ..schemas.project import ProjectCreateSchema, ProjectResponseSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Project, Task
import httpx

router = APIRouter(
    prefix="/api", 
    tags=["api"]
)

# Get all projects
@router.get("/projects", response_model=list[ProjectResponseSchema])
async def get_all(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects

# Get a single project
@router.get("/projects/{id}", response_model=ProjectResponseSchema)
async def get(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.owner_id == current_user.id, Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Create a project
@router.post("/projects", response_model=ProjectResponseSchema)
async def create(project: ProjectCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_project = Project(
        title = project.title,
        owner_id=current_user.id,
        description = project.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Update a project
@router.put("/projects/{id}", response_model=ProjectResponseSchema)
async def update(id: int, project:ProjectCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project_updated = db.query(Project).filter(Project.id == id, Project.owner_id == current_user.id).first()
    if not project_updated:
        raise HTTPException(status_code=404, detail="Project not found")
    project_updated.title = project.title
    project_updated.description = project.description
    db.commit()
    db.refresh(project_updated)
    return project_updated
    

# Delete a project
@router.delete("/projects/{id}")
async def delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}

@router.post("/projects/{id}/summary")
async def summarise_project(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = db.query(Task).filter(Task.project_id == id).all()
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks to summarise")

    task_lines = "\n".join([f"- [{t.status}] {t.title} (priority: {t.priority})" for t in tasks])
    prompt = f"""You are a project manager assistant. Summarise the following tasks for project "{project.title}" in 2-3 sentences. Be concise and focus on overall progress and any concerns.

Tasks:
{task_lines}"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://host.docker.internal:11434/api/generate",  # <- fix here
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return {"summary": result["response"]}
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot reach Ollama — is it running on the host?")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama timed out — model may still be loading")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")