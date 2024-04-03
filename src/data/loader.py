from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils import schema


def prep_gas_data() -> pd.DataFrame:
  """
  Formats the half hourly gas data from Total and returns a DataFrame.

  Returns:
      pd.DataFrame: The formatted half hourly gas data.
  """
  dataf = pd.read_csv(r"src/data/gas_hh_data.csv",
                      index_col=None,
                      parse_dates=True)
  read_date = schema.InvoiceSchema.READDATE
  time = schema.InvoiceSchema.TIME
  df = pd.melt(dataf,
               id_vars=[read_date, schema.InvoiceSchema.MPR_2],
               var_name=time,
               value_name='Value')

  df[time] = df[time].str[-4:]
  mask = df[time] == '2400'
  df.loc[mask, time] = '0000'

  df[read_date] = pd.to_datetime(df[read_date], format='%d/%m/%Y')
  df.loc[mask, read_date] = df.loc[mask, read_date] + pd.Timedelta(days=1)
  df[read_date] = df[read_date].astype(str)

  df[schema.HHSchema.DATETIME] = pd.to_datetime(
      df[read_date] + ' ' + df[time],
      format='%Y-%m-%d %H%M') - pd.Timedelta(minutes=30)

  final_df = df.pivot(index=schema.HHSchema.DATETIME,
                      columns=schema.InvoiceSchema.MPR_2,
                      values='Value')
  final_df = final_df * schema.SM3_TO_KWH
  return final_df


def load_hh_data(resample: Optional[str],
                 utility: str = schema.PageSchema.ELEC) -> pd.DataFrame:
  """
  Loads the half hourly data for the given utility and resamples it if required.

  Args:
      resample (Optional[str]): The resampling frequency.
      utility (str, optional): The utility type. Defaults to schema.PageSchema.ELEC.

  Returns:
      pd.DataFrame: The half hourly data.
  """
  if utility == schema.PageSchema.ELEC:
    dataf = pd.read_csv(r"src/data/elec_hh_data.csv",
                        index_col=0,
                        parse_dates=True)
    for col in dataf.columns:
      if dataf[col].dtype == object:
        dataf[col] = dataf[col].str.replace(',', '')
        dataf[col] = dataf[col].astype(float)
  else:
    dataf = prep_gas_data()
  if resample:
    dataf = dataf.resample(resample).sum()
  dataf['All'] = dataf.sum(axis=1)
  dataf[schema.HHSchema.MONTH_OF_YEAR] = dataf.index.month  # type: ignore
  return dataf


def load_elec_invoice_data() -> pd.DataFrame:
  """
  Pulls and formats the electricity invoice data from the csv file.

  Returns:
      pd.DataFrame: The formatted electricity invoice data.
  """
  data_path = Path(r"src/data/electric_invoice_data.csv")

  dataf = pd.read_csv(data_path, index_col=0, parse_dates=True)
  dataf = dataf.loc['2022-09-01':]
  dataf_resample = dataf.drop([schema.InvoiceSchema.MPAN_MPR], axis=1).copy()
  dataf_resample = dataf_resample.resample('1MS').sum()
  dataf_resample = dataf_resample.sort_index()
  dataf_resample[schema.InvoiceSchema.MPAN_MPR] = dataf[
      schema.InvoiceSchema.MPAN_MPR].resample('1MS').last()
  filtered_columns = dataf_resample.filter(like=schema.InvoiceSchema.CHARGE,
                                           axis=1)
  filtered_columns = filtered_columns.assign(
      mpr=dataf_resample[schema.InvoiceSchema.MPAN_MPR].copy(deep=True))
  dataf = filtered_columns
  fixed_charges = [
      schema.InvoiceSchema.SITE + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.AVAILABILITY + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.DISTRIB + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.DATA + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.SETTLEMENT + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.NETWORK + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.REACTIVE + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.RECONCILIATION + schema.InvoiceSchema.CHARGE,
      schema.InvoiceSchema.STANDING + schema.InvoiceSchema.CHARGE
  ]
  new_column: pd.Series[float] = dataf[fixed_charges].sum(axis=1)
  dataf = dataf.copy()
  dataf[schema.InvoiceSchema.FIXED_CHARGES +
        schema.InvoiceSchema.CHARGE] = new_column
  dataf = dataf.drop(columns=fixed_charges)
  dataf = dataf.reset_index()
  sum_consumption = dataf.groupby(['index', schema.InvoiceSchema.MPR
                                   ]).sum().reset_index()
  sum_all = sum_consumption.groupby('index').sum().reset_index()
  sum_all[schema.InvoiceSchema.MPR] = 'All'
  # Set 'period_from' as the index of the 'sum_all' DataFrame
  sum_all = sum_all.set_index('index')
  dataf = dataf.set_index('index')
  # Concatenate the 'All' row with the original DataFrame
  dataf = pd.concat([dataf, sum_all])
  # cols = dataf.columns.tolist()
  # cols.remove('mpr')
  dataf = dataf.dropna()
  return dataf


