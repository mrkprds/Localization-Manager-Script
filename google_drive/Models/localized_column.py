from typing import List
from Models.localized_string import LocalizedString


class LocalizedColumn:
    """
        This class represents a column within a localized string table in a Google Sheet.
        It contains information about the language the column represents,
        including the language code and name, as well as a list of LocalizedString objects.
        Each LocalizedString object represents a row in the column, containing the
        translated string value and an optional comment.
   """

    def __init__(self, language: str, language_code: str, language_name: str, strings: List[LocalizedString]):
        """Initializes a new LocalizedColumn object.

           Args:
               language (str): Name of the language represented by this column (e.g., "English").
               language_code (str): Language code associated with the language (e.g., "en").
               language_name (str): Full name of the language (e.g., "English (US)").
               strings List[LocalizedString]: List of LocalizedString objects, where each object
                                              represents a row in the column containing the translated
                                              string value and an optional comment.
        """
        self._language = language
        self._language_code = language_code
        self._language_name = language_name
        self._strings = strings

    @property
    def language(self) -> str:
        """ Gets the language name associated with this column (e.g., "English").

        :return str:
            The language name.
        """
        return self._language

    @property
    def language_code(self) -> str:
        """Gets the language code associated with this column (e.g., "en").

        :return str:
            The language code.
        """
        return self._language_code

    @property
    def language_name(self) -> str:
        """Gets the full language name associated with this column (e.g., "English (US)").

        :return str:
            The full language name.
        """
        return self._language_name

    @property
    def strings(self) -> list[LocalizedString]:
        """Gets the list of LocalizedString objects associated with this column.

        :return List[LocalizedString]:
            A list of LocalizedString objects representing rows in the column.
        """
        return self._strings
