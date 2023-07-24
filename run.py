from app import sdx_app
from app.routes import process_pck, process_prepop

if __name__ == '__main__':
    sdx_app.add_post_endpoint(process_pck, rule="/pck")
    sdx_app.add_post_endpoint(process_prepop, rule="/prepop")
    sdx_app.run(port=5000)
