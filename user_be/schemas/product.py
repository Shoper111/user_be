from datetime import datetime
from datetime import timedelta

from beanie import Document
from beanie import Indexed
from beanie import PydanticObjectId
from pydantic import BaseModel
from pydantic import Field


class ProductCreateSchema(BaseModel):
    name: str
    description: str | None
    content: str
    images: list[str]
    quantity: int
    price: float


class Product(Document, ProductCreateSchema):
    merchant_id: Indexed(str)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'products'
        use_cache = True
        cache_expiration_time = timedelta(minutes=60)
        cache_capacity = 5


class ProjectProduct(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
