from waitress import serve

from app import sdx_app
from app.routes import init_routes

if __name__ == '__main__':
    init_routes(sdx_app)
    def new_run(self, port: int = 5000):
        """Start the server"""
        print("hi")
        serve(self.app, host='0.0.0.0', port=port, channel_timeout=300, inactivity=300)


    sdx_app.run = new_run
    sdx_app.run(sdx_app, port=5000)
