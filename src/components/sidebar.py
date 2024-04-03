import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dash_table, dcc, html
from dash.dependencies import Component

from src.utils import IDS

# from dash_app import app
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


def get_sidebar(app: Dash) -> Component:
  """Create the sidebar for the app.

  Args:
      app (Dash): Dash app object.

  Returns:
      Component: Sidebar for the app.
  """
  sidebar = html.Div(
      [
          html.Img(src=app.get_asset_url('e2s_logo.png'), height="120px"),
          html.Hr(),
          dbc.Nav(
              id='sidebar-nav',
              children=[
                  dbc.NavLink(IDS.OVERVIEW,
                              href="/energy-system-overview",
                              active="exact"),
                  dbc.NavLink(
                      IDS.POWER, href="/power-demand-usage", active="exact"),
                  dbc.NavLink(IDS.ENERGY,
                              href="/out-of-hours-energy-consumption",
                              active="exact"),
                  dbc.NavLink(
                      IDS.COST, href="/invoice-cost-analysis", active="exact"),
                  # dbc.NavLink("Submeter-breakdown", href="/submeter", active="exact"),
                  # dbc.NavLink("Carbon-emissions", href="/carbon", active="exact"),
              ],
              vertical=True,
              pills=True,
          ),
      ],
      style=SIDEBAR_STYLE,
  )
  return sidebar
