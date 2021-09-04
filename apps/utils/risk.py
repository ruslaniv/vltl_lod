import pandas as pd
import numpy as np
from scipy.stats import norm
from . import stats
from . import annualize


# import scipy


def get_historic_var(returns_series, significance_level=5):
    """Compute historic VAR at a given confidence level.

  Parameters
  ----------
  returns_series : pd.Series
    Series of returns
  significance_level : int, optional, default=5
    Significance level.

  Returns
  -------
  positive float
    Historical Value at Risk for series of returns

  Notes
  -----
    Significance_level % of returns are below VaR and (100 - significance_level) % of returns are above VaR.
    Significance_level probability of losing VaR or more in a timeframe that series of returns represents (if daily returns, then in losing in a day).
    Confidence level (100 - significance_level) is a probability of NOT losing more than VaR in a timeframe that series of returns represents.
  """
    # TODO: Adjust for calculating monthly VaR for historical VaR
    if isinstance(returns_series, pd.DataFrame):
        # if returns_series is dataframe, call get_historic_var on every column of that dataframe
        return returns_series.aggregate(get_historic_var, significance_level=significance_level)
    elif isinstance(returns_series, pd.Series):
        return -np.percentile(returns_series, significance_level)
    else:
        raise TypeError('Expected either Dataframe or Series')


def get_gaussian_var(returns_series, significance_level=5, ddof=0):
    """Compute parametric Gaussian VAR at a given confidence level.
  Assumption is that returns_series is normally distributed

  Parameters
  ----------
  returns_series : pd.Series
    Series of returns
  significance_level : int, optional, default=5
    Significance level.
  ddof: int, optional, default=0
    Degrees of freedom, 0 is for population size N; 1 is for sample size N-1

  Returns
  -------
  positive float
    Parametric Gaussian Value at Risk for Series of returns

  Notes
  -----
    Significance_level % of returns are below VaR and (100 - significance_level) % of returns are above VaR.
    Significance_level probability of losing VaR or more in a timeframe that series of returns represents (if daily returns, then in losing in a day).
    Confidence level (100 - significance_level) is a probability of NOT losing more than VaR in a timeframe that series of returns represents.
    95% confidence level is 1 std deviation (1.65 from mean)
    99% confidence level is 2 std deviation (2.33 from mean)
  """
    # TODO: Adjust for calculating monthly VaR for Gaussian VaR
    # calculates distance (std) from mean to significance_level
    z_score = norm.ppf(significance_level / 100)
    return -(returns_series.mean() + z_score * returns_series.std(ddof=ddof))


def get_cf_var(returns_series, significance_level=5, ddof=0):
    """Compute semi-parametric Cornish-Fisher VaR at a given confidence level.
    Cornish-Fisher VaR makes adjustments to Gaussian VaR by adjusting the Z-Score to actual returns_series's \n
    skewness and kurtosis.

  Parameters
  ----------
  returns_series : pd.Series
    Series of returns
  significance_level : int, optional, default=5
    Significance level.
  ddof: int, optional, default=0
    Degrees of freedom, 0 is for population size N; 1 is for sample size N-1

  Returns
  -------
  positive float
    Semi-parametric Cornish-Fisher Value at Risk for Series of returns

  Notes
  -----
    Significance_level % of returns are below VaR and (100 - significance_level) % of returns are above VaR.
    Significance_level probability of losing VaR in a timeframe that series of returns represents (if daily returns, then in losing in a day).
    Confidence level (100 - significance_level) is a probability of NOT losing more than VaR in a timeframe that series of returns represents.
  """
    # TODO: Adjust for calculating monthly VaR for Cornish-Fisher VaR
    # Compute Z-Score as if it was Gaussian
    z_score = norm.ppf(significance_level / 100)
    skewness = stats.get_skewness(returns_series)
    # skewness = scipy.stats.skew(returns_series)
    kurtosis = stats.get_kurtosis(returns_series)
    # kurtosis = scipy.stats.kurtosis(returns_series)
    # Adjust Z-Score for actual skewness and kurtosis
    z_score = (z_score + (z_score ** 2 - 1) * skewness / 6 + (z_score ** 3 - 3 * z_score) * (kurtosis - 3) / 24 - (
            2 * z_score ** 3 - 5 * z_score) * (skewness ** 2) / 36)
    return -(returns_series.mean() + z_score * returns_series.std(ddof=ddof))


