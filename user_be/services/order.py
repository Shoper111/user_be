from bson import ObjectId

from user_be.schemas import Order
from user_be.schemas.order import CreateOrder
from user_be.schemas.order import OrderInfoSchema
from user_be.schemas.order import ProjectOrder
from user_be.schemas.order import UpdateOrder


class OrderService:

    @staticmethod
    async def create_new(order_data: CreateOrder) -> OrderInfoSchema:
        return await Order(**order_data.dict()).insert()

    @staticmethod
    async def get_by_merchant_id(merchant_id: str, limit: int, offset: int) -> list[OrderInfoSchema]:
        orders = Order.find(Order.merchant_id == merchant_id, fetch_links=True).limit(limit).skip(offset)
        return await orders.to_list()

    @staticmethod
    async def get_available_ids() -> list[str]:
        orders = await Order.find().project(ProjectOrder).to_list()
        return [str(item.id) for item in orders]

    @staticmethod
    async def get_by_id(order_id: str, merchant_id: str) -> Order:
        return await Order.find_one(
            {'_id': ObjectId(order_id), 'merchant_id': merchant_id},
            fetch_links=True,
        )

    async def update_by_id(self, order_id: str, merchant_id: str, data: UpdateOrder) -> Order:
        order = await self.get_by_id(order_id, merchant_id)
        await order.set(data.dict())
        return order
