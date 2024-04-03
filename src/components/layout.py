from dash import Dash, dcc, html  # type: ignore


def create_layout(app: Dash) -> html.Div:
  """Create the layout for the app.
  
  Args:
      app (Dash): Dash app object.
      
  Returns:
      html.Div: Div containing the layout for the app.
  """
  return html.Div(
      [
          html.Div(
              id='logo-container',
              children=[
                  html.Img(src=app.get_asset_url("e2s_logo.png"),
                           style={"height": "60px"
                                  }),  # Adjust the image path and height
                  html.Div(
                      id='auth-buttons',
                      style={'text-align': 'right'},
                      children=[
                          html.Div(
                              [
                                  dcc.Link(
                                      'Login', href='/login'
                                  ),  # Placeholder for the login button
                              ],
                              style={"margin-right": "80px"
                                     }),  # Adjust the margin as needed
                          html.Div([
                              dcc.Link('Logout', href='/logout'
                                       )  # Placeholder for the logout button
                          ]),
                      ]),
              ]),
          dcc.Tabs(
              id='tabs-example',
              value='tab-0',
              children=[
                  dcc.Tab(label='Site Overview', value='tab-0'),
                  dcc.Tab(label='Electrical power demand', value='tab-1'),
                  dcc.Tab(label='Consumption performance', value='tab-2'),
                  dcc.Tab(label='Cost analysis', value='tab-3'),
              ],
          ),
          html.Div(id='tabs-content')
      ], )
