from generate_translations_base import GenerateTranslation
from googleapiclient.discovery import build
from file_manager import FileManager

import json


# noinspection PyCompatibility
class IOSTranslation(GenerateTranslation):

    """
    An XCStrings file is composed of the following structure and is mapped using the following properties
    {
          "sourceLanguage" : COLUMN_VALUE.LANGUAGE_CODE,
          "strings" : {
            LOCALIZED_STRING.LOCALIZED_KEY : {
              "localizations" : {
                "LOCALIZED_STRING.LANGUAGE_CODE" : {
                  "stringUnit" : {
                    "state" : "translated",
                    "value" : "LOCALIZED_STRING.LOCALIZED_VALUE"
                  }
                }
              }
            },
          },
          "version" : "1.0"
        }
    """

    def generate(self):
        dictionary = {
            "sourceLanguage": "",
            "strings": {
            },
        }

        for sheet in self.sheets:
            for column_index, column_value in enumerate(sheet.columns):

                # First language on the columns list will be considered the default or source language
                if column_index == 0:
                    dictionary["sourceLanguage"] = column_value.language_code

                    for localized_string in column_value.strings:
                        dictionary["strings"].update({
                            localized_string.localized_key: {}
                        })
                else:
                    for localized_string in column_value.strings:

                        # Append Localization String

                        # Check if key and value is not empty
                        if not localized_string.localized_key or not localized_string.localized_value:
                            continue

                        # Check if value is not a comment
                        if (not localized_string.localized_key.startswith("//") and
                                localized_string.localized_value.startswith("//")):
                            continue

                        # Check if field "localizations" exist
                        if "localizations" not in dictionary["strings"][localized_string.localized_key]:
                            dictionary["strings"][localized_string.localized_key].update({
                                "localizations": {
                                    column_value.language_code: {
                                        "stringUnit": {
                                            "state": "translated",
                                            "value": localized_string.localized_value
                                        }
                                    }
                                }
                            })
                            continue

                        # If it already exists only append the localized string in the "localizations" field
                        dictionary["strings"][localized_string.localized_key]["localizations"].update({
                            column_value.language_code: {
                                "stringUnit": {
                                    "state": "translated",
                                    "value": localized_string.localized_value
                                }
                            }
                        })

                        # Append Comments on Localization String (if there's any)
                        if not localized_string.comment:
                            continue

                        dictionary["strings"][localized_string.localized_key].update({
                            "comment": localized_string.comment
                        })

        dictionary["version"] = "1.0"

        FileManager.save_to_google_drive(
            drive_service=build('drive', 'v3', credentials=self._credentials),
            file=json.dumps(dictionary, ensure_ascii=False, indent=2),
            file_name="Localizable.json",
            mime_type="application/json",
            folder_structure=['Translations', 'iOS']
        )
