from fastapi import FastAPI
from routes.employee import user as employee_router

app = FastAPI()

app.include_router(employee_router, prefix="/employees")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}
