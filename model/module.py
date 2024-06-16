from typing import Optional

from pydantic import BaseModel, Field


class Module(BaseModel):
    title: str = Field(...)
    created_date: str = Field(...)
    last_accessed: str = Field(...)
    is_deleted: bool = Field(default=False)
    notes: Optional[list] = Field(default=[])


def get_module_schema(module):
    return {
        "_id": str(module["_id"]),
        "title": module["title"],
        "created_date": module["created_date"],
        "last_accessed": module["last_accessed"]
    }

class DeleteModuleRequest(BaseModel):
    user_id: str
    module_id: str
    
