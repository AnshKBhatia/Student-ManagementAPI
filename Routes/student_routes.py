from fastapi import APIRouter, Depends, HTTPException, Query
from models import Student
from database import get_students_collection
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

# POST route to create a student
@router.post("/students", status_code=201)
async def create_student(
    student: Student,
    students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):

    student_data = student.dict()
    try:
        result = await students_collection.insert_one(student_data)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET route to list students with optional filters
@router.get("/students", status_code=200)
async def list_students(
    country: Optional[str] = Query(None, description="Filter students by country"),
    age: Optional[int] = Query(None, description="Filter students with age >= this value"),
    students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):

    # Build the query dynamically based on the filters
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    try:
        # Query the database
        cursor = students_collection.find(query, {"_id": 0, "name": 1, "age": 1})
        students = await cursor.to_list(length=None)

        return {"data": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



# GET route to fetch a student by ID
@router.get("/students/{id}", status_code=200)
async def fetch_student(
    id: str,
    students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):

    try:
        # Validate and convert the ID
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")

        # Fetch the student document from the database
        student = await students_collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Remove the `_id` field and return the result
        student.pop("_id")
        return student

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# GET route to fetch a student by ID
@router.get("/students/{id}", status_code=200)
async def fetch_student(
        id: str,
        students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):

    try:
        # Validate and convert the ID
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")

        # Fetch the student document from the database
        student = await students_collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Remove the _id field and return the result
        student.pop("_id")
        return student

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# PATCH route to update a student by ID
@router.patch("/students/{id}", status_code=200)
async def update_student(
        id: str,
        student: Student,
        students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):
    try:
        # Validate and convert the ID
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")

        update_data = student.dict(exclude_unset=True)
        result = await students_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# DELETE route to delete a student by ID
@router.delete("/students/{id}", status_code=204)
async def delete_student(
        id: str,
        students_collection: AsyncIOMotorCollection = Depends(get_students_collection)
):
    try:
        # Validate and convert the ID
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")

        result = await students_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
