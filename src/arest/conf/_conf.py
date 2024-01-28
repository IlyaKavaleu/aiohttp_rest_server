import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()

DEBUG = True
if DEBUG:
    LOGGER = "dev"
    EXP_TIME = 60 * 60 * 24
else:
    LOGGER = "prod"
    EXP_TIME = 120
DATABASE = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': '@format {this.DB_HOST}',
                'port': 5432,
                'user': '@format {this.DB_USER}',
                'password': '@format {this.DB_PASS}',
                'database': '@format {this.DB_NAME}',
            },
        }
    },
    'apps': {
        'account': {
            'models': ['src.arest.api.account.models', 'aerich.models'],
            'default_connection': 'default'
        },
    },
    'use_tz': False,
    'timezone': 'UTC',
}

