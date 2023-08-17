import plotly.graph_objects as go
from typing import NamedTuple

from app import models
from app import enums


class PlotData(NamedTuple):
    x: list[list[float]]
    y: list[list[float]]
    extra_label: list[str]
    title: str = ""
    ylabel: str = "Time [ms]"
    xlabel: str = ""


tracetype2ylabel = {
    enums.TraceTypes.fluorescence: "\u0394 F / F0",
    enums.TraceTypes.displacement_norm: "\u00b5m",
}

tracetype2title = {
    enums.TraceTypes.fluorescence: "Fluorescence",
    enums.TraceTypes.displacement_norm: "Displacement",
}


def normalize(x: list[float]) -> list[float]:
    if len(x) == 0:
        return x
    xmin = min(x)
    xmax = max(x)

    return [(xi - xmin) / (xmax - xmin) for xi in x]


def get_plot_data(info: models.MPSData, plot_type: enums.PlotTypes, selected_trace: enums.TraceTypes) -> PlotData:
    trace_type = enums.TraceTypes.from_string(selected_trace)
    plot_type = enums.PlotTypes.from_string(plot_type=plot_type)

    ylabel = tracetype2ylabel[trace_type]
    title = tracetype2title[trace_type]
    extra_label = [""]

    if trace_type == enums.TraceTypes.fluorescence:
        if plot_type == enums.PlotTypes.original:
            x = [info.unchopped_data.original_times]
            y = [info.unchopped_data.original_trace]

        elif plot_type == enums.PlotTypes.original_w_pacing:
            x = [info.unchopped_data.original_times, info.unchopped_data.original_times]
            y = [info.unchopped_data.original_trace, info.unchopped_data.pacing]
            extra_label = ["original", "pacing"]

        elif plot_type == enums.PlotTypes.average:
            x = [info.chopped_data.time_1std]
            y = [info.chopped_data.trace_1std]

        elif plot_type == enums.PlotTypes.average_normalized:
            x = [info.chopped_data.time_1std]
            y = [normalize(info.chopped_data.trace_1std)]
            ylabel = "Normalized"

    else:
        if plot_type == enums.PlotTypes.original:
            x = [info.motion_tracking.time]
            y = [info.motion_tracking.get_motion_array(trace_type.name).original]
        elif plot_type == enums.PlotTypes.original_w_pacing:
            x = [info.motion_tracking.time, info.motion_tracking.time]
            y = [
                info.motion_tracking.get_motion_array(trace_type.name),
                info.motion_tracking.pacing,
            ]
            extra_label = ["original", "pacing"]
        elif plot_type == enums.PlotTypes.average:
            arr = info.motion_tracking.get_motion_array(trace_type.name)
            x = [arr.average_time]
            y = [arr.average_trace]

        elif plot_type == enums.PlotTypes.average_normalized:
            arr = info.motion_tracking.get_motion_array(trace_type.name)
            x = [arr.average_time]
            y = [normalize(arr.average_trace)]
            ylabel = "Normalized"

    return PlotData(x=x, y=y, ylabel=ylabel, title=title, extra_label=extra_label)


def plot(
    infos: list[models.MPSData],
    selected_trace: enums.TraceTypes,
    plot_type: enums.PlotTypes,
    label_by: str,
):
    fig = go.Figure()
    data = None
    for info in infos:
        labels = info.plot_label_values
        data = get_plot_data(info, selected_trace=selected_trace, plot_type=plot_type)
        for x, y, label in zip(data.x, data.y, data.extra_label):
            fig.add_trace(go.Scatter(x=x, y=y, name=" ".join([str(labels.get(label_by)), label])))

    if data is not None:
        fig.update_layout(
            title=data.title,
            xaxis_title=data.xlabel,
            yaxis_title=data.ylabel,
            legend_title=label_by,
        )

    return fig
