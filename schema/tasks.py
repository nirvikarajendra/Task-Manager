from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskModel(BaseModel):
    title : str =  Field(min_length=3, max_length=100)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0, lt=6)
    complete : bool
    due_date : Optional[datetime]

