
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils import InitFilesystemRouter, log, Template, Init_Template
from app.middlewares import HTTP_Middleware




#  Context path for the application
APP_NAME=""

app = FastAPI(root_path=f"{APP_NAME}",
              title="zmp-console-shell",
              default_response_class=HTMLResponse,
              version="0.1.0",
              debug=True)
log.info(f"App {APP_NAME} started")

# Mount static files
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")
app.mount("/js", StaticFiles(directory="public/js"), name="js")
app.mount("/css", StaticFiles(directory="public/css"), name="css")
app.mount("/html", StaticFiles(directory="public/html"), name="html")

# Load routers from filesystem
# InitFilesystemRouter(app)
Init_Template(directory="app/routers")
# If Reqeust form HTMX, then response only block html, othwerwise return full html including header
# For HTMX, set request.state.hx_request = True so Jinja2 conditionally add css and js files
mfe_middleware = HTTP_Middleware(app=app, root_path=f"{APP_NAME}")
app.add_middleware(BaseHTTPMiddleware, dispatch=mfe_middleware.dispatch)




@app.get("{full_path:path}")
def read_root(full_path: str,
              name: str = Query(None),
              request: Request=None):
    log.info(f"Request: {request.url}")
    log.info(f"Request: {full_path}")
    log.info(f"Request: {name}")
    return Template().TemplateResponse(request=request, name="main.html", context={"name":"hdhddhh"})


