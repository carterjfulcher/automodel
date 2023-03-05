from src.interface import IEXData
import pandas as pd 

db = IEXData()


def create_model(symbol, save_to_excel=False):
  income = db.get_income_statements(symbol, n_quarters=12)
  balance_sheets = db.get_balance_sheets(symbol, n_quarters=12)
  cash_flow = db.get_cashflow_statements(symbol, n_quarters=12)

  model = pd.concat([income, balance_sheets, cash_flow], axis=1)
  model = model.loc[:,~model.columns.duplicated()].copy().T

  remove_cols = ['currency', 'filingType', 'fiscalQuarter', 'fiscalYear', 'reportDatel', 'symbol', 'id', 'key', 'subkey', 'date', 'updated']
  model = model.drop(remove_cols, axis=0, errors='ignore')
  model = model[model.columns[::-1]]


  if save_to_excel:
    model.to_excel(f"models/model-{symbol}.xlsx")
  return model

def forecast(symbol, model, save_to_excel=False):

  #calculate the change in revenue for each quarter
  model = model.T
  model['revenueChange'] = model['totalRevenue'].astype('int64').pct_change()

  average_revenue_change = model['revenueChange'].mean()
  
  # add four columns for forecasting in Qx-YYYY format
  current_quarter = (pd.Timestamp.now().quarter)
  current_year = pd.Timestamp.now().year

  quarters = [f"Q{x}-{current_year}" for x in range(current_quarter, current_quarter+4)][1:]
  model = model.T
  # append quarters as blank columns
  for quarter in quarters:
    model[quarter] = ''
  if save_to_excel:
    model.to_excel(f"models/model-{symbol}.xlsx")

companies = ['AAPL']
for company in companies:
  model = create_model(company, save_to_excel=False)
  forecast(company, model, save_to_excel=True)


