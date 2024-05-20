class LocalizedString:
    """
        This class represents a single row in a localized string table. It contains
        the localized value for a specific language and an optional comment
        associated with the string.
    """

    def __init__(self, localized_key: str, localized_value: str, comment: str):
        """Initializes a new LocalizedString object.

        Args:
            localized_key (str): The unique key for the localized string. This key can be used to identify
                                 the specific string within the translation context.
            localized_value (str): The actual translated string value for a specific language.
            comment (str): An optional comment associated with the localized string. Defaults to an empty string.
        """
        self._localized_key = localized_key
        self._localized_value = localized_value
        self._comment = comment

    @property
    def localized_key(self) -> str:
        return self._localized_key

    @property
    def localized_value(self) -> str:
        """Gets the localized value (translated string) associated with this object.

        :return str:
            The localized string value.
        """
        return self._localized_value

    @property
    def comment(self) -> str:
        """Gets the optional comment associated with this LocalizedString object.

        :return: str:
            The comment string, or an empty string if no comment was provided.
        """
        return self._comment
