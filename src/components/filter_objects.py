from typing import Any, Optional

from dash import dcc, html  # type: ignore

from src.utils import IDS, schema


def create_dropdown(tab_title: str, text: str, dropdown_options: list[Any],
                    section_no: int) -> html.Div:
  """ Creates a html.Div with a dropdown component and a title to describe the dropdown. 
  
  Args:
      tab_title (str): Title of the tab the dropdown will be used in.
      text (str): Title of the dropdown.
      dropdown_options (list[Any]): List of options for the dropdown.
      section_no (int): Section number of the dropdown.
      
  Returns:
      html.Div: Div containing the dropdown and title."""
  return html.Div(
      [
          html.Div(text),
          dcc.Dropdown(
              id=tab_title + IDS.DROPDOWN + str(section_no),
              # className='date-dropdown',
              options=[{
                  "label": option,
                  "value": option
              } for option in dropdown_options],
              value=dropdown_options[-1])
      ],
      style={'text-align': schema.StructureSchema.TEXT_ALIGN})


def create_sliders(tab_title: str, options: list[float],
                   static: bool) -> html.Div:
  """ Creates a html.Div with a slider component and a title to describe the slider. 
  
  Args:
      tab_title (str): Title of the tab the slider will be used in.
      options (list[float]): List of options for the slider.
      static (bool): Whether the slider is static or not.
      
  Returns:
      html.Div: Div containing the slider and title."""
  if static:
    return html.Div([
        html.Div(schema.PageSchema.YEAR,
                 style={'text-align': schema.StructureSchema.TEXT_ALIGN}),
        dcc.Slider(
            id=tab_title + IDS.RANGESLIDER,
            min=options.min(),
            max=options.max(),
            value=options.max(),
            step=1,
            marks={
                val: str(val)
                for val in range(options.min(),
                                 options.max() + 1)
            },
        ),
    ])
  else:
    return html.Div([
        html.Div(schema.PageSchema.RANGE,
                 style={'text-align': schema.StructureSchema.TEXT_ALIGN}),
        dcc.RangeSlider(
            id=tab_title + IDS.RANGESLIDER,
            min=options.min(),
            max=options.max(),
            step=1,
            marks={
                val: str(val)
                for val in range(options.min(),
                                 options.max() + 1)
            },
        ),
    ], )


def create_radioitem(tab_title: str,
                     options: list[str],
                     item_title: Optional[str] = None,
                     id_int: Optional[int] = None) -> html.Div:
  """ Creates a html.Div with a radioitem component and a title to describe the radioitem. 
  
  Args:
      tab_title (str): Title of the tab the radioitem will be used in.
      options (list[str]): List of options for the radioitem.
      item_title (Optional[str], optional): Title of the radioitem. Defaults to None.
      id_int (Optional[int], optional): ID of the radioitem. Defaults to None.
      
  Returns:
      html.Div: Div containing the radioitem and title.
  """
  if not item_title:
    item_title = schema.PageSchema.ECARRIER
  if not id_int:
    int_val = ''
  else:
    int_val = id_int
  return html.Div([
      html.Div(item_title,
               style={'text-align': schema.StructureSchema.TEXT_ALIGN}),
      dcc.RadioItems(options,
                     id=tab_title + IDS.RADIOITEM + str(int_val),
                     value=options[0],
                     inline=True),
  ])


def box_options(lst_objects: list[html.Div],
                padding: str = '10px',
                width: str = '49%') -> html.Div:
  """ Returns a html.Div with a border and padding to contain the list of dropdown objects passed to it. 
  
  Args:
      lst_objects (list[html.Div]): List of dropdown objects to be contained in the box.
      padding (str, optional): Padding for the box. Defaults to '10px'.
      width (str, optional): Width of the box. Defaults to '49%'.
      
  Returns:
      html.Div: Div containing the list of dropdown objects."""
  return html.Div(lst_objects,
                  style={
                      'border': '1px solid #000',
                      'padding': padding,
                      'text-align': 'center',
                      'width': width
                  })
