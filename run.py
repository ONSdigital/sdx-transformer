from waitress import serve

from app import sdx_app
from app.routes import init_routes

if __name__ == '__main__':
    init_routes(sdx_app)
    serve(sdx_app.app, host='0.0.0.0', port='5000')
