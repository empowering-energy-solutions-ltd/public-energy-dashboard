from datetime import datetime
from typing import Any

import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

from src.components import gen_content_obj, line_fig
from src.data import loader
from src.utils import IDS, schema

POWER_LIMS = {
    f'{IDS.ELEC_MPR_1}': 135,
    f'{IDS.ELEC_MPR_2}': 0,
    f'{IDS.ELEC_MPR_3}': 2155,
}


def create_power_lineplot(peak_date: datetime, target_id: str) -> go.Figure:
  """ 
  Uses the line_fig module to create a line plot of the power demand from the half-hourly data.

  Args:
      peak_date (datetime): The date of the peak power demand.
      target_id (str): The meter ID of the selected meter.

  Returns:
      go.Figure: Plotly figure object.
  """
  data = loader.load_hh_data(resample=None)
  selected_date = pd.to_datetime(peak_date)
  start_date = selected_date - pd.DateOffset(days=3)
  end_date = selected_date + pd.DateOffset(days=3)
  filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
  filtered_data.loc[:, target_id] = filtered_data[target_id] * 2
  fig = gen_content_obj.add_hline(line_fig.create_lower_lineplot(
      filtered_data, target_id, page=schema.HHSchema.POWER_DEMAND),
                                  y_val=POWER_LIMS[target_id],
                                  name=schema.PlotSchema.MAX_CAP)
  return fig


def create_high_demand_table(df: pd.DataFrame,
                             target_col: str = '98765') -> pd.DataFrame:
  """
  Creates a table of the top 10 peak power demand periods for the selected meter.

  Args:
      df (pd.DataFrame): The data to be used.
      target_col (str, optional): The column to be used. Defaults to '98765'.

  Returns:
      pd.DataFrame: The table of the top 10 peak power demand periods.
  """
  power_limit = POWER_LIMS[target_col]
  dataf = df.copy()
  dataf[target_col] = round(dataf[target_col] * 2, 1)
  dataf[schema.PageSchema.PERC_LIM] = round(
      (dataf[target_col] / power_limit * 100), 0)
  dataf.sort_values(by=target_col, ascending=False, inplace=True)
  dataf[schema.HHSchema.DATETIME] = dataf.index
  df_breakdown = dataf[[
      schema.HHSchema.DATETIME, target_col, schema.PageSchema.PERC_LIM
  ]]
  list_index = []
  for index, row in df_breakdown.iterrows():
    skip_row = False
    if len(list_index):
      for existing_index in list_index:
        if abs((index - existing_index).days) <= 3:
          skip_row = True
          break
    if skip_row is False:
      list_index.append(index)
    if len(list_index) == 10:
      break

  df_breakdown = df_breakdown[df_breakdown.index.isin(list_index) == True]
  return df_breakdown


def power_demand_overview(df: pd.DataFrame) -> pd.DataFrame:
  """
  Creates a table of the power demand statistics for each meter.
  With columns for the minimum, 25th percentile, median, 75th percentile, peak and percentage of the limit.

  Args:
      df (pd.DataFrame): The data to be used.

  Returns:
      pd.DataFrame: The table of power demand statistics for each meter.
  """
  df = df * 2
  result_df = pd.DataFrame(columns=[
      schema.PowerTableSchema.COL, schema.PowerTableSchema.MIN_POWER, schema.
      PowerTableSchema.QUART_POWER, schema.PowerTableSchema.MEDIAN_POWER,
      schema.PowerTableSchema.TOP_QUART_POWER,
      schema.PowerTableSchema.PEAK_POWER, schema.PowerTableSchema.PERC_OF_LIM
  ])

  for col in df.columns:
    column_data: dict[str, Any] = {
        schema.PowerTableSchema.COL: col,
        schema.PowerTableSchema.MIN_POWER: round(df[col].quantile(0.01), 0),
        schema.PowerTableSchema.QUART_POWER: round(df[col].quantile(0.25), 0),
        schema.PowerTableSchema.MEDIAN_POWER: round(df[col].median(), 0),
        schema.PowerTableSchema.TOP_QUART_POWER: round(df[col].quantile(0.75),
                                                       0),
        schema.PowerTableSchema.PEAK_POWER: round(df[col].max(), 0),
        schema.PowerTableSchema.PERC_OF_LIM: POWER_LIMS.get(col, 0)
    }

    result_df = pd.concat([result_df, pd.DataFrame([column_data])],
                          ignore_index=True)
  return result_df


def power_load_duration_curve(dataf: pd.DataFrame,
                              target_col: str = '98765') -> go.Figure:
  """
  Creates a load duration curve for the selected meter.

  Args:
      dataf (pd.DataFrame): The data to be used.
      target_col (str, optional): The column to be used. Defaults to '98765'.
  
  Returns:
      go.Figure: Plotly figure object.
  """
  df = dataf.copy()
  df[target_col] = df[target_col] * 2
  df[schema.HHSchema.DATETIME] = df.index
  df.reset_index(inplace=True)
  df = df.sort_values(by=[target_col], ascending=False)
  df.reset_index(inplace=True)
  df.drop(columns=['index'], inplace=True)
  df.reset_index(inplace=True)
  df[schema.PowerTableSchema.PERC_HALF_HOUR] = round(
      (df['index'] + 1) / len(df) * 100, 2)
  fig = px.line(df,
                x=schema.PowerTableSchema.PERC_HALF_HOUR,
                y=target_col,
                title=schema.PowerTableSchema.LOAD_DUR)
  fig.update_xaxes(title_text=schema.PowerTableSchema.PERC_HALF_HOUR_TITLE)
  fig.update_yaxes(title_text=schema.PageSchema.POWER)
  return fig
