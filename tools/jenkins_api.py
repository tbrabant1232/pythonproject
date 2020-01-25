import os
from datetime import datetime

import click
import requests

JSON_FOLDER = os.path.join(os.path.expanduser('~/Pictures'), 'NASA')
URL = 'http://ci-transpoqa.qa.chq.ei/ci-transpoqa/view/Transportation-QA/view/Master%20Consol/view/MCRobot%20Functional/'
AirPOD_ENDPOINT = 'job/MCRobotFunctional%20Air/ws/target/ParallelReports/'
OceanPOD_ENDPOINT = 'job/MCRobotFunctional%20Ocean/ws/target/ParallelReports/'
MmPOD_ENDPOINT = 'job/MCRobotFunctional%20Multimode/ws/target/ParallelReports/'
TruckPOD_ENDPOINT = 'job/MCRobotFunctional%20Transcon/ws/target/ParallelReports/'
API_KEY = 'DEMO_KEY'

if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

 #   TODO: Need to log in



def get_info(date=datetime.today()):
    """
    Downloads the meta-info about jsons for specified date

    Arguments:
    date -- date for which POD should be retrieved, defaults to today

    Output:
    Dictionary with meta-information about POD
    """
    try:
        params = {
            'date': date.strftime("%Y-%m-%d"),
            'hd': True,
            'api_key': API_KEY
        }

        response = requests.get(URL + POD_ENDPOINT, params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        click.echo(f"Could not download meta-info for POD {date.date()}..")
        raise e


def download_json(date=datetime.today()):
    """
    Downloads the hd json for a specified date, and shows progress bar

    Arguments:
    date -- date for which POD should be retrieved, defaults to today

    Output:
    File path of saved json
    """
    try:
        # Download meta_info for url
        meta_info = get_info(date=date)
        if "hdurl" not in meta_info.keys():
            raise KeyError("download_json: meta_info does not contain hdurl.")
        url = meta_info['hdurl']

        # Construct path to save json
        title = meta_info['title'].replace(' ', '-')
        json_name = f"{date.strftime('%Y-%m-%d')}_{title}.jpg"
        json_path = os.path.join(JSON_FOLDER, json_name)

        # Check if json is already downloaded
        if os.path.exists(json_path):
            click.echo(
                "Today's json has already been downloaded and is now being set as background."
            )

        else:
            # Initialize stream and filesize
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length'))

            with open(json_path, 'wb') as local_file:
                # Initialize progress bar
                with click.progressbar(
                        length=total_size,
                        label=
                        f"Downloading - {meta_info['title']} ({date.date()})"
                ) as bar:
                    # Download chunks and update progress bar
                    for data in response.iter_content(chunk_size=4096):
                        local_file.write(data)
                        bar.update(len(data))

        return json_path

    except KeyError as e:
        raise e
    except Exception as e:
        click.echo(f"Could not download: {meta_info['title']}")
        raise e
