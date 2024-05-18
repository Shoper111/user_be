from pydantic import BaseModel


class MerchantSchema(BaseModel):
    sub: str
    family_name: str
    given_name: str
    email: str
