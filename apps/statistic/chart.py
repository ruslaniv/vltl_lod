import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(data, *args, **kwargs):
    plt.switch_backend('AGG')
    column_names = list(data.columns)
    charts = []
    for ticker in column_names:
        fig = plt.figure()
        axes = plt.figure(figsize=(5, 3))
        data[ticker].plot()
        plt.title(ticker)
        plt.tight_layout()
        chart = get_graph()
        charts.append(chart)
        plt.close()
    return charts
