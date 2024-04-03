import pandas as pd
from dash import Input, Output, Patch, State, callback, html  # type: ignore

from src.components import (filter_objects, gen_content_obj, line_fig,
                            summary_plot)
from src.data import loader
from src.tabs import general_tab
from src.utils import IDS, page_text, schema


def render() -> html.Div:
  """Renders the overview tab.

  Returns:
      html.Div: Div containing the layout for the overview tab."""
  target_col = 'All'
  utility = schema.PageSchema.ELEC
  tab_title = IDS.OVERVIEW

  df = loader.load_hh_data(resample=None, utility=utility)

  annual_consump_fig = line_fig.new_create_overview_lineplot(
      df, target_col=target_col)
  data_table = summary_plot.create_summary_table(
      loader.load_hh_data(resample='1MS', utility=utility),
      target_col=target_col,
      table_units=str(annual_consump_fig.layout.yaxis.title.text))
  fig = gen_content_obj.graph_obj(tab_title, annual_consump_fig)
  sankey = gen_content_obj.graph_obj(tab_title,
                                     summary_plot.overview_sankey(),
                                     id=1)
  monthly_table = gen_content_obj.table_obj(tab_title,
                                            data_table,
                                            page_fit=None,
                                            pinned_val=True)
  filt_objs_2 = [
      filter_objects.box_options([
          filter_objects.create_radioitem(
              tab_title, [schema.PageSchema.ELEC, schema.PageSchema.GAS])
      ]),
      filter_objects.box_options([
          filter_objects.create_dropdown(
              tab_title=tab_title,
              text=schema.PageSchema.METERID,
              dropdown_options=df.columns[:-1].tolist(),
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
      chart_table_1=sankey)
  section_3 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_2],
      section_number=2,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.SECOND_PLOT_TEXT],
      filter_obj=filt_objs_2,
      chart_table_1=fig)
  section_4 = general_tab.generate_page(
      section_title=page_text.tab_info(tab_title)[
          page_text.TabSchema.SUB_TITLE_3],
      section_number=3,
      section_text=page_text.tab_info(tab_title)[
          page_text.TabSchema.THIRD_PLOT_TEXT],
      chart_table_1=monthly_table)
  return html.Div([
      section_1.render_section(),
      section_2.render_section(),
      section_3.render_section(),
      section_4.render_section(),
  ])


@callback(
    Output(IDS.OVERVIEW + IDS.FIGURE + "0", 'figure'),
    Output(IDS.OVERVIEW + IDS.TABLE + "0", 'rowData'),
    Output(IDS.OVERVIEW + IDS.TABLE + "0", 'columnDefs'),
    Input(IDS.OVERVIEW + IDS.RADIOITEM, 'value'),
    Input(IDS.OVERVIEW + IDS.DROPDOWN + "2", 'value'),
)
def update_table_and_barplot(utility: str,
                             selected_dropdown_value: str) -> tuple:
  """Updates the figure and table based on the selected filters.

  Args:
      utility (str): The utility selected.
      selected_dropdown_value (str): The selected dropdown value.

  Returns:
      tuple: Tuple containing the figure, table and patched grid."""
  patched_grid = Patch()
  dataf = loader.load_hh_data(resample=None, utility=utility)

  # Use the selected_dropdown_value as the target_col
  fig = line_fig.new_create_overview_lineplot(
      dataf, target_col=selected_dropdown_value)
  plot_units: str = fig.layout.yaxis.title.text
  monthly_table = summary_plot.create_summary_table(
      df_monthly=loader.load_hh_data(resample='1MS', utility=utility),
      target_col=selected_dropdown_value,
      table_units=plot_units)
  patched_grid[0]['headerName'] = plot_units
  return fig, monthly_table.to_dict('records'), patched_grid


@callback(Output(IDS.OVERVIEW + IDS.DROPDOWN + "2", 'options'),
          Output(IDS.OVERVIEW + IDS.DROPDOWN + "2", 'value'),
          Input(IDS.OVERVIEW + IDS.RADIOITEM, 'value'))
def update_dropdown(energy_type: str) -> tuple[list[dict[str, str]], str]:
  """Updates the dropdown options based on the energy type selected.

  Args:
      energy_type (str): The selected energy type.

  Returns:
      tuple: Tuple containing the new options and the default value."""
  dataf = loader.load_hh_data(resample='1MS', utility=energy_type)
  meter_ids = dataf.columns.tolist()
  meter_ids.remove('month_of_year')
  new_options = [{
      'label': meter_id,
      'value': meter_id
  } for meter_id in meter_ids]
  value = new_options[-1]['value']
  return new_options, value


@callback(
    Output(IDS.OVERVIEW + "clipboard" + "0", "content"),
    Input(IDS.OVERVIEW + "clipboard" + "0", "n_clicks"),
    State(IDS.OVERVIEW + IDS.TABLE + "0", "selectedRows"),
)
def selected(n: bool, table_data_selected: list[dict[str, str]]) -> str:
  """Returns the selected rows from the table.

  Args:
      n (bool): The number of clicks.
      table_data_selected (list[dict[str, str]]): The selected rows from the table.

  Returns:
      str: The selected rows as a string."""
  if not table_data_selected:
    return "No selections"
  dff = pd.DataFrame(table_data_selected)
  return dff.to_string()
