from django.views.generic import TemplateView

from ..utils import reader, stats, mvo, annualize, risk
from .chart import get_chart
import numpy as np, numpy.random
import pandas as pd
np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.4f}'.format})


class MarkowitzHomeView(TemplateView):
    template_name = 'markowitz/markowitz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tickers = []
        with open('./apps/data/tickers.csv', 'r') as f:
            for line in f.readlines():
                l = line.strip().split(',')
                tickers.append(l)
        tickers = tickers[0]

        weights = []
        with open('./apps/data/weights.csv', 'r') as f:
            for line in f.readlines():
                l = line.strip().split(',')
                weights.append([float(el) for el in l])
        weights = np.array(weights[0])

        portfolio_pct = reader.get_quotes(tickers)[1]
        # weights = np.array([0.0529, 0.0591, 0.0728, 0.1286, 0.0770, 0.1981, 0.0050, 0.0376, 0.1953, 0.1420, 0.0317])
        portfolio_pct_ann = annualize.get_annualized_returns(portfolio_pct, 255)
        covariance_matrix = portfolio_pct.cov() * 255
        total_port_returns = mvo.get_portfolio_returns(weights, portfolio_pct_ann[tickers])
        total_port_vol = mvo.get_portfolio_volatility(weights, covariance_matrix.loc[tickers, tickers])

        weighted_returns = weights * portfolio_pct
        total_port_returns = weighted_returns.sum(axis=1)
        
        gmv = mvo.get_gmv_portfolio(covariance_matrix)
        gmv_weights=[]
        for t,w in zip(tickers, gmv):
            if round(w, 4) > 0:
                gmv_weights.append((t,w))
        context['gmv_weights'] = gmv_weights
        all_mark = get_chart(portfolio_pct_ann, covariance_matrix, port_ret=total_port_returns, port_vol=total_port_vol)
        context['chart'] = all_mark[0]
        sharp_weights = []
        for elem in all_mark[1][0][0]:
            sharp_weights.append((tickers[elem[0]], elem[1]))
        context['max_sharpe'] = sharp_weights
        return context
