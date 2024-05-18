import logging

from user_be.clients.aws import AWSClient
from user_be.conf import settings
from user_be.schemas.merchant import MerchantSchema

logger = logging.getLogger(__name__)


class CognitoClient(AWSClient):
    CLIENT_TYPE = 'cognito-idp'

    async def get_user(self, access_token: str) -> MerchantSchema:
        async with self.session.client(
                'cognito-idp',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_DEFAULT_REGION,
        ) as client:
            user_data = await client.get_user(AccessToken=access_token)
            attributes = {attr['Name']: attr['Value'] for attr in user_data['UserAttributes']}
            if not attributes.get('name'):
                attributes['name'] = attributes['email'].split('@')[0]
            return MerchantSchema(**attributes)
