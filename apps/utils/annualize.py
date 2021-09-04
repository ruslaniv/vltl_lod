import numpy as np
import pandas as pd


def get_annualized_volatility(returns_series, periods_per_year):
  """Compute annualized volatility

  Parameters
  ----------
  returns_series: one dimensional array
    Series of returns
  periods_per_year: int
    Number of given periods in a year

  Returns
  -------
  float or pd.Dataframe
    Annualized volatility for series of returns
  """
  return returns_series.std()*(periods_per_year**0.5)


def get_annualized_returns(returns_series, periods_per_year):
  """Compute annualized returns rate

  Parameters
  ----------
  returns_series: one dimensional array
    Series of returns
  periods_per_year: int
    Number of given periods in a year

  Returns
  -------
  float or pd.DataFrame
    Annualized returns rate for series of returns

  """

  '''
  Not sure if this test is required since data will ONLY be provided as Series
  if not (isinstance(returns_series, pd.Series) or isinstance(returns_series, np.ndarray)):
    raise TypeError(f"Only one dimensional arrays are supported. Your supplied {returns_series.shape[1]}-dimensinal array")
  '''

  compounded_growth = (1+returns_series).prod()
  number_of_periods = returns_series.shape[0]
  #np.expm1(np.power(np.log1p(returns_series).sum(), (periods_per_year/number_of_periods)))
  return compounded_growth**(periods_per_year/number_of_periods)-1


def get_annualized_rate(instantaneous_rate):
  """Compute instantaneous interest rate
  Converts annual interest rate to interest rate when number of periods reaches infinity.

  Parameters
  ----------
  instantaneous_rate: float
    Instantaneous interest rate
  Returns
  -------
  float: Annualized interest  rate
  """
  return np.expm1(instantaneous_rate)


def get_instantaneous_rate(annualized_rate):
  """Compute annualized interest rate
  Converts instantaneous interest rate to annual interest rate with number of periods = 1
  Parameters
  ----------
  annualized_rate: float
    Annual interest rate

  Returns
  -------
  float: Instantaneous interest rate
  """

  return np.log1p(annualized_rate)

