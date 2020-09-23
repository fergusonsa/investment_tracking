import pathlib
import logging

import ezodf

logger = logging.getLogger(__name__)


def save_investment_update(config, current_values):

    spreadsheet_config = config.get('spreadsheet')
    file_path = pathlib.Path(spreadsheet_config.get("path"))
    if not file_path.is_file():
        logger.warning('The spreadsheet path {} is not a valid file.'.format(file_path))
        return

    sheet_name = spreadsheet_config.get("sheet_name")
    row_index = spreadsheet_config.get('listing_start_row')
    date_column_index = spreadsheet_config.get('date_column')
    total_column_index = spreadsheet_config.get('total_column')
    spreadsheet = ezodf.opendoc(str(file_path))
    sheet = spreadsheet.sheets[sheet_name]
    # find the first row in the range that has no date in the first cell
    while sheet[f'{date_column_index}{row_index}'].value_type == 'date' and row_index < 366:
        row_index += 1
    accounts_config = config.get('accounts')
    for column in current_values.keys():
        if column == 'date':
            cell_index = f'{date_column_index}{row_index}'
            cell = sheet[cell_index]
            cell.set_value(current_values[column], 'date')
        else:
            column_index = accounts_config[column]['column']

            cell = sheet[f'{column_index}{row_index}']
            cell.set_value(current_values[column], currency='CAD')

    # After row data has been added, save the data
    spreadsheet.save()
