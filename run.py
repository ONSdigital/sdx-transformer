from app import sdx_app
from app.routes import init_routes

if __name__ == '__main__':
    init_routes(sdx_app)
    sdx_app.run(port=5000)
