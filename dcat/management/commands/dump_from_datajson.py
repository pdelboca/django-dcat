import json
import logging
import multiprocessing
import os

from django.core.management.base import BaseCommand

logging.basicConfig(filename="download-logs.txt", level=logging.INFO, format="")


def _download_resources_from_dataset(dataset):
    """Download the resources of a dataset.

    Resources will be downloaded in: `data/<dataset_id>/<resource_id>`
    If the folder already exists, it will be assumed as already donwloaded and the process will
    continue with the next one.
    """
    folder_name = "data"
    try:
        os.mkdir(f"{folder_name}/{dataset['identifier']}")
    except FileExistsError:
        pass

    resources = dataset["distribution"]

    logging.info(
        f"Downloading {len(resources)} resources from dataset {dataset['title']}"
    )

    for resource in resources:
        dir_name = f"{folder_name}/{dataset['identifier']}/{resource['identifier']}"
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            # If the resource directory already exists, asume it has been downloaded
            # and continue with the next resource
            continue
        url = resource.get("downloadURL")

        if url is None:
            logging.error(f"Resource {resource['title']} does not have a download URL")
            continue

        exit_value = os.system(
            f"wget --connect-timeout 3 -t 2 --no-check-certificate --directory-prefix '{dir_name}' -q {url}"
        )
        if exit_value != 0:
            logging.error(f"Error when downloading: {url}")
            continue


class Command(BaseCommand):
    help = "Reads a data.json (ckanext-datajson) and downloads all files."

    def handle(self, *args, **options):
        data = {}
        with open("data.json", "r") as f:
            data = json.load(f)
        datasets = data["dataset"]

        try:
            os.mkdir("data")
        except FileExistsError:
            pass

        with multiprocessing.Pool(processes=8) as pool:
            pool.map(_download_resources_from_dataset, datasets)

        logging.info("Finished downloading all resources")
