
from fastapi.staticfiles import StaticFiles

def init_static_files(app):
    app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")
    app.mount("/js", StaticFiles(directory="public/js"), name="js")
    app.mount("/css", StaticFiles(directory="public/css"), name="css")
    app.mount("/html", StaticFiles(directory="public/html"), name="html")