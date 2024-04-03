from e2sviz.data import standard_data_process as sdp
from e2sviz.structure import enums, viz_schema

from src.utils.schema import HHSchema as HS
from src.utils.schema import InvoiceSchema as IS
"""
Here we define the metadata for the different data sources for use with e2sviz. 
I recommend if you plan on adding to this dashboard that you do not use e2sviz, its functionality
is too riggid and its use is not beneficial in most cases. On the other hand, if you have some
data preprocessing to do, you could use the e2sviz dataprep module.
"""

HH_METADATA = {
    HS.ENERGY_CONSUMPTION: {
        viz_schema.MetaDataSchema.NAME: HS.ENERGY_CONSUMPTION,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.WH,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.KILO,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Energy Consumption']
    },
    HS.POWER_DEMAND: {
        viz_schema.MetaDataSchema.NAME: HS.POWER_DEMAND,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.W,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.KILO,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Power Demand']
    },
    HS.TIME_OF_DAY: {
        viz_schema.MetaDataSchema.NAME: HS.TIME_OF_DAY,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.NAN,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.BASE,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Time of Day']
    },
    HS.DAY_OF_MONTH: {
        viz_schema.MetaDataSchema.NAME: HS.DAY_OF_MONTH,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.NAN,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.BASE,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Day of Month']
    },
    HS.MONTH_OF_YEAR: {
        viz_schema.MetaDataSchema.NAME: HS.MONTH_OF_YEAR,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.NAN,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.BASE,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Month of Year']
    },
    HS.YEAR: {
        viz_schema.MetaDataSchema.NAME: HS.YEAR,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.NAN,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.BASE,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.FLOAT,
        viz_schema.MetaDataSchema.LEGEND: ['Month of Year']
    },
    HS.DATETIME: {
        viz_schema.MetaDataSchema.NAME: HS.DATETIME,
        viz_schema.MetaDataSchema.UNITS: enums.UnitsSchema.NAN,
        viz_schema.MetaDataSchema.PREFIX: enums.Prefix.BASE,
        viz_schema.MetaDataSchema.TYPE: enums.DataType.NONE,
        viz_schema.MetaDataSchema.LEGEND: ['Datetime']
    },
    viz_schema.MetaDataSchema.FRAME: {
        viz_schema.MetaDataSchema.FREQ: viz_schema.FrequencySchema.HH,
        viz_schema.MetaDataSchema.GB_AGG: None,
        viz_schema.MetaDataSchema.INDEX_COLS:
        [viz_schema.FrequencySchema.DATETIME],
        viz_schema.MetaDataSchema.GROUPED_COLS: []
    }
}

PRICE_METADATA = {
    IS.AMBER + IS.CHARGE: {
        'Name': IS.AMBER + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.AMBER + IS.CHARGE
    },
    IS.GREEN + IS.CHARGE: {
        'Name': IS.GREEN + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.GREEN + IS.CHARGE
    },
    IS.RED + IS.CHARGE: {
        'Name': IS.RED + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.RED + IS.CHARGE
    },
    IS.DAY + IS.CHARGE: {
        'Name': IS.DAY + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.DAY + IS.CHARGE
    },
    IS.NIGHT + IS.CHARGE: {
        'Name': IS.NIGHT + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.NIGHT + IS.CHARGE
    },
    IS.STANDING + IS.CHARGE: {
        'Name': IS.STANDING + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.STANDING + IS.CHARGE
    },
    IS.CARBON + IS.CHARGE: {
        'Name': IS.CARBON + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.CARBON + IS.CHARGE
    },
    IS.RECONCILIATION + IS.CHARGE: {
        'Name': IS.RECONCILIATION + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.RECONCILIATION + IS.CHARGE
    },
    IS.VAT + IS.CHARGE: {
        'Name': IS.VAT + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.VAT + IS.CHARGE
    },
    IS.FIXED_CHARGES + IS.CHARGE: {
        'Name': IS.FIXED_CHARGES + IS.CHARGE,
        'Units': enums.UnitsSchema.GBP,
        'Prefix': enums.Prefix.BASE,
        'Type': enums.DataType.FLOAT,
        'Legend': IS.FIXED_CHARGES + IS.CHARGE
    },
    viz_schema.MetaDataSchema.FRAME: {
        viz_schema.MetaDataSchema.FREQ: viz_schema.FrequencySchema.MONTH,
        viz_schema.MetaDataSchema.GB_AGG: None,
        viz_schema.MetaDataSchema.INDEX_COLS:
        [viz_schema.FrequencySchema.DATETIME],
        viz_schema.MetaDataSchema.GROUPED_COLS: []
    }
}

DUOS_METADATA = {
    'Charge rate [GBP/kWh]': {
        'Name': 'Charge rate [GBP/kWh]',
        'Units': enums.UnitsSchema.GBP_PER_E,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Charge rate [GBP/kWh]']
    },
    viz_schema.MetaDataSchema.FRAME: {
        viz_schema.MetaDataSchema.FREQ: viz_schema.FrequencySchema.HH,
        viz_schema.MetaDataSchema.GB_AGG: None,
        viz_schema.MetaDataSchema.INDEX_COLS:
        [viz_schema.FrequencySchema.DATETIME],
        viz_schema.MetaDataSchema.GROUPED_COLS: []
    }
}

FLAT_METADATA = {
    'Flat 1': {
        'Name': 'Flat 1',
        'Units': enums.UnitsSchema.WH,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Flat 1']
    },
    'Flat 2': {
        'Name': 'Flat 2',
        'Units': enums.UnitsSchema.WH,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Flat 2']
    },
    'Flat 3': {
        'Name': 'Flat 3',
        'Units': enums.UnitsSchema.WH,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Flat 3']
    },
    'Flat 4': {
        'Name': 'Flat 4',
        'Units': enums.UnitsSchema.WH,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Flat 4']
    },
    'Median Flat': {
        'Name': 'Median Flat',
        'Units': enums.UnitsSchema.WH,
        'Prefix': enums.Prefix.KILO,
        'Type': enums.DataType.FLOAT,
        'Legend': ['Median Flat']
    },
    viz_schema.MetaDataSchema.FRAME: {
        viz_schema.MetaDataSchema.FREQ: viz_schema.FrequencySchema.HH,
        viz_schema.MetaDataSchema.GB_AGG: None,
        viz_schema.MetaDataSchema.INDEX_COLS:
        [viz_schema.FrequencySchema.DATETIME],
        viz_schema.MetaDataSchema.GROUPED_COLS: []
    }
}


def generate_consump_metadata() -> sdp.MetaData:
  """ Generate the metadata for the consumption data.
  
  Returns:
      sdp.MetaData: The metadata for the consumption data.
  """
  return sdp.MetaData(HH_METADATA)


def generate_price_metadata() -> sdp.MetaData:
  """ Generate the metadata for the price data.

  Returns:
      sdp.MetaData: The metadata for the price data.
  """
  return sdp.MetaData(PRICE_METADATA)


def generate_duos_metadata() -> sdp.MetaData:
  """ Generate the metadata for the DUOS data.

  Returns:
      sdp.MetaData: The metadata for the DUOS data.
  """
  return sdp.MetaData(DUOS_METADATA)


def generate_flat_metadata() -> sdp.MetaData:
  """ Generate the metadata for the flat data.

  Returns:
      sdp.MetaData: The metadata for the flat data.
  """
  return sdp.MetaData(FLAT_METADATA)
