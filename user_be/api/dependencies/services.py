from user_be.services.product import ProductService


async def get_product_service() -> ProductService:
    return ProductService()
