from fastapi import FastAPI
from Routes.student_routes import router as student_router

# Create the FastAPI app
app = FastAPI()

# Include student router with a cleaner prefix
app.include_router(student_router, prefix="/api/students")

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Management API"}
