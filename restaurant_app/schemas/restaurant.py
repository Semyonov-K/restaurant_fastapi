from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=2, max_length=500)


class DishCreate(MenuCreate):
    price: str = Field(..., min_length=1, max_length=50)
