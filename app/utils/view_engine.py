from fastapi.templating import Jinja2Templates

_template = None

def Init_Template(directory:str="app/routers"):
    global _template
    _template = Jinja2Templates(directory)


def Template():
    return _template

def RenderTemplate(request, name, context={}):
    return _template.TemplateResponse(request=request, name=name, context=context)