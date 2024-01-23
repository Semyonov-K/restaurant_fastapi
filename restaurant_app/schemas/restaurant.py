from pydantic import BaseModel, Field


class SubMenuCRU(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=2, max_length=500)


class DishCRU(SubMenuCRU):
    price: str = Field(..., min_length=1, max_length=50)


class SubMenuResponse(SubMenuCRU):
    id: int
    # id: int
    
    # @property
    # def id(self) -> str:
    #     return str(self.id)
    
    # class Config:
    #     orm_mode = True
