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


def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        print('bar chart')
        sns.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#2':
        print('pie chart')
        plt.pie(data=d, x='total_price', labels=d[key].values)
    elif chart_type == '#3':
        print('line chart')
        plt.plot(d[key], d['total_price'], color='green', marker='o', linestyle='dashed')
    else:
        print('ups... failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart