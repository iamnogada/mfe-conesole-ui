"""
Main Endpoints for MFE
Serve '/'
- select content area load to htmx and vue/react 
"""
from datetime import datetime


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse,JSONResponse
from app.utils import RenderTemplate, log



router = APIRouter()

# Default Home Router
# select loader: htmx/vue/etc
@router.get("/")
async def index(request: Request=None):
    log.info(f"servicelinks: {request.app.App_Services.serviceLinks}")
    return RenderTemplate(request=request,name="main.html",context={"title":"ZMP Console Shell"})
