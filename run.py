from pathlib import Path

from sdx_base.run import run
from sdx_base.settings.app import AppSettings

from app.routes import router

if __name__ == '__main__':
    proj_root = Path(__file__).parent  # sdx-transformer dir
    run(AppSettings, routers=[router], proj_root=proj_root)
