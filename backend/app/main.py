from fastapi import FastAPI, Depends
from .routers import auth, projects, tasks
import uvicorn
from .dependencies import get_current_user
from .models import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TaskBoard API",
    description="A simple API for managing tasks and projects",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)