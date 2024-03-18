""" smaple router for testing"""
from datetime import datetime


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse,JSONResponse


from app.utils import Template, log


router = APIRouter()
log.info(__name__)



@router.get("/", response_class=HTMLResponse)
async def endpoint(request: Request) -> HTMLResponse:
    """endpoint"""
    return Template().TemplateResponse(
        "sample/sample.html",
        context={'request': request, "datetime": "value"}
    )