from pydantic import AnyHttpUrl
from pydantic import BaseModel


class Attachment(BaseModel):
    url: AnyHttpUrl
