from user_be.clients.cognito import CognitoClient
from user_be.clients.s3 import AWSS3Client

aws_s3_client = AWSS3Client()
aws_cognito_client = CognitoClient()
