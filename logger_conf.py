
LOGGER = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s ',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
        }
    }
}