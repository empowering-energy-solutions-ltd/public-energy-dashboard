import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from e2sviz.data import standard_data_process as sdp  # type: ignore
from e2sviz.structure import viz_schema  # type: ignore
from e2sviz.visualization import plot_styles, visualize  # type: ignore

from src.utils import schema


def create_cost_lineplot(data: pd.DataFrame,
                         val_type: str,
                         target_id: str = 'All') -> go.Figure:
  """
  Creates a line plot for invoice cost breakdown. \
  Figure can be filtered by MPR and viewed as either % or actual £. 

  Args:
      data (pd.DataFrame): Dataframe containing invoice cost breakdown.
      val_type (str): Type of value to be plotted. Either 'Percentage of total bill (%)' or 'Cost [£]'.
      target_id (str, optional): MPR to filter data by. Defaults to 'All'.

  Returns:
      go.Figure: Plotly figure object.
  """
  cols = data.columns.tolist()
  cols.remove(schema.InvoiceSchema.MPR)
  if val_type == 'Percentage of total bill (%)':
    data[cols] = data[cols].div(data[cols].sum(axis=1), axis=0)
  data = data[data[schema.InvoiceSchema.MPR] == target_id].sort_index()
  data = data.drop(columns=[schema.InvoiceSchema.MPR])
  data_object = sdp.DataManip(data, frequency='1MS')
  data_object.metadata.metadata[viz_schema.MetaDataSchema.FRAME][
      viz_schema.MetaDataSchema.INDEX_COLS] = schema.HHSchema.DATETIME
  viz_selector = plot_styles.PlotlyPlot()
  plotter = visualize.DataViz(data=data_object.data,
                              metadata=data_object.metadata,
                              viz_selector=viz_selector,
                              plot_columns=cols)
  plotter.plot(plot_kind='line_plot')
  plotter.viz_selector.container.update_layout(
      yaxis_title=val_type,
      xaxis_title=schema.PlotSchema.MONTH,
      title=schema.PlotSchema.INV_SPEND,
  )

  return plotter.viz_selector.container


def generate_duos_table() -> pd.DataFrame:
  """ 
  Creates static table for Day, Night & DUoS charges. \
  
  NOT CURRENTLY IN USE \
  
  """
  df = pd.DataFrame({
      'DUoS type': ['Red', 'Amber', 'Green', 'Day', 'Night'],
      'time_of_day': [
          '16:00 - 20:00', '10:00 - 16:00 & 20:00 - 22:00',
          '07:00 - 10:00 & 22:00 - 00:00', '00:00 - 07:00', '22:00 - 00:00'
      ],
      'Charge rate [GBP/kWh]': [0.01652, 0.00419, 0.00059, 0.201378, 0.159429]
  })
  return df


def generate_consump_duos_tabe() -> pd.DataFrame:
  """ 
  Creates static table for consumption and DUoS charges \
  across the day.
  
  NOT CURRENTLY IN USE \
  
  """
  df = pd.DataFrame({
      'Metric': [
          'Sum consumption [kWh]', 'Cost per kWh [GBP/kWh]',
          'Avg cost per hour [GBP/h]'
      ],
      'Red': [150, 0.0134, 14],
      'Amber': [120, 0.0063, 9],
      'Green': [250, 0.0014, 10],
  })
  return df
