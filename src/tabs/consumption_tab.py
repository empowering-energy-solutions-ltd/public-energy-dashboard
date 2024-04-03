from datetime import datetime
from typing import Any

import pandas as pd
from dash import Input, Output, State, callback, html  # type: ignore

from src.components import consumption_plots, filter_objects, gen_content_obj
from src.data import loader
from src.tabs import general_tab
from src.utils import IDS, page_text, schema


def render() -> html.Div:
  """Renders the consumption tab.
  
  Returns:
      html.Div: Div containing the layout for the consumption tab."""
  tab_title = IDS.ENERGY
  initial_meter = f'{IDS.ELEC_MPR_3}'
  dataf = loader.load_hh_data(resample=None)
  dataf = dataf.drop(['All'], axis=1)
  options = dataf.columns.tolist()
  options.remove(schema.HHSchema.MONTH_OF_YEAR)
  data = consumption_plots.new_consump_periods(dataf, initial_meter)
  lower_table = gen_content_obj.table_obj(tab_title, data)
  fig = gen_content_obj.graph_obj(
      tab_title, consumption_plots.new_baseline_barplot(dataf, initial_meter))

  baselines = schema.BASELINES
  peak_dates: list[datetime] = data.index.unique().date.tolist()
  years: list[int] = dataf.index.year.unique()
  fig_2 = consumption_plots.create_consumption_lineplot(
      dataf,
      initial_meter,
      selected_baseline=baselines[2],
      selected_date=peak_dates[0])
  lower_line = gen_content_obj.graph_obj(tab_title, fig_2, 1)

  filt_objs = [
      filter_objects.box_options([
          filter_objects.create_sliders(tab_title, years, False),
          filter_objects.create_dropdown(
              tab_title=tab_title,
              text=schema.PageSchema.SELECT_BASELOAD,
              dropdown_options=baselines,
              section_no=0)
      ]),
      filter_objects.box_options([
          filter_objects.create_radioitem(
              tab_title,
              options=[schema.PageSchema.ELEC, schema.PageSchema.GAS]),
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
      chart_table_1=fig)
  section_3 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_2],
      section_number=2,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.SECOND_PLOT_TEXT],
      filter_obj=filt_objs_2,
      chart_table_1=lower_line)
  section_4 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_3],
      section_number=3,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.THIRD_PLOT_TEXT],
      chart_table_1=lower_table)
  return html.Div([
      section_1.render_section(),
      section_2.render_section(),
      section_3.render_section(),
      section_4.render_section(),
  ])


@callback(Output(IDS.ENERGY + IDS.TABLE + "0", 'rowData'),
          Output(IDS.ENERGY + IDS.FIGURE + "0", 'figure'),
          Input(IDS.ENERGY + IDS.RANGESLIDER, 'value'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "1", 'value'),
          Input(IDS.ENERGY + IDS.RADIOITEM, 'value'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "0", 'value'))
def update_table_and_barplot(
    selected_years: list[int], target_col: str, utility: str,
    baseline_type: str) -> tuple[list[dict[str, Any]], Any]:
  """Updates the table and bar plot based on the selected years, meter and baseline type.
  
  Args:
      selected_years (list[int]): The selected years.
      target_col (str): The selected meter.
      utility (str): The selected utility.
      baseline_type (str): The selected baseline type.
      
  Returns:
      tuple[list[dict[str, Any]], Any]: The table data and the bar plot."""
  dataf = loader.load_hh_data(resample=None, utility=utility)
  dataf = dataf.drop(['All'], axis=1)
  if not selected_years:
    selected_years = [dataf.index.year.min(), dataf.index.year.max()]
  year_range = range(selected_years[0], selected_years[-1] + 1)
  filtered_data = dataf[dataf.index.year.isin(year_range)]
  table_data = consumption_plots.new_consump_periods(
      filtered_data, target_col=target_col,
      baseline_type=baseline_type).to_dict('records')
  fig = consumption_plots.new_baseline_barplot(filtered_data,
                                               target_col=target_col,
                                               baseline=baseline_type)

  return table_data, fig


@callback(Output(IDS.ENERGY + IDS.DROPDOWN + "1", 'options'),
          Output(IDS.ENERGY + IDS.DROPDOWN + "1", 'value'),
          Input(IDS.ENERGY + IDS.RADIOITEM, 'value'))
def update_dropdown(energy_type: str) -> tuple[list[dict[str, str]], str]:
  """Updates the dropdown options based on the energy type selected.
  
  Args:
      energy_type (str): The selected energy type.
  
  Returns:
      tuple[list[dict[str, str]], str]: The dropdown options and the default value."""
  dataf = loader.load_hh_data(resample='1MS', utility=energy_type)
  dataf = dataf.drop(['All'], axis=1)
  meter_ids = dataf.columns.tolist()
  meter_ids.remove('month_of_year')
  new_options = [{
      'label': meter_id,
      'value': meter_id
  } for meter_id in meter_ids]
  value = new_options[-1]['value']
  return new_options, value


@callback(Output(IDS.ENERGY + IDS.FIGURE + "1", 'figure'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "2", 'value'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "0", 'value'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "1", 'value'))
def update_consump_lineplot(selected_date: datetime, selected_baseline: str,
                            selected_meter_id: str) -> Any:
  """Updates the consumption line plot based on the selected date, baseline and meter.

  Args:
      selected_date (datetime): The selected date.
      selected_baseline (str): The selected baseline.
      selected_meter_id (str): The selected meter.

  Returns:
      Any: The consumption line plot."""
  data = loader.load_hh_data(resample=None)
  data = data.drop(['All'], axis=1)
  return consumption_plots.create_consumption_lineplot(
      data,
      selected_meter_id,
      selected_baseline=selected_baseline,
      selected_date=selected_date)
  # return fig


@callback(Output(IDS.ENERGY + IDS.DROPDOWN + "2", 'options'),
          Input(IDS.ENERGY + IDS.TABLE + "0", 'rowData'))
def update_peak_dropdown_options(
    table_data: list[dict[str, Any]]) -> list[dict[str, str]]:
  """Updates the peak dropdown options based on the table data.

  Args:
      table_data (list[dict[str, Any]]): The table data.

  Returns:
      list[dict[str, str]]: The peak dropdown options."""
  dataf = pd.DataFrame(table_data)
  peak_dates = pd.to_datetime(
      dataf['Start Datetime']).dt.date.unique().tolist()
  dropdown_options = [{"label": date, "value": date} for date in peak_dates]
  return dropdown_options


@callback(Output(IDS.ENERGY + IDS.DROPDOWN + "2", 'value'),
          Input(IDS.ENERGY + IDS.DROPDOWN + "2", 'options'))
def update_peak_dropdown_value(available_options: list[dict[str, str]]):
  if available_options:
    return available_options[0]['value']
  else:
    return None


@callback(
    Output(IDS.ENERGY + "clipboard" + "0", "content"),
    Input(IDS.ENERGY + "clipboard" + "0", "n_clicks"),
    State(IDS.ENERGY + IDS.TABLE + "0", "selectedRows"),
)
def selected_ooo_consumption_points(
    n: bool, table_data_selected: list[dict[str, str]]) -> str:
  """Returns the selected table data as a string.

  Args:
      n (bool): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected table data.

  Returns:
      str: The selected table data as a string."""
  if not table_data_selected:
    return "No selections"
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()
