import gspread

from pandas import DataFrame
from google.oauth2.credentials import Credentials
from typing import List
from Models.sheet import Sheet
from Models.localized_column import LocalizedColumn
from Models.localized_string import LocalizedString


# noinspection PyCompatibility
class GenerateTranslation:

    def __init__(self, credentials: Credentials):
        """ This class serves as a base class for objects responsible for generating translations
            subclass it to generate a translation file to a specific platform.
            Utilizes the `gspread` library to interact with the Google Sheet API.
        """

        spreadsheet_file_name: str = "Translations"

        # Authorize the client using the credentials
        spreadsheet_service: gspread.Client = gspread.authorize(credentials)

        # Open the spreadsheet by its title
        self._worksheets: List[gspread.Worksheet] = spreadsheet_service.open(spreadsheet_file_name).worksheets()

    @property
    def sheets(self) -> List[Sheet]:
        """
            Retrieves a list of Sheet objects. The Sheet objects are created
            by calling the `_transform_worksheets` method.

        :return List[Sheet]:
            A list of Sheet objects representing the worksheets in the spreadsheet.
        """
        return self._transform_worksheets()

    def _transform_worksheets(self) -> List[Sheet]:
        """
            Loops through worksheets in the spreadsheet, creates DataFrames from their cell values,
            and generates Sheet objects for each worksheet with data.

        :return List[Sheet]:
            A list of Sheet objects
        """
        sheet: List[Sheet] = []

        for worksheet in self._worksheets:
            # Get raw values, create DataFrame
            raw_cells_data = worksheet.get_all_values()
            local_data_frame = DataFrame(raw_cells_data)

            # Skip empty worksheets (all rows empty)
            if local_data_frame.empty:
                continue

            # Define a Sheet
            sheet.append(
                Sheet(
                    columns=self._generate_columns(local_data_frame),
                    name=worksheet.title
                )
            )

        return sheet

    def _generate_columns(self, data_frame: DataFrame) -> List[LocalizedColumn]:
        """
            This function processes a DataFrame (representing a worksheet) to create LocalizedColumn objects.
            It iterates through columns (excluding the first comment column) and creates LocalizedColumn objects
            containing language information and localized strings with comments.

        :param data_frame:
            A pandas DataFrame representing the data from a worksheet.

        :return List[LocalizedColumn]:
            A list of LocalizedColumn objects, one for each column in the DataFrame (excluding the first comment column).
        """
        # Start at second Column as first column is for comments
        start_column_index = 1

        # Define comments
        comments_start_row = 6  # Comments begin at index row 6 of spreadsheet
        comments_column_name = data_frame.columns[0]
        comments_column = data_frame[comments_column_name]
        comments = [comment for comment in comments_column[comments_start_row:]]

        # Define the columns to iterate (using index slicing)
        columns_to_iterate = data_frame.columns[start_column_index:]

        # Base Language
        base_language_column_name = data_frame.columns[1]
        base_language_column = data_frame[base_language_column_name]

        # Define column object
        localized_columns: List[LocalizedColumn] = []

        # Loop through columns starting from column B
        for column_name in columns_to_iterate:

            #Get the rows in column
            rows: List[str] = data_frame[column_name]

            # Define the starting row of localized strings
            row_stat_index = 6

            # Generate the keys
            base_language_column_name = data_frame.columns[1]
            base_language_rows = data_frame[base_language_column_name]
            keys: List[str] = self._splice_and_update_index(start_index=row_stat_index, array=base_language_rows)

            # Slice rows and create a new list with index 0
            row_of_strings = self._splice_and_update_index(start_index=row_stat_index, array=rows)

            localized_columns.append(
                LocalizedColumn(
                    language=rows[0],
                    language_code=rows[1],
                    language_name=rows[2],
                    strings=self._generate_string_rows(keys=keys, rows=row_of_strings, comments=comments)
                )
            )

        return localized_columns

    def _generate_string_rows(self, keys: List[str], rows: List[str], comments: List[str]) -> List[LocalizedString]:
        """
            This function iterates through a list of strings (representing rows in a column) and creates
            LocalizedString objects. Each LocalizedString object contains the localized value from the row
            and the corresponding comment (if available).

        :param keys List[str]:
        A list of strings representing keys for each localized string. The length of this list
        should correspond to the number of rows with actual translations

        :param rows List[str]:
            A list of strings, where each string represents a row in a column from the worksheet.

        :param comments List[str]:
            A list of strings containing comments for each row (extracted from the comments column).

        :return List[LocalizedString]:
            A list of LocalizedString objects, one for each row in the provided list.
        """
        localized_strings: List[LocalizedString] = []

        for row_index, row_value in enumerate(rows):
            if row_index <= len(keys) - 1:
                localized_strings.append(
                    LocalizedString(
                        localized_key=keys[row_index],
                        localized_value=row_value,
                        comment=self._get_comments_in_range(index=row_index, comments=comments)
                    )
                )

            else:
                localized_strings.append(
                    LocalizedString(
                        localized_key="",
                        localized_value=row_value,
                        comment=self._get_comments_in_range(index=row_index, comments=comments)
                    )
                )

        return localized_strings

    def _get_comments_in_range(self, index: int, comments: List[str]) -> str:
        """Retrieves a specific comment from a list of comments based on the provided index.

        :param self (object):
            The object instance itself (usually used in class methods).
            This function is private and intended for internal use within the class.

        :param index int:
            The index of the comment to retrieve. Valid indices range from 0 (first comment)
            to the length of the list minus 1 (last comment).

        :param comments List[str]:
            The index of the comment to retrieve.

        :return str:
            The comment string at the specified index if it exists within the valid range.
            An empty string is returned if the index is out of range.
        """
        comments_index_length = len(comments) - 1
        if comments_index_length <= index and index >= 0:
            return ""

        return comments[index]

    def _splice_and_update_index(self, start_index: int, array: List) -> List:
        """Splices a list starting from a specified index and returns a new list containing the remaining elements.

        :param self (object):
            The object instance itself (usually used in class methods)
            This function is private and intended for internal use within the class.

        :param start_index (int):
            The index at which to begin splicing the list.Elements before this index will be discarded.

        :param array (List[str]):
            The list to be spliced. It can contain elements of any data type.

        :return List:
            A new list containing the elements of the original list starting from the specified index.
            The data types of the elements will be the same as those in the original list.
        """
        return [item for item in array[start_index:]]
