import pandas as pd
from flask_caching import Cache
import logging

from app.api import Api

logger = logging.getLogger(__name__)


def get_all_experiments(_api: Api, cache: Cache | None = None):
    logger.debug("Get all experiments")
    df = None
    if cache is not None:
        # Try to get the data from the cache
        df = cache.get("experiments")

    if df is None:
        logger.debug("Fetching experiments from API")
        data = _api.list_experiments()

        df = pd.DataFrame.from_records(data, columns=("id", "name", "created", "info"))
        df["name"] = df["name"].astype(str)
        df["info"] = df["info"].astype(str)
        df["created"] = df["created"].astype(str)
        df.set_index("id", inplace=True, drop=False)
    else:
        logger.debug("Experiments loaded from cache")

    if cache is not None:
        cache.set("experiments", df)

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
