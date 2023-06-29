import configparser
import requests
import tarfile

def parse_config():
    config = configparser.ConfigParser()
    config.read("GeoIP.conf")

    license_key = config.get("settings", "license_key")
    database_file_path = config.get("settings", "database_file_path")

    return license_key, database_file_path


def untar_file(file_path):
    try:
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall()
        print("File extracted successfully.")
    except tarfile.TarError as e:
        print("Error extracting file:", str(e))

def download_geoip_database(license_key, file_path):
    url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=" + license_key + "&suffix=tar.gz"
    response = requests.get(url, stream=True)
    print(url)
    if response.status_code == 200:
        file_name = file_path  # The desired file name to save
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("GeoIP database downloaded successfully.")
    else:
        print("Failed to download GeoIP database. Status code:", response.status_code)

# Call the function to start the download
license_key, file_path = parse_config()
download_geoip_database(license_key, file_path)
untar_file(file_path)