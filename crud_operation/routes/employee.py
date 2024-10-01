from fastapi import APIRouter, HTTPException
from models.model import Employee
from schemas.serializer import user_entity, user_entities
from config.db import conn
from bson import ObjectId

user = APIRouter()

@user.post('/')
async def create_employee(emp: Employee):
    emp_dict = emp.dict()
    emp_dict['_id'] = ObjectId()  # Generate a new ObjectId
    conn.user.insert_one(emp_dict)
    return user_entity(conn.user.find_one({"_id": emp_dict['_id']}))

@user.get("/")
async def list():
    return user_entities(conn.user.find())

@user.put('/{id}')
async def update(id: str, emp: Employee):
    updated_employee = conn.user.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": emp.dict()},
        return_document=True
    )
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return user_entity(updated_employee)

@user.delete("/{id}")
async def delete_user(id: str):
    user = conn.user.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")
    conn.user.find_one_and_delete({"_id": ObjectId(id)})
    return user_entity(user)
