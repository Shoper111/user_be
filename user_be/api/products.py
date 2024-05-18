from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from user_be.api.dependencies.auth import auth_user
from user_be.api.dependencies.logger import LoggingRoute
from user_be.api.dependencies.services import get_product_service
from user_be.schemas.product import Product
from user_be.schemas.product import ProductCreateSchema
from user_be.services.product import ProductService

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '',
    summary='Create new product',
    status_code=HTTPStatus.CREATED,
    response_model=Product,
)
async def create_new_product(
        request_data: ProductCreateSchema,
        merchant_id: str = Depends(auth_user),
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.create_new(request_data, merchant_id)


@router.get(
    '',
    summary='Get products list',
    status_code=HTTPStatus.CREATED,
    response_model=list[Product],
)
async def get_product_list(
        limit: int = Query(10),
        offset: int = Query(0),
        merchant_id: str = Depends(auth_user),
        product_service: ProductService = Depends(get_product_service),
) -> list[Product]:
    return await product_service.get_products(merchant_id, limit, offset)


@router.get(
    '/available-ids',
    summary='Get available products ids',
    response_model=list[str],
)
async def get_available_product_ids(
        product_service: ProductService = Depends(get_product_service),
) -> list[str]:
    return await product_service.get_available_ids()


@router.get(
    '/{product_id}',
    summary='Get product by id',
    response_model=Product,
)
async def get_product_by_id(
        product_id: str,
        merchant_id: str = Depends(auth_user),
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.get_by_id(product_id, merchant_id)


@router.patch(
    '/{product_id}',
    summary='Update product by id',
    response_model=Product,
)
async def update_product_by_id(
        product_id: str,
        data: ProductCreateSchema,
        merchant_id: str = Depends(auth_user),
        product_service: ProductService = Depends(get_product_service),
) -> Product:
    return await product_service.update_by_id(product_id, merchant_id, data)


@router.delete(
    '/{product_id}',
    summary='Delete product by id',
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
)
async def delete_product_by_id(
        product_id: str,
        merchant_id: str = Depends(auth_user),
        product_service: ProductService = Depends(get_product_service),
) -> None:
    await product_service.delete_by_id(product_id, merchant_id)
