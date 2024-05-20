from generate_translations_base import GenerateTranslation
from  typing import

import json

class IOSTranslation(GenerateTranslation):
    def generate(self):
        dictionary = {}

        for sheet in self.sheets:
            for column_index, column_value in enumerate(sheet.columns):
                if column_index == 0:
                    dictionary["sourceLanguage"] = column_value.language_code

                    for localized_string in column_value.strings:
                        dictionary[localized_string.localized_key] = {}
                else:
                    for localized_string in column_value.strings:

                        # Append Localization String
                        if not localized_string.localized_key or not localized_string.localized_value:
                            continue

                        if localized_string.localized_value.startswith("//"):
                            continue

                        dictionary[localized_string.localized_key] = {
                            "localizations": {
                                column_value.language_code: {
                                    "stringUnit": {
                                        "state": "translated",
                                        "value": localized_string.localized_value
                                    }
                                }
                            }
                        }

                        # Append Comments on Localization String (if there's any)
                        if not localized_string.comment:
                            continue

                        dictionary[localized_string.localized_key]["comment"] = localized_string.comment

        dictionary["version"] = "1.0"
        json_data = json.dumps(dictionary)

        self.file_manager.save_to_google_drive(
            file=json_data,
            file_name="Localization.json",
            folder_name="iOS"

        )