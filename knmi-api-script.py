import urllib.request, json, ssl
from pathlib import Path
import requests
import netCDF4 as nc

class FetchKnmiData():
    def collect_data(self):
        # knmi variables
        knmi_service_url = "https://api.dataplatform.knmi.nl/open-data/datasets/Actuele10mindataKNMIstations/versions/2/files"
        # this key is valid until the 25th of May 2021
        api_key = "5e554e19274a9600012a3eb1b626f95624124cf89e9b5d74c3304520"
        # where to put the datasets, make sure the dir exists
        download_directory = "./dataset-download/"
        try: 
            # Verify that the download directory exists
            if not Path(download_directory).is_dir() or not Path(download_directory).exists():
                raise Exception(f"Invalid or non-existing directory: {download_directory}")
            url = knmi_service_url 
            context = ssl._create_unverified_context()
            # construct the filename on the basis of the timestamp
            timestamp_now = datetime.utcnow()
            timestamp_latest = timestamp_now - timedelta(minutes=0) - timedelta(minutes=timestamp_now.minute % 10)
            filename = f"KMDS__OPER_P___10M_OBS_L2_{timestamp_latest.strftime('%Y%m%d%H%M')}.nc"            
            # construct the filename url
            constructed_url=(knmi_service_url+'/'+filename+'/url')
            # get response
            get_file_response = requests.get(constructed_url, headers={"Authorization":api_key})
            download_url = get_file_response.json().get("temporaryDownloadUrl")
            dataset_file_response = requests.get(download_url)
            # save the dataset in a file in the download dir
            p = Path(download_directory+filename)
            p.write_bytes(dataset_file_response.content)
            file_location = p
            # access the nc file
            dataset = nc.Dataset(file_location)
            concatenated_data = []
            number_of_stations = len(dataset['stationname'][:])
            # cardinals for conversion degrees to cardinals
            dirs = ['N', 'NNO', 'NO', 'ONO', 'O', 'OZO', 'ZO', 'ZZO', 'Z', 'ZZW', 'ZW', 'WZW', 'W', 'WNW', 'NW', 'NNW']
            for i in range(0,number_of_stations):
                to_add_wind_direction = str(dataset['dd'][i])[1:4]
                # remove the dot from the wind direction var
                to_add_wind_direction_degrees = to_add_wind_direction.replace('.', '')
                # take care of the double dash in the var provided
                if to_add_wind_direction_degrees == "--]":
                    to_add_wind_direction_cardinal = "-"
                    to_add_wind_direction_degrees = "-"
                else:
                    # degrees to cardinal
                    ix = round(int(to_add_wind_direction_degrees) / (360. / len(dirs)))
                    to_add_wind_direction_cardinal = dirs[ix % len(dirs)]
                # and here are the other vars - these can be extended with more knmi vars
                to_add_stationname = dataset['stationname'][i]
                to_add_wind_speed_ms = str(dataset['ff'][i])[1:-1]
                if to_add_wind_speed_ms == "--":
                    to_add_wind_speed_ms = 0
                to_add_wind_speed_knots = int(round(float(to_add_wind_speed_ms)*1.9438445))
                to_add_gust_speed_ms = str(dataset['gff'][i])[1:-1]
                if to_add_gust_speed_ms == "--":
                    to_add_gust_speed_ms = 0
                to_add_gust_speed_knots = int(round(float(to_add_gust_speed_ms)*1.9438445))
                # concatenate the list with dicts
                concatenated_data.append([
                    {"stationname": to_add_stationname}, 
                    {"wind_direction_cardinal": to_add_wind_direction_cardinal},
                    {"wind_direction_degrees": to_add_wind_direction_degrees},
                    {"wind_speed_ms": to_add_wind_speed_ms},
                    {"gust_speed_ms": to_add_gust_speed_ms},
                    {"wind_speed_knots": to_add_wind_speed_knots},
                    {"gust_speed_knots": to_add_gust_speed_knots}
                    ])
            return concatenated_data
        except Exception as error_message:
            # one could implement alerting here
            return(error_message)

data = FetchKnmiData()
print(data.collect_data())



