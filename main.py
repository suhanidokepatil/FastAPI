from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# Database (temporary dictionary)
students = {
    1: {
        "name": "Suhani",
        "age": 21,
        "Qualification": "Engg",
        "password": "12345"
    },
    2: {
        "name": "Rahul",
        "age": 22,
        "Qualification": "BCA",
        "password": "67890"
    },
    3: {
        "name": "Priya",
        "age": 20,
        "Qualification": "BSc",
        "password": "11111"
    }
}


# =========================
# REQUEST MODELS
# =========================

# Model for POST request
class Student(BaseModel):
    name: str
    age: int
    Qualification: str
    password: str



# Model for PUT request
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    Qualification: Optional[str] = None
    password: Optional[str] = None



# =========================
# RESPONSE MODEL
# =========================

# This decides what API will return
# Password will not be returned

class StudentResponse(BaseModel):
    name: str
    age: int
    Qualification: str



# Home API
@app.get("/")
def home():
    return {"message": "Hello World"}



# =========================
# GET with response_model
# =========================

@app.get(
    "/get-students/{students_id}",
    response_model=StudentResponse
)
def get_students(
    students_id: int = Path(..., description="ID of student")
):

    if students_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[students_id]



# Get student by name

@app.get(
    "/get-by-name",
    response_model=StudentResponse
)
def get_student(name: str):

    for student_id in students:

        if students[student_id]["name"].lower() == name.lower():
            return students[student_id]

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )



# =========================
# POST with response_model
# =========================

@app.post(
    "/create-student/{student_id}",
    response_model=StudentResponse
)
def create_student(student_id: int, student: Student):

    if student_id in students:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    students[student_id] = student.dict()

    return students[student_id]



# =========================
# PUT with response_model
# =========================

@app.put(
    "/update-student/{student_id}",
    response_model=StudentResponse
)
def update_student(student_id: int, student: UpdateStudent):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


    if student.name is not None:
        students[student_id]["name"] = student.name


    if student.age is not None:
        students[student_id]["age"] = student.age


    if student.Qualification is not None:
        students[student_id]["Qualification"] = student.Qualification


    if student.password is not None:
        students[student_id]["password"] = student.password


    return students[student_id]



# Delete API does not need response_model

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully"
    }