from generate_translations_base import GenerateTranslation
from googleapiclient.discovery import build
from file_manager import FileManager

import xml.etree.ElementTree as ET
from xml.dom import minidom


class AndroidTranslation(GenerateTranslation):
    def generate(self):
        resources = ET.Element("resources")

        for sheet in self.sheets:
            for column_index, column_value in enumerate(sheet.columns):
                # First language on the columns list will be considered the default or source language
                if column_index == 0:
                    source_language = column_value.language_code

                    for localized_string in column_value.strings:
                        # Skip comments
                        if localized_string.localized_key.startswith("//"):
                            continue

                        # Create a new string element for the source language
                        string_element = ET.SubElement(resources, "string", name=localized_string.localized_key)
                        string_element.text = localized_string.localized_value
                else:
                    for localized_string in column_value.strings:
                        # Check if key and value are not empty
                        if not localized_string.localized_key or not localized_string.localized_value:
                            continue

                        # Skip comments
                        if localized_string.localized_key.startswith("//") or localized_string.localized_value.startswith("//"):
                            continue

                        # Find the existing string element for the source language
                        string_element = resources.find("string[@name='{}']".format(localized_string.localized_key))

                        if string_element is None:
                            # If the string element doesn't exist, create a new one
                            string_element = ET.SubElement(resources, "string", name=localized_string.localized_key)

                        # Create a new string-array element for the translation
                        translation_element = ET.SubElement(string_element, "item", {"qualifier": "locale/{}".format(column_value.language_code)})
                        translation_element.text = localized_string.localized_value

        # Save the XML tree to a file
        tree = ET.ElementTree(resources)
        xml_string = minidom.parseString(ET.tostring(tree.getroot(), encoding='utf-8', method='xml')).toprettyxml(indent="    ")

        FileManager.save_to_google_drive(
            drive_service=build('drive', 'v3', credentials=self._credentials),
            file=xml_string,
            file_name="strings.xml",
            mime_type="application/xml",
            folder_structure=['Translations', 'Android']
        )
