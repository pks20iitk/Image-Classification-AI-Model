import zipfile
import os
import gdown
from src.cnnClassifier import logger
from src.cnnClassifier.utils.common import get_size
from src.cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_file(self):
        """feth data from url"""
        try:
            dataset_url = self.config.source_url
            print(dataset_url)
            zip_download_dir = self.config.local_data_file
            print("file_path:",f"File path: {self.config.local_data_file}")
            print("extension:",f"File extension: {self.config.local_data_file}")
            # print(zip_download_dir)
            # print()
           
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")
            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?id="
            gdown.download(prefix+file_id, zip_download_dir)
            logger.info(f"Downloaded data from {dataset_url} info file {zip_download_dir}")
        except Exception as e:
            raise e
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into data directory
        function return None

        """
        unzip_path = self.config.unzip_dir
        print("unzip_path:", unzip_path)
        os.makedirs(unzip_path,exist_ok=True)
        print("zip:", self.config.local_data_file)
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            # Check if the file is a valid zip file
                if not zip_ref.testzip():
                    zip_ref.extractall(unzip_path)
                    print("Successfully extracted zip file.")
                else:
                    print("Error: The file is not a valid zip file.")
        except zipfile.BadZipFile:
            print("Error: The file is not a valid zip file.")
        except Exception as e:
            print(f"Error: {e}")

        