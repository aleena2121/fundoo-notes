import sys

import uvicorn

from app.config.settings import appSettings
from app.f_api import app
from app.utils.exceptions import RequiredEnvVarError

if __name__ == "__main__":
    try:
        uvicorn.run(
            "app.f_api:app",
            host=appSettings.UVICORN_HOST,
            port=appSettings.UVICORN_PORT,
            reload=True,
        )
    except RequiredEnvVarError as e:
        print(f"Configuration error: {str(e)}", file=sys.stderr)
        sys.exit(1)
