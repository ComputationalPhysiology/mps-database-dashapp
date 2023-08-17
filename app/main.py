from dash import Dash
import dash
from flask_caching import Cache

from app.api import Api
from app.config import settings

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": settings.MPS_DATABASE_CACHE_DIR,
        "CACHE_DEFAULT_TIMEOUT": settings.MPS_DATABASE_CACHE_DEFAULT_TIMEOUT,
    }
)

app = Dash(__name__, use_pages=True)
cache.init_app(app.server)

api = Api(
    username=settings.MPS_DATABASE_USERNAME,
    password=settings.MPS_DATABASE_PASSWORD,
    baseurl=settings.MPS_DATABASE_BASEURL,
    timeout=15,
)

app.layout = dash.html.Div(
    [
        dash.html.H1("Multi-page app with Dash Pages"),
        dash.html.Div(
            [
                dash.html.Div(dash.dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"]))
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)
