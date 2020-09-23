import pathlib
import pprint
import logging

import pyexcel_ods3


logger = logging.getLogger(__name__)


def save_investment_update(config, current_values):

    spreadsheet_config = config.get('spreadsheet')
    file_path = pathlib.Path(spreadsheet_config.get("path"))
    if not file_path.is_file():
        logger.warning('The spreadsheet path {} is not a valid file.'.format(file_path))
        return

    sheet_name = spreadsheet_config.get("sheet_name")
    row_index = spreadsheet_config.get('listing_start_row')
    data = pyexcel_ods3.get_data(str(file_path), sheet_name=sheet_name, start_row=row_index)

    pprint.pprint(data)

    # find empty row
    date_column_index = spreadsheet_config.get('date_column')

    # After row data has been added, save the data
    # pyexcel_ods3.save_data(str(file_path), data)