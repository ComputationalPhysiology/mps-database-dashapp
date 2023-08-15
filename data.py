import pandas as pd
from api import Api


def get_all_experiments(_api: Api):
    data = _api.list_experiments()

    df = pd.DataFrame.from_records(data, columns=("id", "name", "created", "info"))
    df["name"] = df["name"].astype(str)
    df["info"] = df["info"].astype(str)
    df["created"] = df["created"].astype(str)
    df.set_index("id", inplace=True, drop=False)
    # df["created"] = pd.to_datetime(df["created"])

    return df


def get_mps_data_by_experiment(_api: Api, experiment_name: str):
    data = _api.search({"experiment_name": experiment_name})

    df = pd.DataFrame.from_records(
        data,
        columns=(
            "id",
            "drug_name",
            "dose",
            "run",
            "chip",
            "cell_line_name",
            "trace_type",
            "path",
            "media",
            "pacing_frequency",
        ),
    )
    df.set_index("id", inplace=True, drop=False)
    return df
