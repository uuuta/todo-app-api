import logging
import logging.config

from config import settings

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s() L%(lineno)d: %(message)s"},
        "default": {"format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s() L%(lineno)d: %(message)s"},
        "access": {"format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s() L%(lineno)d: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": settings.log_level.upper(),
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "level": settings.log_level.upper(),
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "error": {
            "level": settings.log_level.upper(),
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "app": {
            "level": settings.log_level.upper(),
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": settings.log_level.upper(),
            "handlers": ["access"],
        },
        "uvicorn.error": {
            "level": settings.log_level.upper(),
            "handlers": ["error"],
        },
    },
    "root": {  # root logger (default)
        "level": settings.log_level_default.upper(),
        "handlers": ["default"],
        "propagate": False,
    }
}

logging.config.dictConfig(logging_config)


def get_logger(name: str = None) -> logging:
    if not name:
        return logging.getLogger("app")
    return logging.getLogger(name)
