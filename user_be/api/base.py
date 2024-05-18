from http import HTTPStatus

from user_be.schemas.base import HealthSchema
from user_be.schemas.base import VersionSchema
from fastapi import APIRouter
from fastapi import Request

router = APIRouter()


@router.get(
    '/health',
    summary='Health check',
    status_code=HTTPStatus.OK,
    response_model=HealthSchema,
    responses={
        200: {'model': HealthSchema},
        500: {'model': HealthSchema},
    }
)
async def health() -> HealthSchema:
    """Shows status of the server"""
    return HealthSchema(db=True)


@router.get(
    '/version',
    summary='API version',
    response_model=VersionSchema,
)
async def version(request: Request) -> VersionSchema:
    """Get Companion API version"""
    return VersionSchema(version=request.app.version)
