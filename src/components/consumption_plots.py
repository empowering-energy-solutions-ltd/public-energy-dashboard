from datetime import datetime, time, timedelta
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

from src.components import gen_content_obj, line_fig
from src.utils import IDS, schema

WORK_HOURS = {
    f'{IDS.ELEC_MPR_1}': {
        'start': time(8, 0, 0),
        'end': time(18, 0, 0)
    },
    f'{IDS.ELEC_MPR_3}': {
        'start': time(8, 0, 0),
        'end': time(18, 0, 0)
    },
    f'{IDS.ELEC_MPR_2}': {
        'start': time(8, 0, 0),
        'end': time(18, 0, 0)
    },
}


def create_consumption_lineplot(data: pd.DataFrame, selected_meter_id: Any,
                                selected_baseline: str,
                                selected_date: datetime) -> go.Figure:
  """ 
  This uses the create_lower_lineplot function to create the high consumption \
  lineplot and adds a horizontal line to the plot at the selected baseline value.

  Args:
      data (pd.DataFrame): The data to be plotted.
      selected_meter_id (Any): The meter mpr to be plotted.
      selected_baseline (str): The baseload to be plotted [monthly, seasonal, annually].
      selected_date (datetime): The date to be plotted (the peak consumption period +- 3 days).

  Returns:
      go.Figure: The lineplot with the horizontal line at the selected baseline value.
  """
  added_time = WORK_HOURS[selected_meter_id]['end']
  time_dur = pd.Timedelta(hours=added_time.hour,
                          minutes=added_time.minute,
                          seconds=added_time.second)
  chosen_date = pd.to_datetime(selected_date) + time_dur
  start_date = pd.to_datetime(selected_date) - pd.DateOffset(days=3)
  end_date = chosen_date + pd.DateOffset(days=3, hours=12)
  filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
  baseline_dataf = create_baselines(data, selected_meter_id)
  hline_val: float = baseline_dataf.loc[chosen_date][selected_baseline]
  fig = gen_content_obj.add_hline(line_fig.create_lower_lineplot(
      filtered_data,
      selected_meter_id,
      working_hours=WORK_HOURS,
      page=schema.HHSchema.ENERGY_CONSUMPTION),
                                  y_val=hline_val,
                                  name=f"{selected_baseline} baseload")
  return fig


def create_high_demand_table(df: pd.DataFrame,
                             target_col: str = 'All') -> pd.DataFrame:
  """ 
  This function creates a table of the top 10 peak consumption periods. \
  The dates are also used for the callback to update the lineplot.

  Args:
      df (pd.DataFrame): The data to be used for the table.
      target_col (str, optional): The column to be used for the peak consumption. Defaults to 'All'.

  Returns:
      pd.DataFrame: The top 10 peak consumption periods.
  """
  df = df.fillna(0)
  df['peak_consump'] = df[target_col].rolling(8, min_periods=1).sum().round(2)
  df = df.sort_values(by='peak_consump', ascending=False)
  df[schema.HHSchema.DATETIME] = df.index
  df = df[[schema.HHSchema.DATETIME, target_col, 'peak_consump']].head(10)
  return df.rename(
      columns={
          target_col: schema.PlotSchema.PERIOD_CONSUMP,
          'peak_consump': schema.PlotSchema.POTENT_CONSUMP
      })


def create_baselines(dataf: pd.DataFrame,
                     target_col: str = 'All') -> pd.DataFrame:
  """ 
  This function creates the annual, seasonal and monthly baselines from the data.

  Args:
      dataf (pd.DataFrame): The data to be used for the baselines.
      target_col (str, optional): The column to be used for the baselines. Defaults to 'All'.

  Returns:
      pd.DataFrame: The data with the annual, seasonal and monthly baselines.
  """

  if not isinstance(dataf.index, pd.DatetimeIndex):
    raise ValueError(
        "The index should be a DatetimeIndex for year-based calculations.")

  dataf[schema.HHSchema.YEAR] = dataf.index.year
  dataf[schema.HHSchema.SEASON_OF_YEAR] = np.select([
      dataf[schema.HHSchema.MONTH_OF_YEAR].isin([12, 1, 2]),
      dataf[schema.HHSchema.MONTH_OF_YEAR].isin([3, 4, 5]),
      dataf[schema.HHSchema.MONTH_OF_YEAR].isin([6, 7, 8]),
      dataf[schema.HHSchema.MONTH_OF_YEAR].isin([9, 10, 11]),
  ], [1, 2, 3, 4], None)

  dataf[schema.HHSchema.WORK_HOURS] = np.where(
      (dataf.index.hour >= 8) & (dataf.index.hour <= 18), 1, 0)
  dataf['Annual'] = dataf.groupby(
      schema.HHSchema.YEAR)[target_col].transform(lambda x: x.quantile(0.10))
  dataf['Seasonal'] = dataf.groupby([
      schema.HHSchema.YEAR, schema.HHSchema.SEASON_OF_YEAR
  ])[target_col].transform(lambda x: x.quantile(0.10))
  dataf['Monthly'] = dataf.groupby([
      schema.HHSchema.YEAR, schema.HHSchema.MONTH_OF_YEAR
  ])[target_col].transform(lambda x: x.quantile(0.10))
  return dataf


