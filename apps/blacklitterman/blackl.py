import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .pypfopt import black_litterman, risk_models
from .pypfopt import BlackLittermanModel, Plotting
from ..utils import reader
import base64
from io import BytesIO
import seaborn as sns


# tickers = ["SBER","GAZP","LKOH","GMKN","VTBR","ROSN","NVTK","NLMK","TATN","CHMF","HYDR"]
tickers = ['ADBE','AMZN','BAC','COST','CSCO','INTC','JPM','MSFT','PG','XOM']

prices = reader.get_quotes(tickers)[0]
pct = reader.get_quotes(tickers)[1]

# print('Prices\n', prices)
# print('Percent Changes\n', pct)

market_prices = reader.get_ind('GSPC')[0]
# print('Index\n', market_prices.tail())

mcaps = {
    'ADBE': 79504,
    'AMZN': 68012,
    'BAC': 48601,
    'COST': 50604,
    'CSCO': 6639,
    'INTC': 62534,
    'JPM': 51630,
    'MSFT': 16941,
    'PG': 15176,
    'XOM': 15029
}
# print('Market Caps\n', mcaps)

# ## Constructing the prior


S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
delta = black_litterman.market_implied_risk_aversion(market_prices)
# print('Market Risk Aversion\n', delta)

# Plotting.plot_covariance(S) #shrinked cov matrix

market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
# print('Market Implied Returns\n', market_prior)


# market_prior.plot.barh(figsize=(10, 5)) #risk adjusted returns


# ## Views
# In the BL method, views are specified via the matrix P (picking matrix) and the vector Q. Q contains the magnitude of each view, while P maps the views to the assets they belong to.
# If you are providing **absolute views** (i.e a return estimate for each asset), you don't have to worry about P and Q, you can just pass your views as a dictionary.


# You don't have to provide views on all the assets
# viewdict = {
#     "AAL": -0.30,
#     "AAPL": 0.20,
#     "AMZN": 0.35,
#     "FB":    0.05,
#     "GE":  -0.10,
#     "GOOGL": 0.15,
#     "OXY": -0.15,  # I think Coca-Cola will go down 5%
#     "XOM": -0.15, # but low confidence, which will be reflected later
# }

viewdict = {
    'ADBE': 0.35,
    'AMZN': 0.8,
    'BAC': 0.1,
    'COST': -0.15,
    'CSCO': 0.15,
    'INTC': -0.20,
    'JPM': 0.1,
    'MSFT': 0.4,
    'PG': 0.3,
    'XOM': -0.2
}
# bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)


# Black-Litterman also allows for relative views, e.g you think asset A will outperform asset B by 10%. If you'd like to incorporate these, you will have to build P and Q yourself. An explanation for this is given in the [docs](https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html#views).
# ## View confidences
# In this section, we provide two ways that you may wish to construct the uncertainty matrix. The first is known as Idzorek's method. It allows you to specify a vector/list of percentage confidences.

# confidences = [
#     0.8,
#     0.8,
#     0.7,
#     0.5,
#     0.2, # confident in dominos
#     0.6, # confident KO will do poorly
#     0.6,
#     0.6,
# ]


confidences = [
    0.8,
    0.6,
    0.7,
    0.65,
    0.3,
    0.1,
    0.2,
    0.3,
    0.15,
    0.4,
]

bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)

# fig, ax = plt.subplots(figsize=(7,7))
# im = ax.imshow(bl.omega)
#
# # We want to show all ticks...
# ax.set_xticks(np.arange(len(bl.tickers)))
# ax.set_yticks(np.arange(len(bl.tickers)))
#
# ax.set_xticklabels(bl.tickers)
# ax.set_yticklabels(bl.tickers)
# plt.show()

# print('Views Uncertainity\n', np.diag(bl.omega)) #views uncertinity


