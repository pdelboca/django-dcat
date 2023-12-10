import os
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from dcat.models import LicenceDocument


class Command(BaseCommand):
    help = "Import the EU's Licences vocabulary into the database."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if not os.path.isfile("licences.xml"):
            self.stdout.write(
                self.style.ERROR(
                    "licences.xml does not exist. Please download it from https://op.europa.eu/s/y52h."
                )
            )
            return

        tree = ET.parse("licences.xml")
        root = tree.getroot()
        for record in root:
            if record.attrib["deprecated"] == "true":
                self.stdout.write(
                    self.style.WARNING(f"{licence.code} is deprecated. Skipping.")
                )
                continue
            code = record.find("authority-code").text
            label = [
                label.text
                for label in record.find("label").findall("lg.version")
                if label.attrib["lg"] == "eng"
            ][0]
            try:
                url_general = record.find("url.general").text
            except:
                url_general = None
                self.stdout.write(
                    self.style.ERROR(
                        f"{code} does not have a url.general. Setting it to None."
                    )
                )
            try:
                url_document = record.find("url.document").text
            except:
                url_document = None
                self.stdout.write(
                    self.style.ERROR(
                        f"{code} does not have a url.document. Setting it to None."
                    )
                )
            licence, created = LicenceDocument.objects.get_or_create(
                code=code,
                label=label,
                url_general=url_general,
                url_document=url_document,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported {licence.code}.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"{licence.code} already exists in the database."
                    )
                )

        total_licences = LicenceDocument.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {total_licences} licences.")
        )
