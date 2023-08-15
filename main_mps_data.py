from dash import Dash, dash_table, Input, Output, callback, State
import data
import dash
from pathlib import Path
import os
from flask_caching import Cache

# import dash_bootstrap_components as dmc
import dash_mantine_components as dmc
from api import Api

api = Api(
    os.getenv("MPS_DATABASE_USERNAME"),
    os.getenv("MPS_DATABASE_PASSWORD"),
    baseurl="http://172.16.16.92:8004",
)
df = data.get_all_experiments(api)

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": os.getenv(
            "MPS_DATABASE_CACHE_DIR", Path.home() / ".cache" / "mps_database"
        ),
        "CACHE_DEFAULT_TIMEOUT": os.getenv("MPS_DATABASE_CACHE_DEFAULT_TIMEOUT", 3600),
    }
)
app = Dash(__name__)
cache.init_app(app.server)


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
        dmc.Header(
            height=60,
            children=[
                dmc.Title(
                    "MPS data table", style={"textAlign": "center", "height": "200px"}
                )
            ],
            style={"marginTop": 20},
        ),
        dmc.Container(
            children=[
                dmc.Grid(
                    children=[
                        dmc.Col(
                            select_exp := dmc.Select(
                                label="Select experiment",
                                style={"width": "100%"},
                                searchable=True,
                                data=df.name,
                            ),
                            span=5,
                        ),
                        dmc.Col(
                            use_cache_db := dmc.Select(
                                label="Caching",
                                value="Use cache",
                                data=["No caching", "Use cache", "Reset cache"],
                            ),
                            span=2,
                        ),
                        dmc.Col(
                            search_exp_btn := dmc.Button(
                                "Search", style={"marginTop": 25}, n_clicks=0
                            ),
                            span=2,
                        ),
                        dmc.Col(
                            row_drop := dmc.Select(
                                label="Select number of rows",
                                value="10",
                                clearable=False,
                                style={"width": "100%"},
                                disabled=True,
                                data=["10", "25", "50", "100", "all"],
                            ),
                            span=3,
                        ),
                    ],
                    style={"marginTop": 10, "marginBottom": 10, "padding": 5},
                )
            ],
            style={"width": "100%"},
        ),
        dmc.Container(
            children=[
                dmc.Group(
                    children=[
                        select_all_btn := dmc.Button(
                            "Select all",
                            id="select-all-button",
                            variant="gradient",
                            gradient={"from": "teal", "to": "lime", "deg": 105},
                        ),
                        deselect_all_btn := dmc.Button(
                            "Deselect all",
                            id="deselect-all-button",
                            variant="gradient",
                            gradient={"from": "orange", "to": "red"},
                        ),
                    ]
                )
            ],
            style={
                "marginTop": 10,
                "marginBottom": 10,
            },
        ),
        dmc.Container(
            id="datatable-container",
            children=[
                dmc.LoadingOverlay(
                    mytable := dash_table.DataTable(
                        id="data-table",
                        columns=[
                            {"name": "Drug", "id": "drug_name", "type": "text"},
                            {"name": "Dose", "id": "dose", "type": "text"},
                            {"name": "Run", "id": "run", "type": "text"},
                            {"name": "Trace type", "id": "trace_type", "type": "text"},
                        ],
                        selected_rows=[],
                        filter_action="native",
                        page_size=10,
                        row_selectable="multi",
                        style_data={
                            "width": "150px",
                            "minWidth": "150px",
                            "maxWidth": "150px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                        style_cell={
                            "fontSize": 16,
                            "font-family": "'Inter', sans-serif",
                        },
                    ),
                ),
                dmc.Text(id="some-output"),
            ],
        ),
    ],
)


@callback(
    Output(mytable, "data"),
    Output(row_drop, "disabled"),
    Input(search_exp_btn, "n_clicks"),
    State(select_exp, "value"),
    State(use_cache_db, "value"),
)
def search_experiment(n_clicks, experiment_name, use_cache_value):
    if experiment_name is None:
        return [], True

    cache_key = f"search-{experiment_name}"
    df = None
    if use_cache_value in "Use cache":
        df = cache.get(cache_key)

    if df is None:
        df = data.get_mps_data_by_experiment(api, experiment_name=experiment_name)

    if use_cache_value in ["Use cache", "Reset cache"]:
        cache.set(cache_key, df)

    return df.to_dict("records"), False


@callback(
    Output(mytable, "page_size"),
    Input(row_drop, "value"),
    State(mytable, "data"),
)
def update_page_size(value, data):
    if value == "all":
        return len(data)

    return int(value)


# @callback(
#     Output("some-output", "value"),
#     Input(mytable, "selected_row_ids"),
#     Input(mytable, "active_cell"),
# )
# def on_row_click(selected_row_ids, active_cell):
#     print(f"Click: {active_cell=}, {selected_row_ids=}")
#     return "Row clicked"


@app.callback(
    inputs=[
        Input("select-all-button", "n_clicks"),
        Input("deselect-all-button", "n_clicks"),
    ],
    output=[Output(mytable, "selected_rows")],
    state=[
        State(mytable, "data"),
        State(mytable, "derived_virtual_data"),
        State(mytable, "derived_virtual_selected_rows"),
    ],
)
def selection(
    select_n_clicks, deselect_n_clicks, original_rows, filtered_rows, selected_rows
):
    ctx = dash.callback_context.triggered[0]
    ctx_caller = ctx["prop_id"]
    if filtered_rows is not None:
        if ctx_caller == "select-all-button.n_clicks":
            selected_ids = [row["id"] for row in filtered_rows]
            return [
                [i for i, row in enumerate(original_rows) if row["id"] in selected_ids]
            ]
        if ctx_caller == "deselect-all-button.n_clicks":
            return [[]]
        raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
