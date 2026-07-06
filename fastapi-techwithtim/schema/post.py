from pydantic import BaseModel

class Posts(BaseModel):
    title : str
    description : str