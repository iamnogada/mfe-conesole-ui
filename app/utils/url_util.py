
from typing import List, Dict
from urllib.parse import urlparse,parse_qs
from pydantic import BaseModel

class CurrentRequest(BaseModel):
    protocol: str
    server_address: str
    port : str
    app_name: str
    app_path: str
    full_path: str
    query: Dict[str, List[str]]

def extract_url_parts(url: str) -> CurrentRequest:
    if not url.startswith(('http://', 'https://', '/')):
        url = '/dummy_base/' + url

    parsed_url = urlparse(url)
    protocol = parsed_url.scheme or 'http'
    server_address = parsed_url.hostname or 'localhost'
    port = str(parsed_url.port) or '80'  # Convert to string, default to '80'
    path_segments = parsed_url.path.split('/')

    app_name = '/' + path_segments[1] if len(path_segments) > 1 else ''
    app_path = '/' + '/'.join(path_segments[2:]).rstrip('/')  # Ensure app_path starts with '/'
    full_path = parsed_url.path.rstrip('/')  # The full path without the query
    query_params = parse_qs(parsed_url.query)  # The query parameters

    # Removing dummy_base if added for parsing
    if app_name == '/dummy_base':
        app_name = '/' + path_segments[2] if len(path_segments) > 2 else ''
        app_path = '/' + '/'.join(path_segments[3:])  # Adjust app_path
        full_path = '/' + '/'.join(path_segments[2:])  # Adjust full_path without dummy_base

    # Create and return an instance of CurrentRequest
    return CurrentRequest(
        protocol=protocol,
        server_address=server_address,
        port=port,
        app_name=app_name,
        app_path=app_path,
        full_path=full_path,
        query=query_params
    )