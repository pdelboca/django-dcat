import os
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from dcat.models import MediaType


class Command(BaseCommand):
    help = "Import the EU's File types vocabulary into the database."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if not os.path.isfile("filetypes.xml"):
            self.stdout.write(
                self.style.ERROR(
                    "filetypes.xml does not exist. Please download it from https://op.europa.eu/s/y52f."
                )
            )
            return

        tree = ET.parse("filetypes.xml")
        root = tree.getroot()
        for record in root:
            authority_code = record.find("authority-code").text
            try:
                file_extension = record.find("file-extension").text
            except:
                self.stdout.write(
                    self.style.ERROR(
                        f"{authority_code} does not have a file extension. Skipping it."
                    )
                )
                continue
            internet_media_type = record.find("internet-media-type").text
            description = record.find("sources/source/description").text

            MediaType.objects.create(
                code=authority_code,
                extension=file_extension,
                media_type=internet_media_type,
                description=description,
            )

        total_types = MediaType.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {total_types} filetypes.")
        )
