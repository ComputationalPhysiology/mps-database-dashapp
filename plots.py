import plotly.graph_objects as go


def plot_original_trace(info):
    fig = go.Figure()
    for d in info:
        labels = d.get("plot_label_values", {})
        unchopped_data = d.get("unchopped_data", {})
        y = unchopped_data.get("trace", [])
        x = unchopped_data.get("times", [])

        fig.add_trace(go.Scatter(x=x, y=y, name=labels.get("dose")))
    return fig
