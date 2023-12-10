import json

from os import listdir

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from dcat.models import (
    Catalog,
    Dataset,
    Distribution,
    Agent,
    MediaType,
    LicenceDocument,
    DataTheme,
)


class Command(BaseCommand):
    help = "Import data from a DCAT-US file provided by ckanext-datajson."

    def _get_content_file(self, dataset, distribution):
        """Returns a ContentFile to be added to the django model.

        This takes into consideration the following contents in the folder
        where the command is executed:
        - data.json
        - data/
          - {dataset_identifier}
            - {distribution_identifier}
              - some-file.csv
        """
        file_folder = (
            f'data/{dataset.get("identifier")}/{distribution.get("identifier")}'
        )
        file = None
        try:
            local_file_name = listdir(file_folder)[0]
            file_path = f"{file_folder}/{local_file_name}"
            file = ContentFile(
                open(file_path, mode="rb").read(), name=distribution.get("fileName")
            )
        except IndexError:
            self.stdout.write(
                self.style.ERROR(
                    f'{distribution.get("identifier")} folder does not have a file'
                )
            )
        return file

    def handle(self, *args, **options):
        with open("data.json", "r") as file:
            data = json.load(file)

        # Import Catalog
        title = data.get("title")
        description = data.get("description")
        publisher, _ = Agent.objects.get_or_create(
            name=data.get("publisher").get("name"),
            mbox=data.get("publisher").get("mbox", ""),
        )
        try:
            license = LicenceDocument.objects.get(code=data.get("license"))
        except ObjectDoesNotExist:
            license = None
            self.stdout.write(
                self.style.WARNING(
                    "Catalog does not have a license. Setting it to None."
                )
            )

        catalog = Catalog.objects.create(
            title=title, description=description, publisher=publisher, license=license
        )

        for theme in data.get("themeTaxonomy", []):
            theme_id = theme.get("id")
            theme_label = theme.get("label")
            theme_description = theme.get("description")

            theme_obj, _ = DataTheme.objects.get_or_create(
                code=theme_id,
                label=theme_label,
                description=theme_description,
            )
            catalog.themes.add(theme_obj)

        # Import Datasets
        datasets = data.get("dataset")
        for dataset in datasets:
            dataset_info = {}
            dataset_info["title"] = dataset.get("title")
            dataset_info["description"] = dataset.get("description")
            dataset_info["publisher"], _ = Agent.objects.get_or_create(
                name=dataset.get("publisher").get("name"),
                mbox=dataset.get("publisher").get("mbox", ""),
            )
            dataset_info["catalog"] = catalog
            dataset_created = Dataset.objects.create(**dataset_info)

            for theme in dataset.get("theme", []):
                try:
                    dataset_theme = DataTheme.objects.get(code=theme)
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Theme of {dataset.get("identifier")} does not existed a theme'
                        )
                    )
                dataset_created.themes.add(dataset_theme)

            # Import Distributions
            distributions = dataset.get("distribution", [])
            for distribution in distributions:
                distribution_info = {}
                distribution_info["dataset"] = dataset_created
                distribution_info["title"] = distribution.get("title")
                distribution_info["description"] = distribution.get("description", "")
                distribution_info["file"] = self._get_content_file(
                    dataset, distribution
                )
                file_name = distribution.get("fileName")
                if not file_name:
                    # If the file name is not provided, the dataset is hosted
                    # in another portal. We add the download_url instead.
                    external_download = distribution.get("downloadURL")
                    if external_download:
                        distribution_info["external_download_url"] = distribution.get(
                            "downloadURL"
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f'{distribution.get("identifier")} does not have a file name or a download url'
                            )
                        )

                _format = distribution.get("format")
                if _format:
                    try:
                        distribution_info["format"] = MediaType.objects.get(
                            code=_format
                        )
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'{distribution.get("fileName")}. Could not match {_format} with a MediaType'
                            )
                        )

                _license = distribution.get("license")
                if _license:
                    try:
                        distribution_info["license"] = LicenceDocument.objects.get(
                            code=_license
                        )
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'{distribution.get("fileName")}. Could not match {_license} with a LicenceDocument'
                            )
                        )

                Distribution.objects.create(**distribution_info)

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
