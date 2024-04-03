from dataclasses import dataclass
from typing import Any, Optional

import dash_ag_grid as dag  # type: ignore
import pandas as pd  # type: ignore
import plotly.graph_objects as go  # type: ignore
from dash import dcc, html  # type: ignore

from src.utils import page_text, schema  # type: ignore


@dataclass
class generate_page:
  """Class for generating a uniform tab structure.
  
  Attributes:
      section_title (str): Title of the section.
      section_number (int): Number of the section.
      section_text (str): Text for the section.
      filter_obj (Optional[list[html.Div]]): List of filter objects for the section.
      chart_table_1 (Optional[html.Div]): First chart or table for the section.
      chart_table_2 (Optional[html.Div]): Second chart or table for the section.
      
  Methods:
      create_splitter: Creates a horizontal rule.
      format_title: Formats the title of the section.
      format_text: Formats the text of the section.
      format_filter_objs: Formats the filter objects for the section.
      format_first_display: Formats the first chart or table for the section.
      format_second_display: Formats the second chart or table for the section.
      render_section: Renders the section."""

  section_title: str
  section_number: int
  section_text: str
  filter_obj: Optional[list[html.Div]] = None
  chart_table_1: Optional[html.Div] = None
  chart_table_2: Optional[html.Div] = None

  def create_splitter(self) -> html.Hr:
    """Creates a horizontal line to split sections
    
    Returns:
        html.Hr: Horizontal line."""
    return html.Hr(style={'background-color': '#000', 'height': '4px'})

  def format_title(self) -> html.Div:
    """Formats the title of the section.

    Returns:
        html.Div: Div containing the title of the section."""
    return html.Div(self.section_title,
                    style={'text-align': schema.StructureSchema.TEXT_ALIGN})

  def format_text(self) -> html.Div:
    """Formats the text of the section.

    Returns:
        html.Div: Div containing the text of the section."""
    return html.Div(self.section_text,
                    style={'text-align': schema.StructureSchema.TEXT_ALIGN})

  def format_filter_objs(self) -> html.Div:
    """Formats the filter objects for the section.

    Returns:
        html.Div: Div containing the filter objects for the section."""
    return html.Div(self.filter_obj,
                    style={
                        'display': 'flex',
                        'text-align': schema.StructureSchema.ALIGN_CENTER
                    })

  def format_first_display(self) -> html.Div:
    """Formats the first chart or table for the section.

    Returns:
        html.Div: Div containing the first chart or table for the section."""
    return html.Div(self.chart_table_1,
                    style={'text-align': schema.StructureSchema.ALIGN_CENTER})

  def format_second_display(self) -> html.Div:
    """Formats the second chart or table for the section.

    Returns:
        html.Div: Div containing the second chart or table for the section."""
    return html.Div(self.chart_table_2,
                    style={'text-align': schema.StructureSchema.ALIGN_CENTER})

  def render_section(self) -> html.Div:
    """Renders the tab section.

    Returns:
        html.Div: Div containing the tab section."""

    splitter = self.create_splitter()
    title = self.format_title()
    text = self.format_text()
    filter_objs = self.format_filter_objs()
    first_display = self.format_first_display()
    second_display = self.format_second_display()
    return html.Div(
        [splitter, title, text, filter_objs, first_display, second_display])


def tab_info(tab_title: str) -> dict[str, Any]:
  """Returns the information for the tab.

  Args:
      tab_title (str): Title of the tab.

  Returns:
      dict[str, Any]: Dictionary containing the information for the tab."""
  return page_text.TAB_PAGE_DICT[tab_title]
