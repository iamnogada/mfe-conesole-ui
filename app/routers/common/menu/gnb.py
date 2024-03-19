""" common menu GNB """
from datetime import datetime


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse,JSONResponse


from app.utils import Template, log

router = APIRouter()
log.info(__name__)

@router.get("/gnb", response_class=HTMLResponse)
async def gnb(request: Request) -> HTMLResponse:
    """gnb"""
    
    nav_items = [
       
        {"displayName": app.displayName, "active": 'true' if app.href == request.state.current_app else 'false', "href": app.href}
        for app in request.app.App_Services.apps
    ]
    
    return Template().TemplateResponse(
        request=request,
        name="common/menu/gnb.html",
        context={"nav_items": nav_items}
    )