from typing import Any

from dash import html  # type: ignore

from src.utils import IDS

SITE_NAME = 'Example site'
SANKEY_DIAGRAM_YEAR = 2023


class TabSchema():
  TITLE = "Site energy and power dashboard"
  OVERVIEW = IDS.OVERVIEW
  POWER_DEMAND = IDS.POWER
  ENERGY_CONSUMPTION = IDS.ENERGY
  COST_ANALYSIS = IDS.COST
  SUBMETER_BREAKDOWN = "Submeter-breakdown"
  CARBON_EMISSIONS = 'Carbon-emissions'
  TAB_TITLE = 'tab_title'
  SUB_TITLE_1 = 'sub_title_1'
  SUB_TITLE_2 = 'sub_title_2'
  SUB_TITLE_3 = 'sub_title_3'
  OPENING_TEXT = 'opening_text'
  FIRST_PLOT_TEXT = 'first_plot_text'
  SECOND_PLOT_TEXT = 'second_plot_text'
  THIRD_PLOT_TEXT = 'third_plot_text'


TAB_PAGE_DICT = {
    TabSchema.OVERVIEW: {
        TabSchema.TAB_TITLE: [html.H1([TabSchema.OVERVIEW])],
        TabSchema.SUB_TITLE_1: [html.H2(f"{SITE_NAME}'s energy flows")],
        TabSchema.SUB_TITLE_2: [html.H2('Monthly energy consumption')],
        TabSchema.SUB_TITLE_3: [html.H2("")],
        TabSchema.OPENING_TEXT: [
            html.
            P(f"""This page provides an overview of the energy flows and energy consumption at {SITE_NAME}."""
              )
        ],
        TabSchema.FIRST_PLOT_TEXT: [
            html.P([
                f"""The Sankey diagram below shows {SITE_NAME}'s energy flows from the public grid connection points (i.e. electricity, gas, etc)\
          to the end-uses of the site (i.e. space heating, hot water demand, etc.) for the year {SANKEY_DIAGRAM_YEAR:.0f}. \
            Line width indicates energy amount, with colours representing \
          """,
                html.B('electricity'), """ (red), """,
                html.B("gas"), """ (yellow), and """,
                html.B("heating/cooling"), """ (green)."""
            ])
        ],
        TabSchema.SECOND_PLOT_TEXT: [
            html.P([
                """Your fiscal meters' historic monthly energy consumption was compiled from your invoices for month-to-month and year-to-year comparisons."""
            ])
        ],
        TabSchema.THIRD_PLOT_TEXT: [
            html.P([
                """This table presents annual energy consumption values, complementing the chart above. For each month, the table displays:""",
                html.Ul([
                    html.Li([
                        html.B('Current year:'),
                        """ This year's consumption."""
                    ]),
                    html.Li([
                        html.B('Previous year:'),
                        """ Last year's consumption."""
                    ]),
                    html.Li([
                        html.B('Median:'),
                        """ Median monthly value across all years."""
                    ]),
                    html.Li([
                        html.B('Min:'),
                        """ Lowest monthly value across all years."""
                    ]),
                    html.Li([
                        html.B('Max:'),
                        """ Highest monthly value across all years."""
                    ]),
                ])
            ])
        ]
    },
    TabSchema.POWER_DEMAND: {
        TabSchema.TAB_TITLE: [html.H1([TabSchema.POWER_DEMAND])],
        TabSchema.SUB_TITLE_1: [html.H2(["""Load duration curves"""])],
        TabSchema.SUB_TITLE_2: [html.H2(["""Peak demand periods"""])],
        TabSchema.SUB_TITLE_3: [],
        TabSchema.OPENING_TEXT: [
            html.P([
                """This page helps you understand your site's power demand in more details through load duration curves and peak demand periods."""
            ])
        ],
        TabSchema.FIRST_PLOT_TEXT: [
            html.
            P("""A Load Duration Curve (LDC) graphically displays power demand levels in descending order against the duration they occur. \
          It helps visualize peak-to-base loads over a specified period. Your agreed Maximum Available Capacity (MAC) is also shown in the graph (if available).\
          """),
            html.
            P("""If the site's power demand exceeds the MAC you could incur additional charges on your invoice, thus it is important to monitor this."""
              ),
        ],
        TabSchema.SECOND_PLOT_TEXT: [
            html.
            P("""The 10 instances where the peak demand of your meters are the highest are shown below."""
              ),
            html.
            P("""For the selected instance, the chart shows the three days prior and after the peak demand period. This could help understanding the potential causes of the peak demand."""
              ),
        ],
        TabSchema.THIRD_PLOT_TEXT: [
            html.P([
                "This table shows the details regarding the 10 peak demand periods including:",
                html.Ul([
                    html.Li([
                        html.B('Datetime:'),
                        " The time at which the peak demand occured."
                    ]),
                    html.Li([
                        html.B('Power demand [kw]:'),
                        " The power demand recorded at that time in kilowatts."
                    ]),
                    html.Li([
                        html.B('% of DNO limit:'),
                        " Comparison of the power demand recorded with the maximum import capacity of your meter/site."
                    ]),
                ])
            ])
        ]
    },
    TabSchema.ENERGY_CONSUMPTION: {
        TabSchema.TAB_TITLE:
        [html.H1(["""Out of hours energy consumption"""])],
        TabSchema.SUB_TITLE_1:
        [html.H3(["""Baseload during out of hours periods"""])],
        TabSchema.SUB_TITLE_2: [],
        TabSchema.SUB_TITLE_3: [],
        TabSchema.OPENING_TEXT: [
            html.
            P("""The out of hours energy consumption is analysed in this section. \
                  Out of hours energy consumption refers to the energy used by a facility or building outside its normal operating hours. \
                    This could include energy used for lighting, heating, ventilation, air conditioning (HVAC), office equipment, \
                      and other appliances when the facility is not in use or is operating at a reduced capacity."""
              ),
            html.
            P("""Energy used outside of operating hours may be unnecessary and wasteful.\
                    For example, lights or HVAC systems left on when a building is unoccupied can contribute to higher energy bills and greenhouse gas emissions than necessary."""
              )
        ],
        TabSchema.FIRST_PLOT_TEXT: [
            html.P([
                "The baseload during out of hours periods can be calculated for a specific meter or energy carrier with the following methods:",
                html.Ul([
                    html.Li([
                        html.B('Monthly:'),
                        " The baseload during out of hours periods is calculated for each month of the year."
                    ]),
                    html.Li([
                        html.B('Seasonal:'),
                        " The baseload during out of hours periods is calculated for each season of the year."
                    ]),
                    html.Li([
                        html.B('Annual:'),
                        " The baseload during out of hours periods is calculated for each year."
                    ]),
                ])
            ]),
            html.
            P("""For each method, the half-hourly energy data collected from your energy suppliers is used."""
              ),
        ],
        TabSchema.SECOND_PLOT_TEXT: [
            html.
            P("""The 10 instances where the out of hours energy consumption is the highest when compared to the expected energy consumption derived from the baseload for the method selected (Monthly, Seasonal, Annual)."""
              )
        ],
        TabSchema.THIRD_PLOT_TEXT: [
            html.P([
                "This table shows the details regarding the 10 highest out of hours energy demand periods including:",
                html.Ul([
                    html.Li([
                        html.B('Starting datetime:'),
                        " The starting date and time of the out of hours period."
                    ]),
                    # html.Li([
                    #     html.B('Ending datetime:'),
                    #     " The ending date and time of the out of hours period."
                    # ]),
                    html.Li([
                        html.B('Period consumption [kWh]:'),
                        " The energy consumption recorded during the out of hours period."
                    ]),
                    html.Li([
                        html.B('Expected period consumption [kWh]:'),
                        " The expected energy consumption during the out of hours period based on the baseload value."
                    ]),
                    html.Li([
                        html.B('% consumption above expected:'),
                        " Comparison of the energy consumption recorded with the expected energy consumption for the period."
                    ]),
                ])
            ])
        ]
    },
    TabSchema.COST_ANALYSIS: {
        TabSchema.TAB_TITLE: [html.H1([TabSchema.COST_ANALYSIS])],
        TabSchema.SUB_TITLE_1: [html.H2(["""Breakdown"""])],
        TabSchema.SUB_TITLE_2: [html.H2(["""Half-hourly price per unit"""])],
        TabSchema.SUB_TITLE_3: [html.H2(["""Charge rate timetable"""])],
        TabSchema.OPENING_TEXT: [
            html.P([
                """The information from your energy invoices was extracted to be analysed in order to better understand the variations in charges and identify any discrepancies. """
            ])
        ],
        TabSchema.FIRST_PLOT_TEXT: [
            html.P([
                "The charges of your invoices are broken down to visualise the weight of each charge type onto your overall invoice. For electricity, the charges include:",
                html.Ul([
                    html.Li([
                        html.B('Electricity/Gas charges:'),
                        " The cost of the electricity consumed - Day and Night charges."
                    ]),
                    html.Li([
                        html.B('Distribution Use of System (DUoS) charges:'),
                        " Red, Amber, and Green charges for the use of the distribution network."
                    ]),
                    html.Li([
                        html.B('Climate Change Levy (CCL):'),
                        " A tax on energy delivered to non-domestic users in the UK."
                    ]),
                    html.Li([
                        html.B('Fixed charges:'),
                        " Standing charge, Data collection, and Distribution charges."
                    ]),
                    html.Li([html.B('VAT:'), " Value Added Tax."]),
                ])
            ]),
            html.P([
                "For gas, the charges include:",
                html.Ul([
                    html.Li([
                        html.B('Electricity/Gas charges:'),
                        " The cost of the electricity/gas consumed - for electricity this includes Day and Night charges."
                    ]),
                    html.Li([
                        html.B('Climate Change Levy (CCL):'),
                        " A tax on energy delivered to non-domestic users in the UK."
                    ]),
                    html.Li([
                        html.B('Fixed charges:'),
                        " Standing charge, Data collection, and Distribution charges."
                    ]),
                    html.Li([html.B('VAT:'), " Value Added Tax."]),
                ])
            ])
        ],
        TabSchema.SECOND_PLOT_TEXT: [
            html.P([
                """The following plot shows how Rotherhams charge rates vary across the day. Rotherhams main meter has both """,
                html.B('Day/Night'), """ and """,
                html.B('DUoS'), """ \
           charges applied to it. These, along with your """,
                html.B('Climate Change Levy'),
                """ rate have been combined to give you an overall charge rate for \
           each half-hourly period."""
            ])
        ],
        TabSchema.THIRD_PLOT_TEXT: [
            html.P([
                """This table shows the annual energy consumption for the site compared to previous years. Each month in the table has five values, \
          """,
                html.B('Current year'),
                """ is the value from this calendar year, """,
                html.B('Previous year'),
                """ is the value from the previous calendar year, \
            """,
                html.B('Median'),
                """ is the median value for that month across all years as seen in the line plot above, """,
                html.B('Min'), """ is the lowest value \
              for that month across all years and """,
                html.B('Max'),
                """ is the highest value for that month across all years."""
            ])
        ]
    },
    TabSchema.SUBMETER_BREAKDOWN: {
        TabSchema.TAB_TITLE:
        'Submeter breakdown',
        TabSchema.SUB_TITLE_1:
        'Submeter overview',
        TabSchema.SUB_TITLE_2:
        'Overusage submeters',
        TabSchema.SUB_TITLE_3:
        'Overusage submeter table',
        TabSchema.OPENING_TEXT:
        'The submeter breakdown overview shows the submeter breakdown for the whole site.',
        TabSchema.FIRST_PLOT_TEXT:
        "Just imagine this section was overfilled with autogenerated information about the graph above. For example, it goes above the power demand limit which we could talk about and list how many times it breaches this value between the date range. Alternatively, if it doesn't breach the limit we could say the site comes within 10% of the limit which is very close!!!",
        TabSchema.SECOND_PLOT_TEXT:
        "In this section you'll find a dropdown that will allow you to view the top 10 highest peaking periods in the range set above. The table beneath will also show how close these times got to ",
        TabSchema.THIRD_PLOT_TEXT:
        "This table shows the annual energy consumption for the site compared to previous years. Each month in the table has five values, **Current year** is the value from this calendar year, **Previous year** is the value from the previous calendar year, **Median** is the median value for that month across all years as seen in the line plot above, **Min** is the lowest value for that month across all years and **Max** is the highest value for that month across all years."
    },
    TabSchema.CARBON_EMISSIONS: {
        TabSchema.TAB_TITLE:
        'Carbon emissions',
        TabSchema.SUB_TITLE_1:
        'Site carbon emission overview',
        TabSchema.SUB_TITLE_2:
        'Carbon emission across the day',
        TabSchema.SUB_TITLE_3:
        'Carbon emissions table',
        TabSchema.OPENING_TEXT:
        'The carbon emissions overview shows the carbon emissions for the whole site.',
        TabSchema.FIRST_PLOT_TEXT:
        "Just imagine this section was overfilled with autogenerated information about the graph above. For example, it goes above the power demand limit which we could talk about and list how many times it breaches this value between the date range. Alternatively, if it doesn't breach the limit we could say the site comes within 10% of the limit which is very close!!!",
        TabSchema.SECOND_PLOT_TEXT:
        "In this section you'll find a dropdown that will allow you to view the top 10 highest peaking periods in the range set above. The table beneath will also show how close these times got to ",
        TabSchema.THIRD_PLOT_TEXT:
        "This table shows the annual energy consumption for the site compared to previous years. Each month in the table has five values, **Current year** is the value from this calendar year, **Previous year** is the value from the previous calendar year, **Median** is the median value for that month across all years as seen in the line plot above, **Min** is the lowest value for that month across all years and **Max** is the highest value for that month across all years."
    },
}


def tab_info(tab_title: str) -> dict[str, Any]:
  return TAB_PAGE_DICT[tab_title]
