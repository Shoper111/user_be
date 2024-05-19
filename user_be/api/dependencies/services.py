from user_be.services.order import OrderService
from user_be.services.product import ProductService


async def get_product_service() -> ProductService:
    return ProductService()


async def get_order_service() -> OrderService:
    return OrderService()
