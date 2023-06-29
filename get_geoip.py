import configparser
import requests
import tarfile
import os

#This will load and parse the configuration file that has the download file path and the license key for MaxMind.
def parse_config():
    try:
        config = configparser.ConfigParser()
        config.read("GeoIP.conf")
        license_key = config.get("settings", "license_key")
        database_file_path = config.get("settings", "database_file_path")
        return license_key, database_file_path
    except Exception as e:
        print("Error parsing the config file.")

#This will download the DB to the location from the config file and use your license.
def download_geoip_database(license_key, file_path):
    url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=" + license_key + "&suffix=tar.gz"
    response = requests.get(url, stream=True)
    
    try:
        if response.status_code == 200:
            file_name = file_path  # The desired file name to save
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print("GeoIP database downloaded successfully.")
    except Exception as e:
        print("Failed to download GeoIP database:", str(e))
    
#This will untar the file from the location defined in the config file.
def untar_file(file_path):
    try:
        directory = os.path.dirname(file_path)
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=directory)
        print("File extracted successfully.")
    except Exception as e:
        print("Error extracting file:", str(e))

def check_filepath(file_path):
    try:
        # Extract the directory path from the file path
        directory = os.path.dirname(file_path)

        # Check if the directory path exists and create it if it doesn't
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print("unable to creat filepath:", str(e))

# Call the function to start the download
license_key, file_path = parse_config()
check_filepath(file_path)
download_geoip_database(license_key, file_path)
untar_file(file_path)