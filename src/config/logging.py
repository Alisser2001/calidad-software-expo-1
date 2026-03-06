from logging.config import dictConfig

def setup_logging() -> None:
    plain_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "format": plain_format
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "plain",
                "level": "INFO"
            },
            "console_error": {
                "class": "logging.StreamHandler",
                "formatter": "plain",
                "level": "ERROR"
            },
            "file": { 
                "class": "logging.FileHandler",
                "formatter": "plain",
                "level": "INFO",
                "filename": "info.log",  
                "mode": "a",            
                "encoding": "utf-8"
            },
            "file-error": { 
                "class": "logging.FileHandler",
                "formatter": "plain",
                "level": "ERROR",
                "filename": "error.log",  
                "mode": "a",            
                "encoding": "utf-8"
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console_error", "file-error"],
                "level": "ERROR",
                "propagate": False,
            }
        }
    })
