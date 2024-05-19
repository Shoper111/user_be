from fastapi import APIRouter
from fastapi import Depends

from user_be.api.dependencies.auth import auth_user
from user_be.api.dependencies.logger import LoggingRoute
from user_be.api.dependencies.services import get_order_service
from user_be.schemas import Order
from user_be.schemas.order import CreateOrder
from user_be.schemas.order import OrderInfoSchema
from user_be.schemas.order import UpdateOrder
from user_be.services.order import OrderService

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '/public',
    summary='Create new order',
    response_model=OrderInfoSchema,
)
async def create_new_order(
        request_data: CreateOrder,
        order_service: OrderService = Depends(get_order_service),
) -> OrderInfoSchema:
    return await order_service.create_new(request_data)


@router.get(
    '',
    summary='Get orders list',
    response_model=list[OrderInfoSchema],
)
async def get_order_list(
        limit: int = 10,
        offset: int = 0,
        merchant_id: str = Depends(auth_user),
        order_service: OrderService = Depends(get_order_service),
) -> list[OrderInfoSchema]:
    return await order_service.get_by_merchant_id(merchant_id, limit, offset)


@router.get(
    '/available-ids',
    summary='Get available orders ids',
    response_model=list[str],
)
async def get_available_order_ids(
        order_service: OrderService = Depends(get_order_service),
) -> list[str]:
    return await order_service.get_available_ids()


@router.get(
    '/{order_id}',
    summary='Get order by id',
    response_model=Order,
)
async def get_order_by_id(
        order_id: str,
        merchant_id: str = Depends(auth_user),
        order_service: OrderService = Depends(get_order_service),
) -> Order:
    return await order_service.get_by_id(order_id, merchant_id)


@router.patch(
    '/{order_id}',
    summary='Update order by id',
    response_model=Order,
)
async def update_order(
        order_id: str,
        request_data: UpdateOrder,
        merchant_id: str = Depends(auth_user),
        order_service: OrderService = Depends(get_order_service),
) -> Order:
    return await order_service.update_by_id(order_id, merchant_id, request_data)
