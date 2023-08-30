from typing import Any

import dash_mantine_components as dmc
from dash import dash_table, Input, Output, callback, State, dcc
import dash
import logging


from app import plots
from app import data
from app import enums
from app import models

logger = logging.getLogger(__name__)

dash.register_page(__name__)

layout = dmc.MantineProvider(
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
            children=[dmc.Title("MPS data table", order=2, style={"textAlign": "center", "height": "200px"})],
            style={"marginTop": 20},
        ),
        dmc.Container(
            children=[
                dmc.Grid(
                    children=[
                        dmc.Col(
                            load_exp_btn := dmc.Button("Load experiments"),
                            span=3,
                        ),
                        dmc.Col(dmc.Alert("test", title="Success!", color="green"), span=9),
                    ],
                    style={
                        "align": "center",
                        "justify": "center",
                    },
                ),
                dmc.Grid(
                    children=[
                        dmc.Col(
                            select_exp := dmc.Select(
                                label="Select experiment",
                                style={"width": "100%"},
                                searchable=True,
                            ),
                            span=5,
                        ),
                        dmc.Col(
                            use_cache_mps_data_search_db := dmc.Select(
                                label="Caching",
                                value="Use cache",
                                data=["No caching", "Use cache", "Reset cache"],
                            ),
                            span=2,
                        ),
                        dmc.Col(
                            search_exp_btn := dmc.Button("Search", style={"marginTop": 25}, n_clicks=0),
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
                ),
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
                        selected_row_ids=[],
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
            ],
        ),
        dmc.Container(
            children=[
                dmc.Grid(
                    children=[
                        dmc.Col(search_mps_data_btn := dmc.Button("Load data"), span=2),
                        dmc.Col(
                            use_cache_mps_data_load_db := dmc.Select(
                                value="Use cache",
                                data=["No caching", "Use cache", "Reset cache"],
                            ),
                            span=2,
                        ),
                    ]
                ),
            ],
            style={
                "marginTop": 10,
                "marginBottom": 10,
            },
        ),
        dcc.Store(id="mps-data-store"),
        dmc.LoadingOverlay(
            dmc.Container(
                children=[
                    dmc.Container(
                        children=[
                            dmc.Grid(
                                children=[
                                    dmc.Col(
                                        trace_select_db := dmc.Select(
                                            label="Select Trace",
                                            value="fluorescence",
                                            data=[
                                                {
                                                    "value": enums.TraceTypes.fluorescence,
                                                    "label": "Fluorescence",
                                                },
                                                {
                                                    "value": enums.TraceTypes.displacement_norm,
                                                    "label": "Displacement norm",
                                                },
                                            ],
                                        ),
                                        span=4,
                                    ),
                                    dmc.Col(
                                        plot_select_db := dmc.Select(
                                            label="Select plot",
                                            value="original",
                                            data=[
                                                {
                                                    "value": enums.PlotTypes.original,
                                                    "label": "Original Trace",
                                                },
                                                {
                                                    "value": enums.PlotTypes.original_w_pacing,
                                                    "label": "Original trace with pacing",
                                                },
                                                {
                                                    "value": enums.PlotTypes.average,
                                                    "label": "Average",
                                                },
                                                {
                                                    "value": enums.PlotTypes.average_normalized,
                                                    "label": "Average (normalized)",
                                                },
                                                {
                                                    "value": enums.PlotTypes.chopped,
                                                    "label": "Chopped",
                                                },
                                                {
                                                    "value": enums.PlotTypes.chopped_aligned,
                                                    "label": "Chopped",
                                                },
                                                {
                                                    "value": enums.PlotTypes.corrected_and_background,
                                                    "label": "Chopped",
                                                },
                                            ],
                                        ),
                                        span=4,
                                    ),
                                    dmc.Col(
                                        labelby_select_db := dmc.Select(label="Label by", value="id"),
                                        span=4,
                                    ),
                                ]
                            )
                        ]
                    ),
                    dmc.Container(children=[dcc.Graph(id="graph")]),
                ],
            ),
        ),
    ],
)


