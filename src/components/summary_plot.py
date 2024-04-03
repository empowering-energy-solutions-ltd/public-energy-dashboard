from typing import Any

import pandas as pd
import plotly.graph_objects as go  # type: ignore

import src.utils.schema as schema
from src.utils.schema import PageSchema  # SankeySchema,
from src.utils.schema import SankeyTwoSchema, SummarySchema


def overview_sankey() -> go.Figure:
  """
  Creates a Sankey diagram of the energy flows. Check the Sankey schemas to switch to a different layout.

  Returns:
      go.Figure: Plotly figure object.
  """
  sankey = go.Figure(data=[
      go.Sankey(valueformat=".0f",
                valuesuffix="kWh",
                node=dict(
                    pad=15,
                    thickness=15,
                    line=dict(color="black", width=0.5),
                    label=SankeyTwoSchema.label_list,
                    color=SankeyTwoSchema.block_colour_list,
                ),
                link=dict(source=SankeyTwoSchema.source_list,
                          target=SankeyTwoSchema.target_list,
                          value=SankeyTwoSchema.value_list,
                          color=SankeyTwoSchema.flow_colour_list))
  ])
  legend_items = [
      go.Scatter(x=[None],
                 y=[None],
                 mode='markers',
                 marker=dict(size=12,
                             line=dict(width=2, color='DarkSlateGrey'),
                             color='rgba(219, 39, 13, 1)'),
                 name=PageSchema.ELEC),
      go.Scatter(x=[None],
                 y=[None],
                 mode='markers',
                 marker=dict(size=12,
                             line=dict(width=2, color='DarkSlateGrey'),
                             color='rgba(216, 205, 0, 1)'),
                 name=PageSchema.GAS),
      go.Scatter(x=[None],
                 y=[None],
                 mode='markers',
                 marker=dict(size=12,
                             line=dict(width=2, color='DarkSlateGrey'),
                             color='rgba(0,158,115, 1)'),
                 name=PageSchema.HEAT),
  ]

  sankey.update_layout(
      showlegend=True,
      plot_bgcolor='rgba(0,0,0,0)',
      xaxis_visible=False,
      yaxis_visible=False,
      legend=dict(font=dict(size=12)),
  )

  for item in legend_items:
    sankey.add_trace(item)
  return sankey


KWH_TO_MWH = 0.001


def calculate_statistics(month_data: pd.DataFrame, no_years: int,
                         units: str) -> tuple[Any, Any, Any, Any, Any]:
  """
  Calculates the current, most recent, median, minimum and maximum values for the selected month.

  Args:
      month_data (pd.DataFrame): The data for the selected month.
      no_years (int): The number of years of data.
      units (str): The units to be used.

  Returns:
      tuple[Any, Any, Any, Any, Any]: The current, most recent, median, minimum and maximum values.
  """
  if units == schema.PlotSchema.E_MWH:
    multiplier: float = KWH_TO_MWH
  else:
    multiplier: float = 1
  if len(month_data) == 0:
    return SummarySchema.NO_DATA, SummarySchema.NO_DATA, SummarySchema.NO_DATA, SummarySchema.NO_DATA, SummarySchema.NO_DATA
  elif len(month_data) < no_years:
    current_value = SummarySchema.NO_DATA
    most_recent_value = round(
        month_data.iloc[-1].astype(float).sum() * multiplier, 2)
  else:
    current_value = round(month_data.iloc[-1].astype(float).sum() * multiplier,
                          2)
    most_recent_value = round(
        month_data.iloc[-2].astype(float).sum() * multiplier, 2)
  median_value = round(month_data.median().astype(float).sum() * multiplier, 2)
  min_value = round(month_data.min().astype(float).sum() * multiplier, 2)
  max_value = round(month_data.max().astype(float).sum() * multiplier, 2)
  return current_value, most_recent_value, median_value, min_value, max_value


def create_summary_table(df_monthly: pd.DataFrame,
                         table_units: str = 'Energy',
                         target_col: str = 'All') -> pd.DataFrame:
  """
  Creates a table of the monthly statistics for the selected meter.

  Args:
      df_monthly (pd.DataFrame): The monthly data.
      table_units (str, optional): The units to be used. Defaults to 'Energy'.
      target_col (str, optional): The column to be used. Defaults to 'All'.

  Returns:
      pd.DataFrame: The table of the monthly statistics.
  """
  no_years: int = df_monthly.index.year.nunique()
  index_list = [
      SummarySchema.CURRENT, SummarySchema.PREV, SummarySchema.MEDIAN,
      SummarySchema.MIN, SummarySchema.MAX
  ]
  columns = schema.MONTHS
  dataf = pd.DataFrame(index=index_list, columns=columns)
  for month in columns:
    month_data: pd.DataFrame = df_monthly[df_monthly.index.month ==
                                          columns.index(month) + 1][target_col]
    current, most_recent, median, min_val, max_val = calculate_statistics(
        month_data, no_years, table_units)
    dataf.loc[SummarySchema.CURRENT, month] = current
    dataf.loc[SummarySchema.PREV, month] = most_recent
    dataf.loc[SummarySchema.MEDIAN, month] = median
    dataf.loc[SummarySchema.MIN, month] = min_val
    dataf.loc[SummarySchema.MAX, month] = max_val
  dataf.reset_index(inplace=True)
  dataf.rename(columns={'index': schema.PlotSchema.E_MWH}, inplace=True)
  return dataf
