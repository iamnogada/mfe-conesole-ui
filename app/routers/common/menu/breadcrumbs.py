""" common menu GNB """

from functools import reduce

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from app.utils import Template, log


router = APIRouter()
log.info(__name__)


@router.get("/breadcrumbs", response_class=HTMLResponse)
async def breadcrumbs(request: Request) -> HTMLResponse:
    """breadcrumbs"""
    
    breadcrumbs = f"{request.state.current.full_path}".split("/")[1:]

    crumbs = reduce(
        lambda accumulate_path, crumb: accumulate_path
        + [
            {
                "name": crumb,
                "href": (
                    f"{accumulate_path[-1]['href']}/{crumb}"
                    if accumulate_path
                    else f"/{crumb}"
                ),
            }
        ],
        breadcrumbs,
        [],
    )

    return Template().TemplateResponse(
        request=request,
        name="common/menu/breadcrumbs.html",
        context={"breadcrumbs": crumbs},
    )
