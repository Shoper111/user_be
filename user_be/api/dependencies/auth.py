import logging
from http import HTTPStatus
from typing import Dict, Any, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from user_be.conf.constants import JWK_URL, JWT_ACCESS_TOKEN_ALGORITHMS, AWS_COGNITO_URL

logger = logging.getLogger(__name__)

oauth2_scheme = HTTPBearer()
jwk_client = jwt.PyJWKClient(JWK_URL, cache_keys=True)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def get_access_token(authorization: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme)) -> str:
    if not authorization:
        raise _unauthorized()
    return authorization.credentials


def get_jwk_key(token: str = Depends(get_access_token)) -> jwt.PyJWK:
    try:
        return jwk_client.get_signing_key_from_jwt(token)
    except jwt.PyJWTError:
        raise _unauthorized()


def validate_access_token(
        token: str = Depends(get_access_token),
        jwk_key: jwt.PyJWK = Depends(get_jwk_key),
) -> Dict[str, Any]:
    unauthorized_exc = _unauthorized()

    try:
        token_data = jwt.decode(
            token,
            jwk_key.key,
            algorithms=JWT_ACCESS_TOKEN_ALGORITHMS,
            options={'verify_signature': False,
                     'verify_exp': False,
                     'require': ['sub', 'exp', 'iss', 'token_use']}
        )
        if token_data.get('iss') != AWS_COGNITO_URL:
            logger.warning('Invalid "iss" claim')
            raise unauthorized_exc
        if token_data.get('token_use') != 'access':
            logger.warning('Invalid "token_use" claim')
            raise unauthorized_exc

    except jwt.InvalidTokenError as err:
        logger.warning(err)
        raise unauthorized_exc

    else:
        return token_data


async def auth_user(token_payload: Dict[str, Any] = Depends(validate_access_token)) -> str:
    return token_payload['sub']
