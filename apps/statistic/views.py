from django.views.generic import TemplateView

from ..utils import reader, stats, mvo, annualize, risk
from .chart import get_chart
import numpy as np


class StatsHomeView(TemplateView):
    template_name = 'statistic/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tickers = []
        with open('./apps/data/tickers.csv', 'r') as f:
            for line in f.readlines():
                l = line.strip().split(',')
                tickers.append(l)
        tickers = tickers[0]
        # print(tickers)

        portfolio_price = reader.get_quotes(tickers)[0]
        context['charts'] = get_chart(portfolio_price)
        portfolio_pct = reader.get_quotes(tickers)[1]
        # print(portfolio_pct)
        portfolio_pct_stats = stats.get_portfolio_stat_summary(portfolio_pct)
        # print(portfolio_pct_stats)
        context['portfolio_stats'] = portfolio_pct_stats

        weights = []
        with open('./apps/data/weights.csv', 'r') as f:
          for line in f.readlines():
            l = line.strip().split(',')
            weights.append([float(el) for el in l])

        weights = np.array(weights[0])
        portfolio_pct_ann = annualize.get_annualized_returns(portfolio_pct, 255)
        covariance_matrix = portfolio_pct.cov() * 255
        context['total_port_returns'] = mvo.get_portfolio_returns(weights, portfolio_pct_ann[tickers])
        context['total_port_vol'] = mvo.get_portfolio_volatility(weights, covariance_matrix.loc[tickers, tickers])

        weighted_returns = weights * portfolio_pct
        total_port_returns = weighted_returns.sum(axis=1)

        context['skewness'] = total_port_returns.aggregate(stats.get_skewness)
        context['kurtosis'] = total_port_returns.aggregate(stats.get_kurtosis)
        context['cornish_fisher_var'] = total_port_returns.aggregate(risk.get_cf_var)
        context['historic_cvar'] = total_port_returns.aggregate(risk.get_conditional_historic_var)
        # context['annualized_sharpe_ratio'] = total_port_returns.aggregate(risk.get_sharpe_ratio, risk_free_rate=0.03, periods_per_year=255)
        context['annualized_sharpe_ratio'] = total_port_returns.aggregate(risk.get_sharpe_ratio)
        context['drawdown'] = total_port_returns.aggregate(lambda returns_series: risk.get_drawdown(returns_series).Drawdown.min())

        return context

