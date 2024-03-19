
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.services import load_apps_services, App_Services
from app.services.main_service import get_app_services
from app.utils import InitFilesystemRouter, log, RenderTemplate, Init_Template
from app.middlewares import HTTP_Middleware
import httpx

from app.services import init_static_files

#  Context path for the application
APP_NAME=""

app = FastAPI(root_path=f"{APP_NAME}",
              title="zmp-console-shell",
              default_response_class=HTMLResponse,
              version="0.1.0",
              debug=True)

log.info(f"App {APP_NAME} started")

# Mount static files
init_static_files(app)

# Initialize HTML Template(Jinja2   )
Init_Template(directory="app/routers")

# If Reqeust form HTMX, then response only block html, othwerwise return full html including header
# For HTMX, set request.state.hx_request = True so Jinja2 conditionally add css and js files
mfe_middleware = HTTP_Middleware(app=app, root_path=f"{APP_NAME}")
app.add_middleware(BaseHTTPMiddleware, dispatch=mfe_middleware.dispatch)

upstream = {
    "common": "http://127.0.0.1:9010",
    "remote": "http://127.0.0.1:9090",
}


# Load routers from filesystem : menu, header, footer etc
InitFilesystemRouter(app)

# Load Apss & Services from JSON file
APPS_SERVICES_FILE="data/services.json"
app.App_Services =load_apps_services(APPS_SERVICES_FILE)


# Wildcard Router for reverse proxy to remote services
@app.get("/{path:path}")
@app.post("/{path:path}")
@app.put("/{path:path}")
@app.delete("/{path:path}")
@app.patch("/{path:path}")
async def root_get(path:str, request: Request=None, response: Response=None):
    log.info(f"Request: {path}")
    remote_app_path = path.split('/')[0]
    # Find remote app if not return None
    remote_app = app.App_Services.find_app(remote_app_path)
    if remote_app:
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
    upstream_url = f"{remote_app.remoteApp}/{path}?{query_params}" if query_params else f"{remote_app.remoteApp}/{path}"
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





