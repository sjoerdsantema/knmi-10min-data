import urllib.request, json, ssl
from pathlib import Path
import requests
import netCDF4 as nc

# knmi api url
knmi_service_url = "https://api.dataplatform.knmi.nl/open-data/datasets/Actuele10mindataKNMIstations/versions/2/files"

# this public api key is provided by the knmi and will expire on the 1st of May 2021
api_key = "5e554e19274a9600012a3eb1b626f95624124cf89e9b5d74c3304520"

# where to put the datasets - make sure it exists
download_directory = "./dataset-download/"

# Verify that the download directory exists
if not Path(download_directory).is_dir() or not Path(download_directory).exists():
    raise Exception(f"Invalid or non-existing directory: {download_directory}")

# get the url of the temp .nc file
def get_file_url():
    try: 
        url = knmi_service_url 
        context = ssl._create_unverified_context()
        uh = urllib.request.Request(url, data=None, headers={'Authorization': api_key}) # collect data
        with urllib.request.urlopen(uh, context=context) as response:
            data = response.read()
            js = json.loads(data)
            dataset_files = js.get("files")
            filename = dataset_files[0].get("filename")
            return(filename)
    except:
        return(None)

def construct_url():
    # get the temp url
    file_name = get_file_url()
    # construct the filename url
    file_url=(knmi_service_url+'/'+file_name+'/url')
    return(file_url)

def collect_and_save():
    try:
        # construct a url and get the temp .nc file
        constructed_url = construct_url()
        get_file_response = requests.get(constructed_url, headers={"Authorization":api_key})
        download_url = get_file_response.json().get("temporaryDownloadUrl")
        dataset_file_response = requests.get(download_url)
        # save the dataset in a file in the download dir
        p = Path(download_directory+get_file_url())
        p.write_bytes(dataset_file_response.content)
        return p
    except:
        # one could implement alerting here
        return(None)

# get the nc file from the knmi api
file_location = collect_and_save()
dataset = nc.Dataset(file_location)

concatenated_data = []
number_of_stations = len(dataset['stationname'][:])
for i in range(0,number_of_stations):
    to_add_stationname = dataset['stationname'][i]
    to_add_wind_direction = str(dataset['dd'][i])
    to_add_wind_speed = str(dataset['ff'][i])
    to_add_gust_speed = str(dataset['gff'][i])
    concatenated_data.append([
        {"stationname": to_add_stationname}, 
        {"wind_direction": to_add_wind_direction[1:4]},
        {"wind_speed": to_add_wind_speed[1:-1]},
        {"gust_speed": to_add_gust_speed[1:-1]}
        ])

# below here you can do with the data whatever you intended to use this script for
print(concatenated_data)
