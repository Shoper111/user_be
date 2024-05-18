from bson import ObjectId

from user_be.schemas.product import Product
from user_be.schemas.product import ProductCreateSchema
from user_be.schemas.product import ProjectProduct


class ProductService:

    @staticmethod
    async def create_new(values: ProductCreateSchema, merchant_id: str) -> Product:
        return await Product(merchant_id=merchant_id, **values.dict()).insert()

    @staticmethod
    async def get_available_ids() -> list[str]:
        products = await Product.find().project(ProjectProduct).to_list()
        return [str(item.id) for item in products]

    @staticmethod
    async def get_by_id(product_id: str, merchant_id: str) -> Product:
        return await Product.find_one({'_id': ObjectId(product_id), 'merchant_id': merchant_id})

    @staticmethod
    async def get_products(merchant_id: str, limit: int, offset: int) -> list[Product]:
        cursor = Product.find(Product.merchant_id == merchant_id).limit(limit).skip(offset)
        return await cursor.to_list()

    async def update_by_id(self, product_id: str, merchant_id: str, data: ProductCreateSchema) -> Product:
        product = await self.get_by_id(product_id, merchant_id)
        await product.set(data.dict())
        return product

    async def delete_by_id(self, product_id: str, merchant_id: str) -> None:
        product = await self.get_by_id(product_id, merchant_id)
        await product.delete()
