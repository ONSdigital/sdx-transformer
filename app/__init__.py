import os

from sdx_gcp.app import SdxApp


PROJECT_ID = os.getenv('PROJECT_ID')
sdx_app = SdxApp("sdx-transform", PROJECT_ID)
