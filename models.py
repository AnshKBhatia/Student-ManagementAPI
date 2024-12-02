from pydantic import BaseModel
from typing import Optional, Dict

class Student(BaseModel):
    name: str
    age: int
    address: Dict[str, str]  # For example, using a dictionary to store address fields
