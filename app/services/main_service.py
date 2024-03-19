
import json
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ValidationError

def init_static_files(app):
    app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")
    app.mount("/js", StaticFiles(directory="public/js"), name="js")
    app.mount("/css", StaticFiles(directory="public/css"), name="css")
    app.mount("/html", StaticFiles(directory="public/html"), name="html")


App_Services =None

class Sidebar(BaseModel):
    use: bool
    remoteURL: str

class App(BaseModel):
    appID: str
    displayName: str
    href: str
    remoteApp: str
    sidebar: Sidebar

class ServiceLink(BaseModel):
    appID: str
    name: Optional[str] = None  # Making 'name' optional since it's not in all entries
    title: str
    href: str
    type: str
    permission: List[str]

class AppsServices(BaseModel):
    apps: List[App]
    serviceLinks: List[ServiceLink]
    
    def find_app(self, appID: str) -> Optional[App]:
        """Finds and returns an App instance by its appID. Returns None if not found."""
        for app in self.apps:
            if app.appID == appID:
                return app
        return None  # Or you could raise an exception if preferred




def get_app_services():
    return App_Services

def load_apps_services(file_path:str) -> AppsServices:
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            App_Services = AppsServices(**json_data)
            return App_Services
    except FileNotFoundError:
        raise FileNotFoundError("The JSON file was not found.")
    except json.JSONDecodeError:
        raise ValueError("The provided file does not contain valid JSON.")
    except ValidationError as e:
        raise ValueError(f"Validation error for the JSON data: {e}")