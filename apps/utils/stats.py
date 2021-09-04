import scipy.stats
import pandas as pd
from . import risk
from . import annualize


def get_skewness(returns_series, ddof=0):
  """Compute the skewness of the distribution

  Parameters
  ----------
  returns_series: pd.Dataframe
    Series of returns
  ddof: int, optional, default=0
    Degrees of freedom, 0 is for population size N; 1 is for sample size N-1

  Returns
  -------
  float or pd.Dataframe
    Skewness of series of returns

  See Also
  --------
  scipy.stats.skew()
  """
  standard_deviation = returns_series.std(ddof=ddof)  # using population instead of sample
  mean_of_series = ((returns_series-returns_series.mean())**3).mean()
  return mean_of_series/standard_deviation**3


def get_kurtosis(returns_series, ddof=0):
  """Computes the kurtosis of the distribution

  Parameters
  ----------
  returns_series: pd.Dataframe
    Series of returns
  ddof: int, optional, default=0
    Degrees of freedom, 0 for population size N, 1 for sample size N-1

  Returns
  -------
  float or pd.Dataframe
    Kurtosis of series of returns

  See Also
  -------
  scipy.stats.kurtosis()

  Notes
  -----
  Scipy built in module computes excessive kurtosis, which is the difference
  between actual kurtosis and 3 (Normal Distribution kurtosis)
  """
  stadard_deviation = returns_series.std(ddof=ddof)
  mean_of_series = ((returns_series-returns_series.mean())**4).mean()
  return mean_of_series/stadard_deviation**4


def is_normal(returns_series, significance_level=0.01):
  """Apply the Jarque-Bera test to determine if a Series is normally distributed.

  Parameters
  ----------
  returns_series : pd.Dataframe
    Series of returns
  significance_level : float, optional, default=0.01
    Significance level that supports that null hypothesis is true.

  Returns
  -------
  bool
    True if returns_series is normally distributed.

  Notes
  -----
    Test shows with at least 99% confidence that the distribution is normal.
    Test shows that there is 1% confidence that distribution is not normal.
    If p-value is less or equal 0.05 the alternative hypothesis is significant.
    If p-value is less or equal 0.01 the alternative hypothesis is highly significant.
  """
  statistics, p_value = scipy.stats.jarque_bera(returns_series)
  return p_value > significance_level


def get_portfolio_stat_summary(returns_series, risk_free_rate=0.03, periods_per_year=255):
  """Compute securities portfolio statistics

  Parameters
  ----------
  returns_series: pd.DataFrame or Series
    Series of portfolio returns
  risk_free_rate: float, optional, default = 0.03
    Risk Free rate available to investor
  periods_per_year: int, optional, default = 12
    Number of periods in a year. If returns series is monthly, set to 12; if daily, set to 255

  Returns
  -------
  pd.DataFrame
    pandas Dataframe with portfolio statistics
  """
  annualized_returns = returns_series.aggregate(annualize.get_annualized_returns, periods_per_year=periods_per_year)
  annualized_volatility = returns_series.aggregate(annualize.get_annualized_volatility, periods_per_year=periods_per_year)
  annualized_sharpe_ratio = returns_series.aggregate(risk.get_sharpe_ratio, risk_free_rate=risk_free_rate, periods_per_year=periods_per_year)
  drawdown = returns_series.aggregate(lambda returns_series: risk.get_drawdown(returns_series).Drawdown.min())
  skewness = returns_series.aggregate(get_skewness)
  kurtosis = returns_series.aggregate(get_kurtosis)
  cornish_fisher_var = returns_series.aggregate(risk.get_cf_var)
  historic_cvar = returns_series.aggregate(risk.get_conditional_historic_var)
  results = pd.DataFrame({
    "Annualized Returns": annualized_returns,
    "Annualized Volatility": annualized_volatility,
    "Skewness": skewness,
    "Kurtosis": kurtosis,
    "Cornish Fischer VaR (5%)": cornish_fisher_var,
    "Historic CVaR (5%)": historic_cvar,
    "Sharpe Ratio": annualized_sharpe_ratio,
    "Maximum Drawdown": drawdown,
  })
  return results
