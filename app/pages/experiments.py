from dash import dash_table, Input, Output, callback
import dash
import dash_mantine_components as dmc

from app import data


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
    withNormalizeCSS=True,
    children=[
        dmc.Header(
            height=60,
            children=[
                dmc.Title(
                    "Experiments table",
                    order=2,
                    style={"textAlign": "center", "height": "200px"},
                )
            ],
            style={"marginTop": 20},
        ),
        dmc.Container(
            [
                load_exp_btn := dmc.Button("Load experiments"),
                row_drop := dmc.Select(
                    label="Select number of rows",
                    value="10",
                    clearable=False,
                    style={"width": "35%"},
                    data=["10", "25", "50", "100", "all"],
                ),
                my_table := dash_table.DataTable(
                    id="experiment-table",
                    columns=[
                        {"name": "Name", "id": "name", "type": "text"},
                        {"name": "Info", "id": "info", "type": "text"},
                        {"name": "Created", "id": "created", "type": "text"},
                    ],
                    selected_rows=[],
                    filter_action="native",
                    page_size=10,
                    row_selectable="single",
                    style_data={
                        "width": "150px",
                        "minWidth": "150px",
                        "maxWidth": "150px",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    },
                    style_cell={"fontSize": 16, "font-family": "'Inter', sans-serif"},
                ),
                info_text_area := dmc.Textarea(autosize=True),
            ]
        ),
    ],
)


@callback(
    Output(my_table, "data"),
    Input(load_exp_btn, "n_clicks"),
)
def load_experiments(n_clicks):
    if not n_clicks:
        # Not clicked
        raise dash.exceptions.PreventUpdate
    from app.main import api, cache

    df = data.get_all_experiments(api, cache)
    return df.to_dict("records")


@callback(Output(my_table, "page_size"), Input(row_drop, "value"))
def update_dropdown_options(row_v):
    if row_v == "all":
        from app.main import api, cache

        df = data.get_all_experiments(api, cache)
        row_v = df.size

    row_v = int(row_v)

    return row_v


@callback(Output(info_text_area, "value"), Input(my_table, "selected_row_ids"))
def update_selected_rows(selected_row_ids):
    if not selected_row_ids:
        raise dash.exceptions.PreventUpdate

    from app.main import api, cache

    df = data.get_all_experiments(api, cache)

    info = df.loc[selected_row_ids[0]]["info"]
    return info