def get_detailed_info(row_ids: list[int], use_cache_value: str) -> list[dict[str, Any]]:
    info = {}
    from app.main import cache, api

    logger.debug(f"Get detailed info: {use_cache_value=}")
    if use_cache_value == "Use cache":
        logger.debug("Search for data in cache")
        # Fetch existing data from cache
        for row_id in row_ids:
            d_ = cache.get(f"detailed-info-{row_id}")

            if d_ is not None:
                logger.debug(f"Found cached data for {row_id}")
                info[row_id] = d_
            else:
                logger.debug(f"Could not find cached data for {row_id}")

    ids_to_fetch = [row_id for row_id in row_ids if row_id not in info]
    if len(ids_to_fetch) > 0:
        new_info = api.mps_data_detailed_info(ids_to_fetch)
    else:
        new_info = []

    # Make sure we get data in the same order as row_ids
    d = []
    for row_id in row_ids:
        if row_id in info:
            d.append(info[row_id])
        else:
            this_info = new_info[ids_to_fetch.index(row_id)]
            d.append(this_info)
            if use_cache_value in ["Use cache", "Reset cache"]:
                cache.set(f"detailed-info-{row_id}", this_info)
    return d


@callback(
    Output("mps-data-store", "data"),
    Output(labelby_select_db, "data"),
    Input(search_mps_data_btn, "n_clicks"),
    State(mytable, "derived_virtual_selected_rows"),
    State(mytable, "derived_virtual_data"),
    State(use_cache_mps_data_load_db, "value"),
)
def search_mps_data(n_clicks, selected_rows, filtered_rows, use_cache_value):
    if n_clicks == 0:
        # Not clicked
        raise dash.exceptions.PreventUpdate
    if selected_rows is None or len(selected_rows) == 0:
        raise dash.exceptions.PreventUpdate

    rows = [filtered_rows[i]["id"] for i in selected_rows]
    info = get_detailed_info(rows, use_cache_value=use_cache_value)
    plot_labels = []
    if len(info) > 0:
        values = info[0].get("plot_label_values", {})
        plot_labels = [label for label, value in values.items() if isinstance(value, (int, str))]

    return info, plot_labels


@callback(
    Output("graph", "figure"),
    Input("mps-data-store", "data"),
    Input(plot_select_db, "value"),
    Input(trace_select_db, "value"),
    Input(labelby_select_db, "value"),
)
def draw_traces(infos, plot_type, selected_trace, label_by):
    if plot_type is None:
        return {}
    if infos is None or len(infos) == 0:
        return {}

    fig = plots.plot(
        [models.MPSData(**info) for info in infos],
        selected_trace=selected_trace,
        plot_type=plot_type,
        label_by=label_by,
    )
    return fig


@callback(
    Output(select_exp, "data"),
    Input(load_exp_btn, "n_clicks"),
)
def load_experiments(n_clicks):
    if not n_clicks:
        # Not clicked
        raise dash.exceptions.PreventUpdate

    from app.main import api, cache

    df = data.get_all_experiments(api, cache)
    return df.name


@callback(
    Output(mytable, "data"),
    Output(row_drop, "disabled"),
    Input(search_exp_btn, "n_clicks"),
    State(select_exp, "value"),
    State(use_cache_mps_data_search_db, "value"),
)
def search_experiment(n_clicks, experiment_name, use_cache_value):
    if experiment_name is None:
        return [], True

    from app.main import cache, api

    cache_key = f"search-{experiment_name}"
    logger.debug(f"Loading mps data from experiment {experiment_name}")
    df = None
    if use_cache_value in "Use cache":
        df = cache.get(cache_key)

    # We don't want to make unnecessary saves to the cache.
    # If df is None it means that we need to fetch from the database
    # and it should be stored in the cache if `use_cache value` is either
    # of "Use cache" or "Reset cache". Otherwise we should not save it
    # to the cache
    update_cache = False
    if df is None:
        logger.debug("Fetching mps data from API")
        update_cache = use_cache_value in ["Use cache", "Reset cache"]
        df = data.get_mps_data_by_experiment(api, experiment_name=experiment_name)
    else:
        logger.debug("Data loaded from cache")

    if update_cache:
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


@callback(
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
def selection(select_n_clicks, deselect_n_clicks, original_rows, filtered_rows, selected_rows):
    ctx = dash.callback_context.triggered[0]
    ctx_caller = ctx["prop_id"]
    if filtered_rows is not None:
        if ctx_caller == "select-all-button.n_clicks":
            selected_ids = [row["id"] for row in filtered_rows]
            print(selected_ids)
            return [[i for i, row in enumerate(original_rows) if row["id"] in selected_ids]]
        if ctx_caller == "deselect-all-button.n_clicks":
            return [[]]
        raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate
