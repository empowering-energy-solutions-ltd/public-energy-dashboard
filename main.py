import dash_auth  # type: ignore
from dash import Dash, Input, Output, callback, dcc, html  # type: ignore
from dash_bootstrap_components.themes import LUX  # type: ignore
from flask import Flask

from src.components.sidebar import get_sidebar
from src.tabs import consumption_tab, cost_tab, overview_tab, power_tab
from src.utils import IDS, page_text

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
VALID_USERNAME_PASSWORD_PAIRS = {'User': 'Password'}  # username:password


def create_layout(app: Dash) -> html.Div:

  @callback(Output(IDS.PAGE_CONTENT, 'children'), [Input(IDS.URL, 'pathname')])
  def display_page(pathname: str):
    """Render the content of the tabs"""
    if pathname == '/power-demand-usage':
      return power_tab.render()
    if pathname == '/out-of-hours-energy-consumption':
      return consumption_tab.render()
    if pathname == '/invoice-cost-analysis':
      return cost_tab.render()
    else:
      return overview_tab.render()

  return html.Div([
      dcc.Location(id=IDS.URL, refresh='callback-nav'),
      get_sidebar(app),
      html.Div(id=IDS.PAGE_CONTENT, style=CONTENT_STYLE, children=[]),
  ])


def create_app():
  server = Flask(__name__)
  app = Dash(external_stylesheets=[LUX],
             suppress_callback_exceptions=True,
             server=server)
  dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
  app.title = page_text.TabSchema.TITLE
  app.layout = create_layout(app)
  return app


def main():
  app = create_app()

  # port = int(os.environ.get("PORT", 5000)) # For Heroku deployment
  # app.run(host="0.0.0.0", port=port) # For Heroku deployment

  app.run(port="8070")  # For local development


if __name__ == "__main__":
  main()
