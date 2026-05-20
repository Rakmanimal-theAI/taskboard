from ..dependencies import get_current_user, get_db
from ..schemas.project import ProjectCreateSchema, ProjectResponseSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import Project

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
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# Update a project
@router.put("/projects/{id}")
async def update(id: int, project:ProjectCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project_updated = db.query(Project).filter(Project.id == id, Project.owner_id == current_user.id).first()
    if not project_updated:
        raise HTTPException(status_code=404, detail="Project not found")
    project_updated.title = project.title
    db.commit()
    db.refresh(project_updated)
    return {"message": "Project updated"}
    

# Delete a project
@router.delete("/projects/{id}")
async def delete(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}