from datetime import datetime
from enum import Enum

from beanie import Document
from beanie import Indexed
from beanie import Link
from beanie import PydanticObjectId
from pydantic import BaseModel
from pydantic import Field

from user_be.schemas.product import Product
from user_be.schemas.product import ShippingMethod


class OrderStatus(str, Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELLED'


class OrderUser(BaseModel):
    name: str
    phone: str


class CreateOrder(BaseModel):
    user: OrderUser
    shipping_method: ShippingMethod
    shipping_options: dict
    comment: str
    products: list[str]
    quantity: int
    merchant_id: Indexed(str)


class Order(CreateOrder, Document):
    products: list[Link[Product]]
    status: OrderStatus = Field(default=OrderStatus.NEW)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'orders'


class OrderInfoSchema(Order):
    _id: PydanticObjectId


class ProjectOrder(BaseModel):
    id: PydanticObjectId = Field(alias='_id')


class UpdateOrder(BaseModel):
    status: OrderStatus
