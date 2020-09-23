import pathlib
import pprint
import logging

import odf
import odf.table
import odf.opendocument


logger = logging.getLogger(__name__)


def save_investment_update(config, current_values):

    spreadsheet_config = config.get('spreadsheet')
    file_path = pathlib.Path(spreadsheet_config.get("path"))
    if not file_path.is_file():
        logger.warning('The spreadsheet path {} is not a valid file.'.format(file_path))
        return

    sheet_name = spreadsheet_config.get("sheet_name")
    row_index = spreadsheet_config.get('listing_start_row')
    spreadsheet = odf.opendocument.load(str(file_path))
    sheet = spreadsheet.spreadsheet.firstChild
    rows = sheet.getElementsByType(odf.table.TableRow)
    # find the first row in the range that has no date in the first cell
    # while rows[row_index].
    pprint.pprint(spreadsheet)

    # find empty row
    date_column_index = spreadsheet_config.get('date_column')

    # After row data has been added, save the data
    # spreadsheet.save()