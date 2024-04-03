from typing import Any, Optional

import dash_ag_grid as dag  # type: ignore
import pandas as pd
from dash import dcc, html  # type: ignore
from plotly import graph_objects as go  # type: ignore

# from src.components.filter_objects import box_options
from src.utils import IDS


def graph_obj(tab_title: str, figure: go.Figure, id: int = 0) -> html.Div:
  """ 
  Puts a plotly figure into a dcc.Graph object with an ID so that it can be \
  identified by the callbacks.

  Args:
      tab_title (str): The title of the tab used in the id generation.
      figure (go.Figure): The plotly figure to be displayed.
      id (int, optional): The id of the figure. Defaults to 0.

  Returns:
      html.Div: The dcc.Graph object to be displayed."""
  return html.Div(dcc.Graph(id=tab_title + IDS.FIGURE + str(id),
                            figure=figure),
                  style={'text-align': 'center'})


def add_hline(fig: go.Figure, y_val: int, name: str) -> go.Figure:
  """
  Adds a horizontal line to a plotly figure.

  Args:
      fig (go.Figure): The plotly figure to add the line to.
      y_val (int): The y value of the line.
      name (str): The name of the line.

  Returns:
      go.Figure: The plotly figure with the line added."""
  if y_val == 0:
    return fig
  else:
    line = go.Scatter(x=[fig.data[0].x[0], fig.data[0].x[-1]],
                      y=[y_val, y_val],
                      mode='lines',
                      line=dict(dash="dash", color="red"),
                      name=name)
    fig.add_trace(line)
    return fig


def add_x_range_box_to_legend(fig: go.Figure, x_start: int, x_end: int,
                              name: str) -> go.Figure:
  """
  Adds a box to the legend of a plotly figure.

  Args:
      fig (go.Figure): The plotly figure to add the box to.
      x_start (int): The start x value of the box.
      x_end (int): The end x value of the box.
      name (str): The name of the box.

  Returns:
      go.Figure: The plotly figure with the box added.
  """
  box = go.Scatter(
      x=[x_start, x_end, x_end, x_start, x_start],
      y=[
          fig.layout.yaxis.range[0], fig.layout.yaxis.range[0],
          fig.layout.yaxis.range[1], fig.layout.yaxis.range[1],
          fig.layout.yaxis.range[0]
      ],
      mode='lines',
      fill='toself',
      fillcolor='rgba(0,0,255,0.2)',  # Set the color and opacity of the box
      line=dict(color='rgba(0,0,0,0)'),  # Set line color to transparent
      name=name)
  fig.add_trace(box)
  return fig


def table_obj(tab_title: str,
              data: pd.DataFrame,
              id: int = 0,
              page_fit: Optional[str] = "responsiveSizeToFit",
              colour: bool = False,
              pinned_val: bool = False) -> html.Div:
  """ 
  Generates Ag-Grid table object with ID and formatting.

  Args:
      tab_title (str): The title of the tab used in the id generation.
      data (pd.DataFrame): The data to be displayed in the table.
      id (int, optional): The id of the table. Defaults to 0.
      page_fit (Optional[str], optional): The page fit of the table. Defaults to "responsiveSizeToFit".
      colour (bool, optional): Whether to colour the table. Defaults to False.
      pinned_val (bool, optional): Whether to pin the first column. Defaults to False.
      
  Returns:
      html.Div: The Ag-Grid table object to be displayed.
  """
  cell_styles = {'textAlign': 'center'}
  columnDefs = []

  for x, i in enumerate(data.columns):
    column_def = {
        "headerName": i,
        "field": i,
        "cellStyle": cell_styles,
    }
    if x == 0:
      column_def["pinned"] = f"{pinned_val}"
      column_def['headerCheckboxSelection'] = "True"
      column_def['checkboxSelection'] = "True"
    columnDefs.append(column_def)
  if colour:
    columnDefs[-1]['styleConditions'] = generate_style_conditions()
  copy_to_clipboard_div = html.Div([
      html.Span("Copy to clipboard:", style={"float": "left"}),
      dcc.Clipboard(id=tab_title + "clipboard" + str(id),
                    title="Copy to clipboard",
                    style={"float": "left"})
  ])
  ag_grid = dag.AgGrid(
      id=tab_title + IDS.TABLE + str(id),
      rowData=data.to_dict("records"),
      defaultColDef={
          "editable": True,
          "resizable": True,
          "skipHeader": False,
          "wrapHeaderText": True,
      },
      columnSize=page_fit,
      columnDefs=columnDefs,
      dashGridOptions={
          "domLayout": "autoHeight",
          "rowSelection": "multiple",
      },
      style={
          "height": "100%",
          # "width": "100%"
      },
  )
  return html.Div([
      html.Div(copy_to_clipboard_div, style={"display": "flex"}),
      html.Div(ag_grid, style={"display": "flex"})
  ])


def generate_style_conditions() -> list[dict[str, Any]]:
  """ Style conditions for the Ag-Grid table. NOT IN USE. """
  style_conditions = [
      {
          'condition': "params.value < 80",
          'style': {
              'backgroundColor': 'yellowgreen'
          },
      },
      {
          "condition": "80 <= params.value <= 95",
          "style": {
              "backgroundColor": "orange"
          },
      },
      {
          "condition": "params.value >= 95",
          "style": {
              "backgroundColor": "orangered"
          },
      },
  ]
  return style_conditions
