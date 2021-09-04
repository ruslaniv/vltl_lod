import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

def get_portfolio_returns(weights, returns_series):
  """Compute portfolio returns

  Parameters
  ----------
  weights: array_like
    Weights of assets in portfolio, from 0 to 1
  returns_series: pd.Dataframe
    Series of assets returns
  Returns
  -------
  float
    Total portfolio returns based on asset weights

  Note
  -------
  For matrix multiplication the number of columns im matrix #1 must be equal to number of rows in matrix #2, that's why ome matrix is transposed.
  """
  return weights.T @ returns_series


def get_portfolio_volatility(weights, covariance_matrix):
  """Compute portfolio volatility

  Parameters
  ----------
  weights: array_like
    Weights of assets in portfolio, from 0 to 1
  covariance_matrix: pd.Dataframe
    Covariance-variance matrix for assets in portfolio
  Returns
  -------
  float
    Total portfolio volatility based on asset weights and their covariance
  """
  # return np.sqrt(weights.T @ covariance_matrix @ weights)*np.sqrt(12)
  return (weights.T @ covariance_matrix @ weights)**0.5


def plot_efficient_frontier_2assets(number_of_portfolios, returns_series, covariance_matrix):
  """Computes and plots efficient frontier for 2 assets portfolio

  Parameters
  ----------
  number_of_portfolios
  returns_series
  covariance_matrix

  Returns
  -------

  """
  if returns_series.shape[0] != 2:
    raise ValueError('Can only plot Efficient Frontier for 2 assets')
  weights = [np.array([weight, 1 - weight]) for weight in np.linspace(0, 1, number_of_portfolios)]
  portfolio_returns = [get_portfolio_returns(weight, returns_series) for weight in weights]
  portfolio_volatility = [get_portfolio_volatility(weight, covariance_matrix) for weight in weights]
  efficient_frontier = pd.DataFrame({'Returns': portfolio_returns, "Volatility": portfolio_volatility})
  ax = efficient_frontier.plot.line(x='Volatility', y='Returns', style=".-", legend=False)
  ax.set(xlabel="Volatility", ylabel="Returns")
  plt.show()
  return


def get_optimal_weights(number_of_portfolios, expected_returns, covariance_matrix):
  """Computes a list of optimal weights for a list of given expected returns

  Parameters
  ----------
  number_of_portfolios
  expected_returns
  covariance_matrix

  Returns
  -------

  """
  target_returns = np.linspace(expected_returns.min(), expected_returns.max(), number_of_portfolios)
  weights = [minimize_volatility(target_return, expected_returns, covariance_matrix) for target_return in target_returns]
  return weights


def plot_efficient_frontier(number_of_portfolios, expected_returns, covariance_matrix, risk_free_rate=0, show_cml=False, show_ew_portfolio=False, show_gmv_portfolio=False, style='.-', *args):
  other_data=[]
  weights = get_optimal_weights(number_of_portfolios, expected_returns, covariance_matrix)
  portfolio_returns = [get_portfolio_returns(weight, expected_returns) for weight in weights]
  portfolio_volatility = [get_portfolio_volatility(weight, covariance_matrix) for weight in weights]
  efficient_frontier = pd.DataFrame({'Returns': portfolio_returns, "Volatility": portfolio_volatility})
  chart = efficient_frontier.plot.line(x='Volatility', y='Returns', color="darkblue", style=style)
  chart.set(xlabel="Волатильность", ylabel="Доходность")
  chart.set_xlim(left=0)
  chart.xaxis.labelpad = 20
  # plt.xticks(np.arange(0.02, max(portfolio_volatility), 0.02))
  # plt.xticks(np.arange(0.02, max(portfolio_volatility)))
  chart.spines['left'].set_position(('data', 0))
  chart.spines['bottom'].set_position(('data', 0))
  chart.spines['top'].set_visible(False)
  chart.spines['right'].set_visible(False)
  lines = [Line2D([0], [0], color='darkblue', linewidth=3, linestyle="-")]
  labels = ['Эффективное множество']
  if show_cml:
    weights_max_sharpe = maximize_sharpe_ratio(risk_free_rate, expected_returns, covariance_matrix)
    returns_max_sharpe = get_portfolio_returns(weights_max_sharpe, expected_returns)
    volatility_max_sharpe = get_portfolio_volatility(weights_max_sharpe, covariance_matrix)
    # print(f'Weights for Max Sharpe: {[round(w*100) for w in weights_max_sharpe if w > 0.01]} \nReturns Max Sharpe: {round(returns_max_sharpe*100,2)}\nVolatility Max Sharpe: {round(volatility_max_sharpe*100,2)}')
    print(f'Weights for Max Sharpe: {[x for x in enumerate([round(w*100) for w in weights_max_sharpe]) if x[1] > 0]} \nReturns Max Sharpe: {round(returns_max_sharpe*100,2)}\nVolatility Max Sharpe: {round(volatility_max_sharpe*100,2)}')
    weights_max_sharpe = [x for x in enumerate([round(w*100) for w in weights_max_sharpe]) if x[1] > 0]
    ret_max_sharpe = round(returns_max_sharpe*100,2)
    vol_max_sharpe = round(volatility_max_sharpe*100,2)
    other_data.append((weights_max_sharpe,ret_max_sharpe,vol_max_sharpe))
    # Add CML
    cml_x = [0, volatility_max_sharpe]
    cml_y = [risk_free_rate, returns_max_sharpe]
    chart.plot(cml_x, cml_y, color='green', marker='o', markersize=12, linestyle='dashed', linewidth=2)
    # chart.plot(cml_x, cml_y, color='white', markersize=0, linestyle='dashed', linewidth=0)
    lines.append(Line2D([0], [0], color='green', linewidth=3, linestyle="-"))
    labels.append('CML')
  if show_ew_portfolio:  # show equally weighted portfolio
    number_of_assets = expected_returns.shape[0]
    weights = np.repeat(1 / number_of_assets, number_of_assets)
    returns_ew_portfolio = get_portfolio_returns(weights, expected_returns)
    volatility_ew_portfolio = get_portfolio_volatility(weights, covariance_matrix)
    chart.plot([volatility_ew_portfolio], [returns_ew_portfolio], color="goldenrod", marker="o", markersize=10)
  if show_gmv_portfolio:
    weights = get_gmv_portfolio(covariance_matrix)
    returns_gmv_portfolio = get_portfolio_returns(weights, expected_returns)
    volatility_gmv_portfolio = get_portfolio_volatility(weights, covariance_matrix)
    chart.plot([volatility_gmv_portfolio], [returns_gmv_portfolio], color="midnightblue", marker="o", markersize=10)
  plt.legend(lines, labels)
  return chart, other_data


