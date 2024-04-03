from datetime import datetime

import pandas as pd
import plotly.graph_objects as go  # type: ignore
from dash import Input, Output, State, callback, html  # type: ignore

# from dash_app import app
from src.components import filter_objects, gen_content_obj, power_plots
from src.data import loader
from src.tabs import general_tab
from src.utils import IDS, page_text, schema


def render() -> html.Div:
  """Renders the power tab.

  Returns:
      html.Div: Div containing the layout for the power tab."""
  target_col: str = '98765'
  tab_title = IDS.POWER

  new_dataf = loader.load_hh_data(resample=None)
  test_df = new_dataf.drop([schema.HHSchema.MONTH_OF_YEAR, 'All'], axis=1)

  options = test_df.columns.tolist()

  table_data = power_plots.create_high_demand_table(test_df,
                                                    target_col=target_col)
  table_data = table_data.rename(
      columns={
          target_col: schema.PageSchema.POWER,
          schema.PageSchema.PERC_LIM: schema.PageSchema.PERCENT_LIM
      })
  load_curve = gen_content_obj.graph_obj(
      tab_title,
      gen_content_obj.add_hline(power_plots.power_load_duration_curve(
          test_df, target_col=target_col),
                                y_val=power_plots.POWER_LIMS[target_col],
                                name=schema.PageSchema.MAX_CAP))
  lower_table = gen_content_obj.table_obj(
      tab_title, power_plots.power_demand_overview(test_df))
  data_table = gen_content_obj.table_obj(tab_title,
                                         table_data,
                                         id=1,
                                         colour=True)

  peak_dates: list[datetime] = table_data.index.unique().tolist()
  years: list[int] = test_df.index.year.unique()

  fig_2 = gen_content_obj.graph_obj(tab_title,
                                    power_plots.create_power_lineplot(
                                        peak_dates[0], target_col),
                                    id=1)

  filt_objs = [
      filter_objects.box_options(
          [filter_objects.create_sliders(tab_title, years, False)]),
      filter_objects.box_options([
          filter_objects.create_dropdown(tab_title, schema.PageSchema.METERID,
                                         options, 1)
      ])
  ]
  filt_objs_2 = [
      filter_objects.box_options([
          filter_objects.create_dropdown(tab_title,
                                         schema.PageSchema.DATES,
                                         peak_dates,
                                         section_no=2)
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
      chart_table_1=load_curve,
      chart_table_2=lower_table)
  section_3 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_2],
      section_number=2,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.SECOND_PLOT_TEXT],
      filter_obj=filt_objs_2,
      chart_table_1=fig_2)
  section_4 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_3],
      section_number=3,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.THIRD_PLOT_TEXT],
      chart_table_1=data_table)
  return html.Div([
      section_1.render_section(),
      section_2.render_section(),
      section_3.render_section(),
      section_4.render_section(),
  ])


@callback(Output(IDS.POWER + IDS.TABLE + "1", 'rowData'),
          Output(IDS.POWER + IDS.FIGURE + "0", 'figure'),
          Input(IDS.POWER + IDS.DROPDOWN + "1", 'value'),
          Input(IDS.POWER + IDS.RANGESLIDER, 'value'))
def update_table_and_barplot(selected_id: str,
                             selected_years: list[int]) -> tuple:
  """Updates the figure and table based on the selected filters.

  Args:
      selected_id (str): The selected meter ID.
      selected_years (list[int]): The selected years.

  Returns:
      tuple: The table data and figure."""
  dataf = loader.load_hh_data(resample=None)
  if not selected_years:
    selected_years = [dataf.index.year.min(), dataf.index.year.max()]
  filtered_data: pd.DataFrame = dataf[dataf.index.year.isin(selected_years)]
  table_data = power_plots.create_high_demand_table(filtered_data,
                                                    target_col=selected_id)
  table_data = table_data.rename(
      columns={
          selected_id: schema.PageSchema.POWER,
          schema.PageSchema.PERC_LIM: schema.PageSchema.PERCENT_LIM
      }).to_dict('records')
  fig = gen_content_obj.add_hline(power_plots.power_load_duration_curve(
      filtered_data, target_col=selected_id),
                                  y_val=power_plots.POWER_LIMS[selected_id],
                                  name=schema.PlotSchema.MAX_CAP)
  return table_data, fig


@callback(Output(IDS.POWER + IDS.FIGURE + "1", 'figure'),
          Input(IDS.POWER + IDS.DROPDOWN + "2", 'value'),
          Input(IDS.POWER + IDS.DROPDOWN + "1", 'value'))
def update_power_lineplot(selected_date: datetime,
                          selected_id: str) -> go.Figure:
  """Updates the figure based on the selected filters.

  Args:
      selected_date (datetime): The selected date.
      selected_id (str): The selected meter ID.

  Returns:
      go.Figure: Plotly figure object.
  """
  return power_plots.create_power_lineplot(selected_date, selected_id)


@callback(Output(IDS.POWER + IDS.DROPDOWN + "2", 'options'),
          Output(IDS.POWER + IDS.DROPDOWN + "2", 'value'),
          Input(IDS.POWER + IDS.TABLE + "1", 'rowData'))
def update_peak_dropdown_options(
    table_data: pd.DataFrame) -> tuple[list[dict[str, str]], str]:
  """Updates the dropdown options based on the table data.

  Args:
      table_data (pd.DataFrame): The table data.

  Returns:
      tuple[list[dict[str, str]], str]: The dropdown options and the default value."""
  dataf = pd.DataFrame(table_data)
  peak_dates = dataf[schema.HHSchema.DATETIME].unique().tolist()
  dropdown_options = [{"label": date, "value": date} for date in peak_dates]
  return dropdown_options, dropdown_options[0]['value']


@callback(Output(IDS.POWER + IDS.DROPDOWN + "1", 'value'),
          Input(IDS.POWER + IDS.DROPDOWN + "1", 'options'))
def update_peak_dropdown_value(available_options: list[dict[str, str]]) -> str:
  """Updates the dropdown value based on the available options.

  Args:
      available_options (list[dict[str, str]]): The available options.

  Returns:
      str: The dropdown value."""
  if available_options:
    return available_options[-1]['value']
  else:
    return None


@callback(
    Output(IDS.POWER + "clipboard" + "0", "content"),
    Input(IDS.POWER + "clipboard" + "0", "n_clicks"),
    State(IDS.POWER + IDS.TABLE + "0", "selectedRows"),
)
def selected_power_demand_info(
    n: int, table_data_selected: list[dict[str, str]]) -> str:
  """Returns the selected power demand information.
  
  Args:
      n (int): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected table data.

  Returns:
      str: The selected power demand information as a string."""
  if not table_data_selected:
    return "No selections"
  print(table_data_selected)
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()


@callback(
    Output(IDS.POWER + "clipboard" + "1", "content"),
    Input(IDS.POWER + "clipboard" + "1", "n_clicks"),
    State(IDS.POWER + IDS.TABLE + "1", "selectedRows"),
)
def selected_peak_power_points(
    n: int, table_data_selected: list[dict[str, str]]) -> str:
  """Returns the selected peak power points.

  Args:
      n (int): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected table data.
  
  Returns:
      str: The selected peak power points as a string."""
  if not table_data_selected:
    return "No selections"
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()