def load_gas_invoice_data() -> pd.DataFrame:
  """
  Pulls and formats the gas invoice data from the csv file.

  Returns:
      pd.DataFrame: The formatted gas invoice data.
  """
  data_path = Path(r"src/data/gas_invoice_data.csv")
  dataf = pd.read_csv(data_path, index_col=1, parse_dates=True)
  dataf = dataf.loc['2022-09-01':]
  dataf = dataf.drop(columns=[schema.InvoiceSchema.UNNAMED])
  #     schema.InvoiceSchema.NET, schema.InvoiceSchema.UNNAMED,
  #     schema.InvoiceSchema.ACCOUNT, schema.InvoiceSchema.TOTAL_GAS,
  #     schema.InvoiceSchema.CONSUMPTION_KWH
  # ])
  dataf = dataf.reset_index()

  sum_consumption = dataf.groupby(
      [schema.InvoiceSchema.PERIOD_FROM,
       schema.InvoiceSchema.MPR]).sum().reset_index()
  sum_all = sum_consumption.groupby(
      schema.InvoiceSchema.PERIOD_FROM).sum().reset_index()
  sum_all[schema.InvoiceSchema.MPR] = 'All'
  # Set 'period_from' as the index of the 'sum_all' DataFrame
  sum_all = sum_all.set_index(schema.InvoiceSchema.PERIOD_FROM)
  dataf = dataf.set_index(schema.InvoiceSchema.PERIOD_FROM)
  # Concatenate the 'All' row with the original DataFrame
  dataf = pd.concat([dataf, sum_all])
  cols = dataf.columns.tolist()
  cols.remove(schema.InvoiceSchema.MPR)
  for col in cols:
    if dataf[col].dtype == object:
      dataf[col] = pd.to_numeric(dataf[col].str.replace(',', ''),
                                 errors='coerce')
  dataf.rename(columns={
      'cost_per_meter': 'Cost Per Meter [GBP]',
      'ccl_total': 'Climate Change Levy [GBP]',
      'standing_charge': 'Standing Charges [GBP]',
      'vat_total': 'VAT Charge [GBP]'
  },
               inplace=True)
  return dataf


def load_invoice_cost_data(energy_type: str) -> pd.DataFrame:
  """
  Loads the invoice cost data for the given energy type.

  Args:
      energy_type (str): The energy type.

  Returns:
      pd.DataFrame: The invoice cost data.
  """
  dataf: pd.DataFrame = pd.DataFrame()
  if energy_type == schema.PageSchema.ELEC:
    dataf = load_elec_invoice_data()
  elif energy_type == schema.PageSchema.GAS:
    dataf = load_gas_invoice_data()
  return dataf


def load_duos_data() -> pd.DataFrame:
  """
  Loads the generated DUOS data from the csv file.

  Returns:
      pd.DataFrame: The DUOS data.
  """
  data_path = Path(r"src/data/duos_data.csv")
  df = pd.read_csv(data_path, index_col=0, parse_dates=True)
  df = df.sort_index()
  df.index = df.index.hour  # type: ignore
  return df
