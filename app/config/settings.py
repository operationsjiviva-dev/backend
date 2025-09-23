import os
from decouple import config as env_config

# AWS
AWS_S3_KEY = env_config('AWS_S3_KEY', cast=str)
AWS_S3_SECRET = env_config('AWS_S3_SECRET', cast=str)