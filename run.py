from app import sdx_app
from app.routes import transform


if __name__ == '__main__':
    sdx_app.add_post_endpoint(transform, rule="/transform")
    sdx_app.run(port=5000)
