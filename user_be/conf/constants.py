from user_be.conf import settings

JWT_ACCESS_TOKEN_ALGORITHMS = ['RS256']
AWS_COGNITO_URL = f'https://cognito-idp.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{settings.COGNITO_POOL_ID}'
JWK_URL = '/'.join([AWS_COGNITO_URL.rstrip('/'), '.well-known/jwks.json'])


class ErrorMessages:
    TOKEN_TYPE_IS_NOT_VALID = 'Token type is not valid.'
    TOKEN_INVALID = 'Token is invalid.'
    TOKEN_EXPIRED = 'Token expired.'
    DO_NOT_HAVE_PERMISSIONS = 'You don\'t have permission.'
    OBJECT_NOT_FOUND = '{object_type} with ID {id} not found.'
