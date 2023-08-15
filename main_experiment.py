from dash import Dash, dash_table, Input, Output, callback
import data
import os
import dash_mantine_components as dmc
from api import Api

api = Api(
    os.getenv("MPS_DATABASE_USERNAME"),
    os.getenv("MPS_DATABASE_PASSWORD"),
    baseurl="http://172.16.16.92:8004",
)
df = data.get_all_experiments(api)

app = Dash(__name__)


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
    withNormalizeCSS=True,
    children=[
        dmc.Header(
            height=60,
            children=[
                dmc.Title(
                    "Experiments table",
                    style={"textAlign": "center", "height": "200px"},
                )
            ],
            style={"marginTop": 20},
        ),
        dmc.Container(
            [
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
                    data=df.to_dict("records"),
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
    Output(my_table, "data"), Output(my_table, "page_size"), Input(row_drop, "value")
)
def update_dropdown_options(row_v):
    dff = df.copy()

    if row_v == "all":
        row_v = dff.size

    row_v = int(row_v)

    return dff.to_dict("records"), row_v


@callback(Output(info_text_area, "value"), Input(my_table, "selected_row_ids"))
def update_selected_rows(selected_row_ids):
    if selected_row_ids is None:
        return "No experiment selected"

    info = df.loc[selected_row_ids[0]]["info"]
    return info


if __name__ == "__main__":
    app.run_server(debug=True, port=8001)
