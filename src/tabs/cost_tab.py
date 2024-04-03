import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, html  # type: ignore

from src.components import cost_plots, filter_objects, gen_content_obj
from src.data import loader
from src.tabs import general_tab
from src.utils import IDS, page_text, schema


def render() -> html.Div:
  """Renders the cost tab.

  Returns:
      html.Div: Div containing the layout for the cost tab."""
  tab_title = IDS.COST
  df = loader.load_invoice_cost_data(energy_type=schema.PageSchema.ELEC)
  meters = df[schema.InvoiceSchema.MPR].unique().tolist()
  years = df.index.year.unique()
  plot_types = ['Total charge (£)', 'Percentage of total bill (%)']

  fig = cost_plots.create_cost_lineplot(df, plot_types[0], target_id='All')

  top_plot = gen_content_obj.graph_obj(tab_title, fig)

  filt_objs = [
      filter_objects.box_options([
          filter_objects.create_sliders(tab_title, years, False),
          filter_objects.create_radioitem(tab_title=tab_title,
                                          options=plot_types,
                                          item_title='Plot value type',
                                          id_int=1)
      ]),
      filter_objects.box_options([
          filter_objects.create_radioitem(
              tab_title,
              options=[schema.PageSchema.ELEC, schema.PageSchema.GAS],
              item_title=schema.PageSchema.ECARRIER,
              id_int=0),
          filter_objects.create_dropdown(tab_title, schema.PageSchema.METERID,
                                         meters, 0)
      ])
  ]

  section_1 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.TAB_TITLE],
      section_number=0,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.OPENING_TEXT])
  section_2 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_1],
      section_number=1,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.FIRST_PLOT_TEXT],
      filter_obj=filt_objs,
      chart_table_1=top_plot)

  return html.Div([
      section_1.render_section(),
      section_2.render_section(),
      # section_3.render_section(),
      # section_4.render_section(),
  ])


@callback(
    Output(IDS.COST + IDS.FIGURE + "0", 'figure'),
    Input(IDS.COST + IDS.RADIOITEM, 'value'),
    Input(IDS.COST + IDS.DROPDOWN + "0", 'value'),
    Input(IDS.COST + IDS.RADIOITEM + "1", 'value'),
    Input(IDS.COST + IDS.RANGESLIDER, 'value'),
)
def update_fig(energy_type: str, meter_id: str, value_type: str,
               selected_years: list[int]) -> go.Figure:
  """Updates the figure based on the selected filters.
  
  Args:
      energy_type (str): The energy type selected.
      meter_id (str): The meter ID selected.
      value_type (str): The value type selected.
      selected_years (list[int]): The selected years.
      
  Returns:
      go.Figure: Plotly figure object.
  """
  dataf = loader.load_invoice_cost_data(energy_type=energy_type)
  if not selected_years:
    selected_years = [dataf.index.year.min(), dataf.index.year.max()]
  year_range = range(selected_years[0], selected_years[-1] + 1)
  filtered_data = dataf[dataf.index.year.isin(year_range)]
  fig = cost_plots.create_cost_lineplot(
      filtered_data, value_type,
      target_id=meter_id)  #   target_col).to_dict('records')
  return fig


@callback(Output(IDS.COST + IDS.DROPDOWN + "0", 'options'),
          Output(IDS.COST + IDS.DROPDOWN + "0", 'value'),
          Input(IDS.COST + IDS.RADIOITEM, 'value'))
def update_dropdown(energy_type: str) -> tuple[list[dict[str, str]], str]:
  """Updates the dropdown options based on the energy type selected.

  Args:
      energy_type (str): The selected energy type.

  Returns:
      tuple[list[dict[str, str]], str]: The dropdown options and the default value."""
  dataf = loader.load_invoice_cost_data(energy_type=energy_type)
  meter_ids = dataf[schema.InvoiceSchema.MPR].unique().tolist()
  new_options = [{
      'label': meter_id,
      'value': meter_id
  } for meter_id in meter_ids]
  value = new_options[-1]['value']
  return new_options, value


@callback(
    Output(IDS.COST + "clipboard" + "0", "content"),
    Input(IDS.COST + "clipboard" + "0", "n_clicks"),
    State(IDS.COST + IDS.TABLE + "0", "selectedRows"),
)
def selected_duos_d_n_table(n: bool,
                            table_data_selected: list[dict[str, str]]) -> str:
  """Returns the selected rows from the table as a string.

  Args:
      n (bool): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected rows from the table.

  Returns:
      str: The selected rows as a string."""
  if not table_data_selected:
    return "No selections"
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()


@callback(
    Output(IDS.COST + "clipboard" + "1", "content"),
    Input(IDS.COST + "clipboard" + "1", "n_clicks"),
    State(IDS.COST + IDS.TABLE + "1", "selectedRows"),
)
def selected_other_table(n: bool, table_data_selected: list[dict[str,
                                                                 str]]) -> str:
  """Returns the selected rows from the table as a string.

  Args:
      n (bool): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected rows from the table.
  
  Returns:
      str: The selected rows as a string."""
  if not table_data_selected:
    return "No selections"
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()


# ----------------- Removed sections -----------------

# from src.data.loader import load_rotherham_invoice_cost_data, load_duos_data, load_elec_invoice_data
# from src.data.metadata import generate_duos_metadata

# from e2sviz.data import standard_data_process as sdp
# from plotly import graph_objects as go

# dataf = loader.load_duos_data()
# data = gen_content_obj.table_obj(tab_title, cost_plots.generate_duos_table())
# data_table_2 = gen_content_obj.table_obj(
#     tab_title, cost_plots.generate_consump_duos_tabe(), 1)

# fig_2 = line_fig.create_lower_lineplot(
#     data=dataf,
#     metadata=generate_duos_metadata(),
#     target_col=dataf.columns)
# fig_2.update_layout(
#     yaxis_title='Cost per unit energy (GBP/kWh)',
#     xaxis_title='Hour of the day',
# )
# bottom_plot = gen_content_obj.graph_obj(tab_title, fig_2, 1)
# section_3 = new_general_tab.generate_page(
#     section_title=schema.tab_info(tab_title)[schema.TabSchema.SUB_TITLE_2],
#     section_number=2,
#     section_text=schema.tab_info(tab_title)[
#         schema.TabSchema.SECOND_PLOT_TEXT],
#     chart_table_1=bottom_plot)
# section_4 = new_general_tab.generate_page(
#     section_title=schema.tab_info(tab_title)[schema.TabSchema.SUB_TITLE_3],
#     section_number=3,
#     section_text=schema.tab_info(tab_title)[
#         schema.TabSchema.THIRD_PLOT_TEXT],
#     chart_table_1=data,
#     chart_table_2=data_table_2)
