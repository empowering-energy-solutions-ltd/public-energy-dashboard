MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

SEASONS = ['Winter', 'Spring', 'Summer', 'Autumn']

PLOT_MARKERS = [
    'circle', 'square', 'diamond', 'cross', 'x', 'star', 'triangle-up',
    'triangle-down', 'pentagon', 'hexagon'
]

BASELINES = ['Annual', 'Seasonal', 'Monthly']

SM3_TO_KWH = 10.795


class ColourSchema():
  RED_BLOCK = "rgba(216, 205, 0, 1)"
  YELLOW_BLOCK = "rgba(219, 39, 13, 1)"
  GREEN_BLOCK = "rgba(0,158,115, 1)"
  RED_FADED = "rgba(216, 205, 0, 0.75)"
  YELLOW_FADED = "rgba(219, 39, 13, 0.75)"
  GREEN_FADED = "rgba(0,158,115, 0.75)"
  GREY = "rgba(0, 0, 0, 0.1)"


class SankeyOneSchema():
  label_list = [
      "Grid Elec", "Grid Gas", "Fiscal Elec", "Fiscal Gas", "E storage",
      "E chillers", "HVAC system", "CHP", "Gas boilers", "Steam boiler",
      "Gas demand", "Elec demand", "Heat/cooling demand", "Hot water demand",
      "Steam demand", "Absorption chillers"
  ]
  block_colour_list = [
      ColourSchema.RED_BLOCK, ColourSchema.YELLOW_BLOCK,
      ColourSchema.RED_BLOCK, ColourSchema.YELLOW_BLOCK,
      ColourSchema.RED_BLOCK, ColourSchema.RED_BLOCK, ColourSchema.RED_BLOCK,
      ColourSchema.YELLOW_BLOCK, ColourSchema.YELLOW_BLOCK,
      ColourSchema.YELLOW_BLOCK, ColourSchema.YELLOW_BLOCK,
      ColourSchema.RED_BLOCK, ColourSchema.GREEN_BLOCK,
      ColourSchema.GREEN_BLOCK, ColourSchema.GREEN_BLOCK,
      ColourSchema.RED_BLOCK
  ]
  flow_colour_list = [
      ColourSchema.YELLOW_FADED, ColourSchema.RED_FADED,
      ColourSchema.YELLOW_FADED, ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED, ColourSchema.YELLOW_FADED,
      ColourSchema.RED_FADED, ColourSchema.RED_FADED, ColourSchema.RED_FADED,
      ColourSchema.RED_FADED, ColourSchema.YELLOW_FADED,
      ColourSchema.GREEN_FADED, ColourSchema.YELLOW_FADED,
      ColourSchema.GREEN_FADED, ColourSchema.RED_FADED, ColourSchema.RED_FADED,
      ColourSchema.GREEN_FADED, ColourSchema.RED_FADED,
      ColourSchema.GREEN_FADED
  ]
  source_list = [0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 7, 7, 7, 7, 8, 8, 9, 5, 6]
  target_list = [
      2, 3, 4, 5, 6, 11, 7, 8, 9, 10, 4, 15, 11, 12, 12, 13, 14, 12, 12
  ]
  value_list = [
      13011, 39689, 1000, 1600, 9000, 1411, 23259, 10213, 3285, 2932, 1000,
      2148.2, 8115, 6936.4, 4172, 4000, 2000, 1070, 7500
  ]


class SankeyTwoSchema():
  label_list = [
      "Grid Elec",  # 0
      "Grid Gas",  # 1
      "Fiscal Elec",  # 2
      "Fiscal Gas",  # 3
      "Gas Central Heating",  # 4
      "Gas boiler",  # 5
      "Gas demand",  # 6
      "Elec demand",  # 7
      "Heat/Hot water demand",  # 8
      "Flat 1",  # 9
      "Flat 2",  # 10
      "Flat 3",  # 11
      "Flat 4",  # 12
      "Additional Flats",  # 13
      "Communal areas",  # 14
  ]
  block_colour_list = [
      ColourSchema.YELLOW_BLOCK,  # 0
      ColourSchema.RED_BLOCK,  # 1
      ColourSchema.YELLOW_BLOCK,  # 2
      ColourSchema.RED_BLOCK,  # 3
      ColourSchema.RED_BLOCK,  # 4
      ColourSchema.RED_BLOCK,  # 5
      ColourSchema.RED_BLOCK,  # 6
      ColourSchema.YELLOW_BLOCK,  # 7
      ColourSchema.GREEN_BLOCK,  # 8
  ]
  flow_colour_list = [
      ColourSchema.YELLOW_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.YELLOW_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.RED_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
      ColourSchema.GREEN_FADED,
  ]
  source_list = [
      0, 1, 2, 7, 7, 7, 7, 7, 7, 3, 3, 3, 4, 5, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8,
      8, 8
  ]
  target_list = [
      2, 3, 7, 9, 10, 11, 12, 13, 14, 4, 5, 6, 8, 8, 9, 10, 11, 12, 13, 14, 9,
      10, 11, 12, 13, 14
  ]
  value_list = [
      6, 12, 6, 1, 1, 1, 1, 1, 1, 3, 3, 6, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
      1, 1
  ]