def new_baseline_barplot(dataf: pd.DataFrame,
                         target_col: str,
                         baseline: str = 'Monthly') -> go.Figure:
  """ 
  This function creates a barplot of the annual, seasonal or monthly baselines.

  Args:
      dataf (pd.DataFrame): The data to be used for the barplot.
      target_col (str): The column to be used for the baselines.
      baseload (str, optional): The baseline to be plotted [monthly, seasonal, annually]. Defaults to 'Monthly'.

  Returns:
      go.Figure: The barplot of the annual, seasonal or monthly baselines.
  """
  data = create_baselines(dataf, target_col=target_col)

  baseline_dict_two = {
      'Annual': schema.SummarySchema.ALL,
      'Seasonal': schema.HHSchema.SEASON_OF_YEAR,
      'Monthly': schema.HHSchema.MONTH_OF_YEAR
  }

  x_label_dict = {'Annual': 'Year', 'Seasonal': 'Season', 'Monthly': 'Month'}

  if baseline == 'Annual':
    new_df = data.groupby(schema.HHSchema.YEAR)[baseline].mean().reset_index()
  else:
    new_df = data.groupby([baseline_dict_two[baseline], schema.HHSchema.YEAR
                           ])[baseline].mean().reset_index()
    new_df[baseline_dict_two[baseline]] = new_df[
        baseline_dict_two[baseline]].astype(int)
  new_df[schema.HHSchema.YEAR] = new_df[schema.HHSchema.YEAR].astype(str)

  baseline_tick_vals = {
      'Annual': [schema.SummarySchema.ALL],
      'Seasonal': schema.SEASONS,
      'Monthly': schema.MONTHS
  }
  if baseline == 'Annual':
    new_df[schema.SummarySchema.ALL] = schema.SummarySchema.ALL

    # Plot using Plotly Express
    fig = px.bar(new_df,
                 x=baseline_dict_two[baseline],
                 y=baseline,
                 color=schema.HHSchema.YEAR,
                 barmode='group',
                 labels={'Annual': 'Value'},
                 title=f'Off hours {baseline} baseload consumption value',
                 color_discrete_map={
                     '2021': schema.ColourSchema.YELLOW_BLOCK,
                     '2022': schema.ColourSchema.RED_BLOCK,
                     '2023': schema.ColourSchema.GREEN_BLOCK
                 })
  else:
    fig = px.bar(new_df,
                 x=baseline_dict_two[baseline],
                 y=baseline,
                 color=schema.HHSchema.YEAR,
                 labels={
                     baseline_dict_two[baseline]: x_label_dict[baseline],
                     'value': 'Baseload consumption [kWh]'
                 },
                 title=f'Off hours {baseline} baseload consumption value',
                 barmode='group',
                 color_discrete_map={
                     '2021': schema.ColourSchema.YELLOW_BLOCK,
                     '2022': schema.ColourSchema.RED_BLOCK,
                     '2023': schema.ColourSchema.GREEN_BLOCK
                 })
  fig.update_layout(xaxis=dict(tickvals=new_df[
      baseline_dict_two[baseline]].unique().tolist(),
                               ticktext=baseline_tick_vals[baseline]))
  fig.update_layout(yaxis_title='Baseload [kWh]')

  return fig


def new_consump_periods(data: pd.DataFrame,
                        target_col: str,
                        baseline_type: str = 'Monthly') -> pd.DataFrame:
  """ 
  This function generates the top 10 peak consumption period dataframe.

  Args:
      data (pd.DataFrame): The data to be used for the table.
      target_col (str): The column to be used for the peak consumption.
      baseline_type (str, optional): The baseline to be used for the percentage above baseline. Defaults to 'Monthly'.
      
  Returns:
      pd.DataFrame: The top 10 peak consumption periods.
  """
  dataf = create_baselines(data, target_col=target_col)
  periods = []
  current_period = []
  dataf = dataf[dataf[schema.HHSchema.WORK_HOURS] == 0]
  prev_date = None
  for index, row in dataf.iterrows():
    current_date: datetime = index
    if prev_date is not None:
      delta_time: float = (current_date - prev_date).total_seconds() / 3600
      if delta_time == 0.5:
        current_period.append(row)
      else:
        consump: float = sum(row[target_col] for row in current_period)
        if consump == 0:
          consump = 1
        if row[baseline_type] == 0:
          perc_above_baseline = 0
        else:
          val: float = row[baseline_type]
          perc_above_baseline: float = round(
              (consump / (val * delta_time) * 100), 0)
        periods.append({
            schema.HHSchema.START_DATE:
            current_period[0].name,
            schema.HHSchema.END_DATE:
            current_period[0].name + timedelta(hours=delta_time),
            'total_consumption':
            consump,
            'period_est_consumption':
            round(row[baseline_type] * delta_time, 0),
            'perc_above_baseline':
            perc_above_baseline
        })
        current_period = []
        current_period.append(row)

    prev_date = current_date

  data = pd.DataFrame(periods)
  data.index = pd.DatetimeIndex(data[schema.HHSchema.START_DATE])
  data.rename(columns={
      schema.HHSchema.START_DATE: schema.PageSchema.START_DATE,
      schema.HHSchema.END_DATE: schema.PageSchema.END_DATE,
      'total_consumption': schema.PageSchema.PERIOD_CONSUMP,
      'period_est_consumption': schema.PageSchema.EXP_CONSUMP,
      'perc_above_baseline': schema.PageSchema.PERC_BASELINE
  },
              inplace=True)

  data.sort_values(by=schema.PageSchema.PERC_BASELINE,
                   ascending=False,
                   inplace=True)
  data[schema.PageSchema.PERIOD_CONSUMP] = data[
      schema.PageSchema.PERIOD_CONSUMP].apply(lambda x: round(x, 2))
  return data.head(10)