def minimize_volatility(target_return, expected_returns, covariance_matrix):
  number_of_assets = expected_returns.shape[0]  # get number of assets from returns vector
  initial_guess = np.repeat(1/number_of_assets, number_of_assets)  # start with equally weighted portfolio
  weight_constraints = ((0.0, 1.0),) * number_of_assets  # set constraints for each asset, bottom and top
  return_equals_target = {  # condition #1 - use only those returns where calculated returns equal target returns
    'type': 'eq',
    'args': (expected_returns,),
    'fun': lambda weights, expected_returns: target_return - get_portfolio_returns(weights, expected_returns)
  }
  weights_sum_to_one = {  # condition #2 - all weights must add up to 1, i.e. no shorting or leverage
    'type': 'eq',
    'fun': lambda weights: np.sum(weights) - 1
  }
  results = minimize(
                      get_portfolio_volatility, initial_guess,
                      args=(covariance_matrix,),
                      method="SLSQP",
                      options={"disp": False},
                      constraints=(return_equals_target, weights_sum_to_one),
                      bounds=weight_constraints
                    )
  return results.x


def maximize_sharpe_ratio(risk_free_rate, expected_returns, covariance_matrix):
  number_of_assets = expected_returns.shape[0]  # get number of assets from returns vector
  initial_guess = np.repeat(1/number_of_assets, number_of_assets)  # start with equally weighted portfolio
  weight_constraints = ((0.0, 1.0),) * number_of_assets  # set constraints for each asset, bottom and top
  all_weights_sum_to_one = {
    'type': 'eq',
    'fun': lambda weights: np.sum(weights) - 1
  }

  def get_negative_sharpe_ratio(weights, risk_free_rate, expected_returns, covariance_matrix):
    portfolio_returns = get_portfolio_returns(weights, expected_returns)
    portfolio_volatility = get_portfolio_volatility(weights, covariance_matrix)
    return -(portfolio_returns - risk_free_rate) / portfolio_volatility

  results = minimize(
                      get_negative_sharpe_ratio, initial_guess,
                      args=(risk_free_rate, expected_returns, covariance_matrix,),
                      method="SLSQP",
                      options={"disp" : False},
                      constraints=(all_weights_sum_to_one),
                      bounds=weight_constraints
                    )
  return results.x


def get_gmv_portfolio(covariance_matrix):
  """

  Parameters
  ----------
  covariance_matrix

  Returns
  -------

  Notes
  -----
  To calculate the GMV portfolio we set all expected (historical) returns vector to the same scalar, in this case the only way
   to maximize the Sharpe Ratio of the portfolio is to minimize the volatility of this portfolio
  """
  number_of_assets = covariance_matrix.shape[0]
  return maximize_sharpe_ratio(0, np.repeat(1, number_of_assets), covariance_matrix)