import dash
import dash_mantine_components as dmc


dash.register_page(__name__, path="/")

layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        # "components": {
        # "Button": {"styles": {"root": {"fontWeight": 400}}},
        # "Alert": {"styles": {"title": {"fontWeight": 500}}},
        # "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        # },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Header(
            height=60,
            children=[dmc.Title("Home", order=2, style={"textAlign": "center", "height": "200px"})],
            style={"marginTop": 20},
        ),
    ],
)