class InvoiceSchema():
  MPR = 'mpr'
  MPR_2 = 'MPR'
  MPAN_MPR = 'MPAN/MPR'
  READDATE = 'ReadDate'
  TIME = 'Time'
  CHARGE = '- Charge [GBP]'
  CONSUMPTION = '- Consumption [kWh]'
  RATE_PER_KWH = '- Rate [GBP/kWh]'
  RATE_PER_DAY = '- Rate [GBP/day]'
  AMBER = 'Amber '
  GREEN = 'Green '
  RED = 'Red '
  DAY = 'Day '
  NIGHT = 'Night '
  STANDING = 'Standing '
  CARBON = 'Carbon '
  VAT = 'VAT '
  SITE = 'Site '
  AVAILABILITY = 'Availability '
  DISTRIB = 'Distrib fixed '
  DATA = 'Data collection '
  SETTLEMENT = 'Settlement '
  NETWORK = 'Network '
  REACTIVE = 'Reactive '
  RECONCILIATION = 'Reconciliation '
  FIXED_CHARGES = 'Fixed '
  NET = 'net_charge'
  UNNAMED = 'Unnamed: 0'
  ACCOUNT = 'account_no'
  TOTAL_GAS = 'total_gas_sales'
  CONSUMPTION_KWH = 'consumption_kWh'
  PERIOD_FROM = 'period_from'
  PERIOD_TO = 'period_to'


class PageSchema():
  GAS = 'Gas'
  ELEC = 'Electricity'
  HEAT = 'Heat/Cooling'
  RANGE = 'Select year range.'
  YEAR = 'Select year.'
  ECARRIER = 'Select energy carrier.'
  METERID = 'Select meter ID.'
  DATES = 'Select peak date.'
  ENERGY = 'Energy consumption [kWh]'
  POWER = 'Power demand [kW]'
  PERC_LIM = 'perc_of_limit'
  PERCENT_LIM = '% of DNO limit'

  START_DATE = 'Start Datetime'
  END_DATE = 'End Datetime'
  PERIOD_CONSUMP = 'Period consumption [kWh]'
  EXP_CONSUMP = 'Expected period consumption [kWh]'
  PERC_BASELINE = '% consumption above expected'

  SELECT_BASELOAD = 'Select baseload method.'
  MAX_CAP = 'Maximum Available Capacity'


class PlotSchema():
  PERC_BILL = 'Percentage of bill (%)'
  MONTH = 'Month '
  INV_SPEND = 'Invoice spend breakdown'
  MONTH_YEAR = 'Month of year'
  PEAK_POWER = 'Instance of peak power demand'
  HIGH_CONSUMPTION = 'High out of hours consumption period'
  MAX_CAP = 'Maximum Available Capacity'
  E_MWH = 'Energy (MWh)'
  PERIOD_CONSUMP = 'Period consumption [kWh]'
  POTENT_CONSUMP = 'Potential peak consumption [kWh]'


class SummarySchema():
  ALL = 'All years'
  CURRENT = 'Current year'
  PREV = 'Previous year'
  MEDIAN = 'Median'
  MIN = 'Min'
  MAX = 'Max'
  NO_DATA = 'No data'


class HHSchema():
  ENERGY_CONSUMPTION = 'energy_consumption'
  POWER_DEMAND = 'power_demand'
  TIME_OF_DAY = 'time_of_day'
  DAY_OF_MONTH = 'day_of_month'
  MONTH_OF_YEAR = 'month_of_year'
  SEASON_OF_YEAR = 'season_of_year'
  YEAR = 'year'
  DATETIME = 'Datetime'
  START_DATE = 'start_date'
  END_DATE = 'end_date'
  WORK_HOURS = 'work_hours'


class PowerTableSchema():
  COL = 'Column'
  MIN_POWER = 'Minimum Power [kW]'
  QUART_POWER = '25% of Power demand [kW]'
  MEDIAN_POWER = 'Median Power [kW]'
  TOP_QUART_POWER = '75% of Power demand [kW]'
  PEAK_POWER = 'Peak Power demand [kW]'
  PERC_OF_LIM = 'DNO Connection Limit [kW]'
  PERC_HALF_HOUR = 'perc_half_hours'
  PERC_HALF_HOUR_TITLE = 'Percentage of half-hours (%)'
  LOAD_DUR = 'Load Duration Curve'


class StructureSchema():
  TEXT_ALIGN = 'left'
  ALIGN_CENTER = 'center'
