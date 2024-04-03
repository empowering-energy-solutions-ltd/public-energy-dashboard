import calendar
from datetime import time
from typing import Any, Optional, Protocol

import numpy as np
import pandas as pd
import plotly.graph_objects as go  # type: ignore
from e2sviz.data import standard_data_process as sdp  # type: ignore
from e2sviz.structure import enums as viz_enums  # type: ignore
from e2sviz.structure import viz_schema  # type: ignore
from e2sviz.visualization import plot_styles, visualize  # type: ignore

from src.utils import schema


def numeric_to_month_name(month_number: int) -> str:
  """
  Converts a numeric month to its name.

  Args:
      month_number (int): The numeric month.

  Returns:
      str: The name of the month.
  """
  return calendar.month_name[month_number]


def add_time_to_date(data: pd.DataFrame, time: time, day: int) -> pd.DataFrame:
  return data[(data.index.day == day)].index.min().replace(hour=time.hour,
                                                           minute=time.minute)


class MetaData(Protocol):
  """
  MetaData Protocol for type hinting.
    """

  metadata: dict[str, dict[str, Any]]

  def units(self, col: str) -> viz_enums.UnitsSchema:
    ...

  def siunits(self, col: str) -> viz_enums.Prefix:
    ...

  @property
  def freq(self) -> viz_schema.FrequencySchema:
    ...

  def dtype(self, col: str) -> viz_enums.DataType:
    ...

  @property
  def get_x_label(self) -> str:
    ...

  def get_y_label(self, col: str) -> str:
    ...

  def get_title(self, col: str, category: str | None = None) -> str:
    ...

  def get_legend(self, col: str) -> str:
    ...


def create_lower_lineplot(
    data: pd.DataFrame,
    target_col: str,
    page: str,
    metadata: Optional[MetaData] = None,
    working_hours: Optional[dict[str, dict[str, time]]] = None) -> go.Figure:
  """ 
  Generates the lower lineplots on both the Power & Consumption tabs.

  Args:
      data (pd.DataFrame): The data to be plotted.
      target_col (str): The column to be plotted.
      page (str): The page to be plotted.
      metadata (MetaData, optional): The metadata for the data. Defaults to None.
      working_hours (dict[str, dict[str, time]], optional): The working hours for the data. Defaults to None.

  Returns:
      go.Figure: The plotly figure.
  """
  if metadata is None:
    data_object = sdp.DataManip(data)
    metadata = data_object.metadata
  metadata.metadata[viz_schema.MetaDataSchema.FRAME][
      viz_schema.MetaDataSchema.INDEX_COLS] = [schema.HHSchema.DATETIME]
  plotter = visualize.DataViz(data=data,
                              metadata=metadata,
                              viz_selector=plot_styles.PlotlyPlot(),
                              plot_columns=[target_col])
  plotter.plot('line_plot')

  page_dict = {
      schema.HHSchema.POWER_DEMAND:
      plotter.viz_selector.container.update_layout(
          yaxis_title=schema.PageSchema.POWER,
          title=dict(text=schema.PlotSchema.PEAK_POWER),
      ),
      schema.HHSchema.ENERGY_CONSUMPTION:
      plotter.viz_selector.container.update_layout(
          yaxis_title=schema.PageSchema.ENERGY,
          title=dict(text=schema.PlotSchema.HIGH_CONSUMPTION),
      )
  }
  try:
    page_dict[page]
  except KeyError:
    pass

  if working_hours is not None:
    # Add shaded regions for working hours.
    start_time = working_hours[target_col]['start']
    end_time = working_hours[target_col]['end']
    shaded_regions: list[dict[str, Any]] = [{
        'xref':
        'x',
        'yref':
        'paper',
        'x0':
        add_time_to_date(data, start_time, day),
        'x1':
        add_time_to_date(data, end_time, day),
        'y0':
        0,
        'y1':
        1,
        'fillcolor':
        'rgba(0, 0, 0, 0.1)',
        'line': {
            'width': 0
        },
    } for day in data.index.day.unique()]

    transparent_trace = go.Scatter(
        x=[shaded_regions[-1]['x0'], shaded_regions[-1]['x1']],
        y=[0, 1],
        fill='toself',
        fillcolor='rgba(0, 0, 0, 0.1)',
        mode='none',
        legendgroup='Working Hours',
        showlegend=True,
        name='Work Hours')
    plotter.viz_selector.container.add_trace(transparent_trace)
    plotter.viz_selector.container.update_layout(shapes=shaded_regions)

  plotter.viz_selector.container.update_layout(xaxis=dict(tickformat='%a'))
  return plotter.viz_selector.container


def new_create_overview_lineplot(data: pd.DataFrame,
                                 target_col: str = 'All') -> go.Figure:
  """ 
  Generates the monthly line plot for the overview tab split across years.

  Args:
      data (pd.DataFrame): The data to be plotted.
      target_col (str, optional): The column to be plotted. Defaults to 'All'.
      
  Returns:
      go.Figure: The plotly figure.
  """
  overview_data = sdp.DataManip(data, rescale=False)
  overview_data.check_rescaling()
  overview_data.metadata.metadata[target_col][
      viz_schema.MetaDataSchema.UNITS] = viz_enums.UnitsSchema.WH
  overview_data.metadata.metadata[target_col][
      viz_schema.MetaDataSchema.PREFIX] = viz_enums.Prefix.KILO
  overview_data.resampled('1MS', func=np.sum, inplace=True)

  overview_data.check_rescaling()
  overview_data.data[
      schema.HHSchema.MONTH_OF_YEAR] = overview_data.data.index.month
  overview_data.data[schema.HHSchema.MONTH_OF_YEAR] = overview_data.data[
      schema.HHSchema.MONTH_OF_YEAR].apply(numeric_to_month_name)
  overview_data.data[schema.HHSchema.YEAR] = overview_data.data.index.year
  overview_data.metadata.metadata[viz_schema.MetaDataSchema.FRAME][
      viz_schema.MetaDataSchema.INDEX_COLS] = [schema.PlotSchema.MONTH_YEAR]
  plotter = plot_styles.PlotlyPlot()

  line_markers = schema.PLOT_MARKERS

  for i, year in enumerate(overview_data.data[schema.HHSchema.YEAR].unique()):
    year_data = overview_data.data[overview_data.data[schema.HHSchema.YEAR] ==
                                   year]
    line_marker = line_markers[i % len(line_markers)]
    overview_data.metadata.metadata[target_col][
        viz_schema.MetaDataSchema.LEGEND] = year
    resamp_viz_boi = visualize.DataViz(
        data=year_data,
        metadata=overview_data.metadata,
        viz_selector=plotter,
        plot_columns=[target_col],
        x=year_data[schema.HHSchema.MONTH_OF_YEAR])
    resamp_viz_boi.plot(plot_kind='line_plot')
    plotter.container.update_traces(marker=dict(symbol=line_marker),
                                    selector=dict(name=str(year))),

  plotter.container.update_layout(
      yaxis_title=f'{overview_data.metadata.get_y_label(target_col)}',
      xaxis_title=schema.PlotSchema.MONTH,
      title='',
  )

  return plotter.container
