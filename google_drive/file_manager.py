from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from googleapiclient.discovery import build
from typing import List


# noinspection PyCompatibility
class FileManager:
    """
       A class for managing file operations related to Google Drive.

       This class provides static methods for creating folders, retrieving folder IDs,
       and saving files to Google Drive.
   """

    @staticmethod
    def _create_folder(drive_service: build, parent_folder_id: str, folder_name: str):
        """Create a new folder in Google Drive.

        :param
            drive_service (build): An instance of the Google Drive API service object.

        :param
            parent_folder_id (str): The ID of the parent folder where the new folder will be created.

        :param
            folder_name (str): The name of the new folder to be created.

        :return:
            str: The ID of the newly created folder.
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    @staticmethod
    def _get_folder_id(drive_service: build, parent_folder_id: str, folder_name: str):
        """Retrieve the ID of a folder in Google Drive.

        :param drive_service:
            An instance of the Google Drive API service object.

        :param parent_folder_id:
            The ID of the parent folder where the folder is located.

        :param folder_name:
            The name of the folder whose ID is to be retrieved.

        :return  str or None:
            The ID of the folder if found, otherwise None.
        """
        query = f"'{parent_folder_id}' in parents and name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        folders = results.get('files', [])
        if folders:
            return folders[0]['id']
        else:
            return None

    @staticmethod
    def save_to_google_drive(drive_service: build, file: str, file_name: str, mime_type: str, folder_structure: List[str]):

        # Get the root folder ID
        root_folder_id = 'root'
        current_folder_id = root_folder_id

        # Create the folder structure if it doesn't exist
        for folder_name in folder_structure:
            folder_id = FileManager._get_folder_id(
                drive_service=drive_service,
                parent_folder_id=current_folder_id,
                folder_name=folder_name
            )
            if folder_id:
                current_folder_id = folder_id
            else:
                current_folder_id = FileManager._create_folder(
                    drive_service=drive_service,
                    parent_folder_id=current_folder_id,
                    folder_name=folder_name
                )

        file_metadata = {'name': file_name, 'parents': [current_folder_id]}
        media = MediaIoBaseUpload(BytesIO(file.encode()), mimetype= mime_type, resumable=True)
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f'File ID: {file.get("id")}')