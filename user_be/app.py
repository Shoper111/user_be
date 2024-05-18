from fastapi import FastAPI

from user_be import __version__
from user_be.api import attachments
from user_be.api import base
from user_be.api import products
from user_be.clients import aws_cognito_client
from user_be.clients import aws_s3_client
from user_be.conf import settings
from user_be.conf.mongodb import init_mongodb
from user_be.conf.sentry import init_sentry
from user_be.conf.settings import Env
from user_be.conf.settings import Settings
from user_be.exception_handlers import init_exception_handlers
from user_be.middlewares import init_middlewares


def init_routes(app: 'FastAPI') -> None:
    app.include_router(base.router, tags=['Base'], prefix='/api')
    app.include_router(products.router, tags=['Products'], prefix='/api/products')
    app.include_router(attachments.router, tags=['Attachments'], prefix='/api/attachments')


def create_app(app_settings: Settings = None):
    """Create app with including configurations"""
    app_settings = app_settings if app_settings is not None else settings
    init_sentry(app_settings, version=__version__)
    is_production = app_settings.ENV == Env.PRODUCTION
    app = FastAPI(
        title='Crafter',
        debug=app_settings.DEBUG,
        docs_url='/docs' if not is_production else None,
        redoc_url='/redoc' if not is_production else None,
        version=__version__,
    )
    init_middlewares(app)
    init_exception_handlers(app)
    init_routes(app)

    @app.on_event('startup')
    async def startup():
        await init_mongodb(settings)
        await aws_s3_client.configure()
        await aws_cognito_client.configure()

    @app.on_event('shutdown')
    async def shutdown():
        await aws_s3_client.close()
        await aws_cognito_client.close()

    return app
