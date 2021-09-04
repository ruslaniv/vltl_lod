from django.views.generic import TemplateView
from .blackl import *

from ..utils import reader, stats, mvo, annualize, risk
import numpy as np, numpy.random
import pandas as pd

np.set_printoptions(suppress=True, formatter={'float_kind': '{:0.4f}'.format})

tickers = ['ADBE','AMZN','BAC','COST','CSCO','INTC','JPM','MSFT','PG','XOM']
# tickers = []
# with open('tickers.csv', 'r') as f:
#     for line in f.readlines():
#         l = line.strip().split(',')
#         tickers.append(l)
# tickers = tickers[0]


class BlackHomeView(TemplateView):
    template_name = 'blacklitterman/blacklitterman.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views_uncertain'] = get_chart1()
        context['risk_rets'] = get_chart2()
        context['cov_mat'] = get_chart3()
        context['views'] = get_chart4()
        context['rets'] = get_chart5()
        context['weights'] = get_weights()
        return context
