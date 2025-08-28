from pydantic import BaseModel

class TagModel(BaseModel):
    """id & name as in db"""
    id: int
    name: str