from src.interface import IEXData
from typing import List
import numpy as np 
import pandas as pd 

db = IEXData()


def create_model(symbol, save_to_excel=False):
  income = db.get_income_statements(symbol, n_quarters=12)
  balance_sheets = db.get_balance_sheets(symbol, n_quarters=12)
  cash_flow = db.get_cashflow_statements(symbol, n_quarters=12)

  prices = db.get_quarterly_prices(symbol, income['fiscalDate'])

  income['price'] = prices

  print(income)


  model = pd.concat([income, balance_sheets, cash_flow], axis=1)
  model = model.loc[:,~model.columns.duplicated()].copy().T

  remove_cols = ['currency', 'filingType', 'fiscalQuarter', 'fiscalYear', 'reportDate', 'symbol', 'id', 'key', 'subkey', 'date', 'updated']
  model = model.drop(remove_cols, axis=0, errors='ignore')
  model = model[model.columns[::-1]]


  if save_to_excel:
    model.to_excel(f"models/model-{symbol}.xlsx")
  return model

def forecast(symbol, model, discount, terminal_growth, save_to_excel=False):

  model = model.T

  #calculate the change in revenue for each quarter
  change_in_revenue = model['totalRevenue'].pct_change()
  avg_revenue_growth = change_in_revenue.mean()

  print(avg_revenue_growth)


  
  if save_to_excel:
    model.T.to_excel(f"models/model-{symbol}.xlsx")

companies = ['EPD']
for company in companies:
  model = create_model(company, save_to_excel=False)
  forecast(company, model, .09, .01, save_to_excel=True)