def get_conditional_historic_var(returns_series, significance_level=5):
    """Compute Conditional VaR based on historic data a given confidence level.
    It computes the average of all the returns that are beyond significance_level

  Parameters
  ----------
  returns_series: pd.Dataframe
    Series of returns
  significance_level: int, optional, default=5
    Significance level.

  Returns
  -------
   positive float

  Notes
  -----
  Shows average loss at the worst significance_level % cases
  """
    # TODO: Adjust for calculating monthly CVaR for CVaR
    # TODO: Adjust ot calculate CVaR based on other types of VaR
    if isinstance(returns_series, pd.Series):
        # Find all returns that are below historical VaR
        is_beyond = returns_series <= -get_historic_var(returns_series, significance_level=significance_level)
        # Average such returns
        return -returns_series[is_beyond].mean()
    elif isinstance(returns_series, pd.DataFrame):
        return returns_series.aggregate(get_historic_var, significance_level=significance_level)
    else:
        raise TypeError('Expected either Dataframe or Series')


def get_drawdown(returns_series):
    """Computes historical Wealth Index and maximum drawdown \n
  Maximum drawdown - is the maximum loss investor could have experienced if they bought stocks at the top and sold stocks at the bottom \n
  Parameters
  ----------
  returns_series: pd.Dataframe
    Series of returns

  Returns
  -------
  pd.Dataframe
    Wealth Index | Previous peak | Percent maximum drawdown

  Notes
  -----
    The Wealth Index inception is 100 units of currency
    To get the maximum drawdown call pd.DataFrame['Drawdown'].min()
    To get the date for maximum drawdown call pd.DataFrame['Drawdown'].idxmin()
  """
    wealth_index = 100 * (1 + returns_series).cumprod()  # compute the growth of 100 dollars
    previous_peaks = wealth_index.cummax()  # compute the cumulative maximum value of growth index at any given time
    drawdown = (wealth_index - previous_peaks) / previous_peaks  # compute drawdown in percent of the loss relative to the previous peak
    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peak": previous_peaks,
        "Drawdown": drawdown
    })


def get_maximum_drawdown_and_date(returns_series):
    """Computes maximum drawdown and the date it occurred

  Parameters
  ----------
  returns_series: pd.Dataframe
    Series of returns

  Returns
  -------
  dictionary
    Percent maximum drawdown, Maximum drawdown date
  """
    df = get_drawdown(returns_series)
    maximum_drawdown = df['Drawdown'].min().round(2) * 100
    maximum_drawdown_date = df['Drawdown'].idxmin().strftime('%B, %Y')
    return {
        'Maximum drawdown': maximum_drawdown,
        'Maximum drawdown date': maximum_drawdown_date
    }


def get_semi_deviation(returns_series, ddof=0):
    """Computes semideviation of a negative side of series of returns

  Parameters
  ----------
  returns_series: pd.Series
    Series of returns
  ddof: int, optional, default=0
    Degrees of freedom, 0 is for population size N; 1 is for sample size N-1

  Returns
  -------
  float
    Semideviation of series of returns
  """
    is_negative = returns_series < 0
    return returns_series[is_negative].std(ddof=ddof)


def get_sharpe_ratio(returns_series, risk_free_rate=0.03, periods_per_year=255):
    """Computes the Sharpe Ratio for series of returns

  Parameters
  ----------
  returns_series: pd.Series
    Series of returns
  risk_free_rate: float
    Risk Free rate
  periods_per_year: int
    Number of periods that returns series is in in a year

  Returns
  -------
  float
    Sharpe Ratio
  """
    # convert annual risk free rate to per period
    risk_free_rate_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess_returns = returns_series - risk_free_rate_per_period
    annualized_excess_returns = annualize.get_annualized_returns(excess_returns, periods_per_year)
    annualized_volatility = annualize.get_annualized_volatility(returns_series, periods_per_year)
    return annualized_excess_returns / annualized_volatility
