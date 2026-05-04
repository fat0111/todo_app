from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import todo, auth

app = FastAPI(
    title="To-do App API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router)
app.include_router(auth.router)
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running smoothly!"}

@app.get("/")
def root():
    return {"message": "Chào mừng đến với To-do App!"}