import requests
import pandas as pd 

class IEXData():
  def __init__(self, key=None):
    if key is None:
      with open('src/.iexkey.txt', 'r') as f:
        self.key = f.read().strip()
    else: 
      self.key = key
  
    self.base= "https://cloud.iexapis.com/stable/"

  def _quarterly_format(self, df):
    df['quarter'] = df[['fiscalQuarter', 'fiscalYear']].apply(lambda x: f"Q{x[0]}-{x[1]}", axis=1)
    return df.set_index('quarter')

  def get_balance_sheets(self, symbol, n_quarters=4):
    url = f"{self.base}/stock/{symbol}/balance-sheet?token={self.key}&period=quarter&last={n_quarters}"
    df = pd.DataFrame(requests.get(url).json()['balancesheet'])
    return self._quarterly_format(df)

  
  def get_income_statements(self, symbol, n_quarters=4):
    url = f"{self.base}/stock/{symbol}/income?token={self.key}&period=quarter&last={n_quarters}"
    df = pd.DataFrame(requests.get(url).json()['income'])
    return self._quarterly_format(df)
  
  def get_cashflow_statements(self, symbol, n_quarters=4):
    url = f"{self.base}/stock/{symbol}/cash-flow?token={self.key}&period=quarter&last={n_quarters}"
    df = pd.DataFrame(requests.get(url).json()['cashflow'])
    return self._quarterly_format(df)
  



