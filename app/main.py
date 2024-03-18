
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils import InitFilesystemRouter, log, RenderTemplate, Init_Template
from app.middlewares import HTTP_Middleware
import httpx

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
InitFilesystemRouter(app)
Init_Template(directory="app/routers")
# If Reqeust form HTMX, then response only block html, othwerwise return full html including header
# For HTMX, set request.state.hx_request = True so Jinja2 conditionally add css and js files
mfe_middleware = HTTP_Middleware(app=app, root_path=f"{APP_NAME}")
app.add_middleware(BaseHTTPMiddleware, dispatch=mfe_middleware.dispatch)

upstream = {
    "common": "http://127.0.0.1:9010",
    "remote": "http://127.0.0.1:9090",
}
@app.get("/")
async def index(request: Request=None):
    return RenderTemplate(request=request,name="main.html",context={"title":"ZMP Console Shell"})

@app.get("/{path:path}")
@app.post("/{path:path}")
@app.put("/{path:path}")
@app.delete("/{path:path}")
@app.patch("/{path:path}")
async def root_get(path:str, request: Request=None, response: Response=None):
    log.info(f"Request: {path}")
    remote_app = path.split('/')[0]
    # Check 'Request app' exists in upstream 
    if remote_app not in upstream:
        log.info("Cannot find app")
        raise HTTPException(status_code=404, detail="Item not found")
        # return RenderTemplate(request=request,name="404.html",context={"title":"ZMP Console Shell"})
    # Response with Full template pages for direct request
    if not request.state.hx_request:
        log.info("Direct Request, Response with Full template pages")
        return RenderTemplate(request=request,name="main.html",context={"title":"ZMP Console Shell"})
    
    # Reverse proxy to remote app
    full_url = str(request.url)
    query_params = full_url.split('?')[1] if '?' in full_url else ''
    upstream_url = f"{upstream[remote_app]}/{path}?{query_params}" if query_params else f"{upstream[remote_app]}/{path}"
    log.info(f"Upstream URL: {upstream_url}")
    
    # handle request headers
    headers = dict(request.headers)
    async with httpx.AsyncClient() as client:
        result = await client.request(
            method=request.method,
            url=upstream_url,
            headers=headers,
            data=await request.body(),
            timeout=10.0  # TODO: Adjust the timeout as necessary
        )
        response.body = result.content
        for name, value in result.headers.items():
            response.headers[name] = value
        response.status_code = result.status_code
        return response
