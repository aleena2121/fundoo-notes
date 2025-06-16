from pydantic import BaseModel


class Label(BaseModel):
    title: str

    class Config:
        from_attributes = True
