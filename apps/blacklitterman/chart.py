import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import mvo, annualize


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(returns, covariance_matrix, **kwargs):
    plt.switch_backend('AGG')
    all_mark = mvo.plot_efficient_frontier(20, returns, covariance_matrix, 0.02, show_cml=True, show_ew_portfolio=True, show_gmv_portfolio=True)
    chart = get_graph()
    return chart, all_mark[1]