# Note how NAT, which we gave the lowest confidence, also has the highest uncertainty.
#
# Instead of inputting confidences, we can calculate the uncertainty matrix directly by specifying 1 standard deviation confidence intervals, i.e bounds which we think will contain the true return 68% of the time. This may be easier than coming up with somewhat arbitrary percentage confidences
# intervals = [
#     (0, 0.25),
#     (0.1, 0.4),
#     (-0.1, 0.15),
#     (-0.05, 0.1),
#     (0.15, 0.25),
#     (-0.1, 0),
#     (0.1, 0.2),
#     (0.08, 0.12),
#     (0.1, 0.9),
#     (0, 0.3)
# ]
#
#
# variances = []
# for lb, ub in intervals:
#     sigma = (ub - lb)/2
#     variances.append(sigma ** 2)
#
# print(variances)
# omega = np.diag(variances)
#
#
# # ## Posterior estimates
# #
# # Given the inputs, we can compute a posterior estiamte of returns
# #
#
# # In[ ]:
#
#
# # We are using the shortcut to automatically compute market-implied prior
# bl = BlackLittermanModel(S, pi="market", market_caps=mcaps, risk_averison="delta",
#                         absolute_views=viewdict, omega=omega)



# Posterior estimate of returns
ret_bl = bl.bl_returns()
# print('Return Estimates\n', ret_bl)


# We can visualise how this compares to the prior and our views:


rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)], index=["Априори", "Апостериори", "Мнение"]).T
# print('Returns DF\n', rets_df)

# rets_df.plot.bar(figsize=(12,8)) # BL returns estimation
# plt.show()

# Notice that the posterior is always between the prior and the views. This supports the fact that the BL method is essentially a Bayesian weighted-average of the prior and views, where the weight is determined by the confidence.
# A similar but less intuitive procedure can be used to produce the posterior covariance estimate:


S_bl = bl.bl_cov()
# Plotting.plot_covariance(S_bl)


# ## Portfolio allocation
#
# Now that we have constructed our Black-Litterman posterior estimate, we can proceed to use any of the optimisers discussed in previous recipes.

from .pypfopt import EfficientFrontier, objective_functions

ef = EfficientFrontier(ret_bl, S_bl)
ef.add_objective(objective_functions.L2_reg)
ef.max_sharpe()
weights = ef.clean_weights()
# print('New weights\n', weights)

# pd.Series(weights).plot.pie(figsize=(10,10), normalize=True)
# plt.show()

# from pypfopt import DiscreteAllocation
#
# da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=20000)
# alloc, leftover = da.lp_portfolio()
# print(f"Leftover: ${leftover:.2f}")
# print('Allocations\n', alloc)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart1(): #view uncertainty
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(8,6))
    df = pd.DataFrame(data=bl.omega[0:,0:], columns=tickers)
    chart1 = sns.heatmap(df, cmap="Reds", annot=False)
    ax.set_yticklabels(bl.tickers, rotation=0)
    chart1 = get_graph()
    return chart1

def get_chart2(): #risk adjusted returns
    plt.switch_backend('AGG')
    chart2 = market_prior.plot.bar(figsize=(8, 6))
    chart2 = get_graph()
    return chart2

def get_chart3(): #shrink cov matrix
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(8,6))
    chart3 = sns.heatmap(S, cmap="Reds", annot=False)
    chart3 = get_graph()
    return chart3

def get_chart4(): #exp returns views
    plt.switch_backend('AGG')
    names = list(viewdict.keys())
    values = list(viewdict.values())
    fig, ax = plt.subplots(figsize=(8, 6))
    chart4 = plt.bar(range(len(viewdict)),values,tick_label=names)
    chart4 = get_graph()
    return chart4

def get_chart5(): #exp returns views
    plt.switch_backend('AGG')
    chart5 = rets_df.plot.bar(figsize=(12, 6))
    chart5 = get_graph()
    return chart5

def get_weights():
    # df = pd.DataFrame.from_dict(weights.items(), columns=['Ticker', 'Weight'])
    df = pd.Series(weights, name='Weights')
    df.index.name = 'Ticker'
    df.reset_index()
    print(df)
    return df
