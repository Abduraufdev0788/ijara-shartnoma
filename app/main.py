from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import students, groups, courses

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(groups.router)
app.include_router(students.router)

@app.get("/" )
async def read_root():
    return {"message": "Welcome to the University Management API"}