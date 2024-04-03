import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data import loader
from src.utils.modifiers import round_to_first_x_digits


def generate_area_plot() -> go.Figure:
  """ Generates an area plot of the flat consumption as a percentage of the total.
    
    Returns:
        go.Figure: Plotly figure object."""
  dataf = loader.create_fake_flats()
  dataf = dataf[['Flat 1', 'Flat 2', 'Flat 3', 'Flat 4']]
  df_percentage = dataf.div(dataf.sum(axis=1), axis=0) * 100
  fig = px.area(df_percentage,
                x=df_percentage.index,
                y=df_percentage.columns,
                title='Flat Consumption as Percentage of Total',
                labels={
                    'index': 'Date',
                    'value': 'Percentage'
                })
  return fig


def create_table_data(dataf: pd.DataFrame, highflat: [str]) -> pd.DataFrame:
  """Creates a table of the average monthly consumption and cost for the selected flats.

    Args:
        dataf (pd.DataFrame): The data to be used.
        highflat ([str]): The selected flats.

    Returns:
        pd.DataFrame: The table of the average monthly consumption and cost."""
  columns = [
      'Flats', 'Avg monthly consumption [kWh]', 'Avg monthly cost [GBP]'
  ]
  df_table = pd.DataFrame(columns=columns)
  df_table['Flats'] = highflat
  df_table['Avg monthly consumption [kWh]'] = df_table['Flats'].apply(
      lambda x: round_to_first_x_digits(dataf[x].mean())
      if x in dataf.columns else None)
  df_table['Avg monthly cost [GBP]'] = df_table[
      'Avg monthly consumption [kWh]'] * 0.15
  return df_table
