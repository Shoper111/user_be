import logging

import sentry_sdk

from user_be.conf import settings, Settings

logger = logging.getLogger(__name__)


def init_sentry(app_settings: Settings, version: str) -> None:
    try:
        if settings.SENTRY_DSN and not settings.ENV == 'LOCAL':
            sentry_sdk.init(
                settings.SENTRY_DSN,
                traces_sample_rate=1.0,
                release=version,
                environment=app_settings.ENV,
            )
        else:
            logger.warning('Sentry integration not configured. To configure set SENTRY_DSN environment variable')

    except Exception as err:
        logger.exception(err)
