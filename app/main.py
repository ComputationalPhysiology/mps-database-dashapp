from dash import Dash, html
import dash
import dash_mantine_components as dmc
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
server = app.server
cache.init_app(app.server)

api = Api(
    username=settings.MPS_DATABASE_USERNAME,
    password=settings.MPS_DATABASE_PASSWORD,
    baseurl=settings.MPS_DATABASE_BASEURL,
    timeout=15,
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = dmc.Container(
    [
        dmc.Navbar(
            p="md",
            width={"base": 300},
            height=500,
            fixed=True,
            children=[
                dmc.Header(
                    height=60,
                    children=[dmc.Title("MPS database", order=3, style={"textAlign": "center", "height": "200px"})],
                ),
                dmc.Anchor("Home", href="/", underline=False),
                dmc.Anchor("Experiments", href="/experiments", underline=False),
                dmc.Anchor("MPS data", href="/mpsdata", underline=False),
            ],
        ),
    ],
    style=SIDEBAR_STYLE,
)

sidebar = dmc.Navbar(
    p="md",
    children=[
        dmc.Anchor("Home", href="/", underline=False),
        dmc.Anchor("Experiments", href="/experiments", underline=False),
        dmc.Anchor("MPS data", href="/mpsdata", underline=False),
    ],
)


app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Grid(
            children=[
                dmc.Col(html.Div("MPS database", style={"fontSize": 50, "textAlign": "center"}), span=12),
                dmc.Col([sidebar], span="content"),
                dmc.Col([dash.page_container], span="auto"),
            ],
        )
    ],
)
