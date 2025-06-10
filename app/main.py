import sys

import uvicorn

from app.config import settings
from app.config.logger import config_logger
from app.f_api import app
from app.utils.exceptions import RequiredEnvVarError

if __name__ == "__main__":
    config_logger = config_logger
    try:
        uvicorn.run("app.f_api:app", 
                    host=settings.UVICORN_HOST, 
                    port=settings.UVICORN_PORT, 
                    reload= True)
    except RequiredEnvVarError as e:
        print(f"Configuration error: {str(e)}", file=sys.stderr)
        sys.exit(1)
