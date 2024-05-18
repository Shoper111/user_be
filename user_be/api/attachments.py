from http import HTTPStatus

from fastapi import APIRouter
from fastapi import UploadFile

from user_be.api.dependencies.logger import LoggingRoute
from user_be.clients import aws_s3_client
from user_be.schemas.attachment import Attachment

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '',
    summary='Make new attachment',
    status_code=HTTPStatus.CREATED,
    response_model=Attachment,
)
async def upload_attachments(file: UploadFile) -> Attachment:
    url = await aws_s3_client.save_file(file)
    return Attachment(url=str(url))
