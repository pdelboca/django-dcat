""" Models for the DCAT application.

The models are based on the DCAT specification:
https://www.w3.org/TR/vocab-dcat-3/

Initial Mandatory/Recommended/Optional properties are based on the DCAT-AP
specification: https://semiceu.github.io/DCAT-AP/releases/3.0.0/

"""
import hashlib

from django.db import models


class Agent(models.Model):
    """Any entity carrying out actions with respect to the (Core) entities.

    Example: Publishers, Creators, etc.
    """

    # Mandatory properties
    name = models.CharField(max_length=255)

    # Recommended properties
    type = models.CharField(max_length=20, blank=True)

    # Optional properties
    mbox = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Catalog(models.Model):
    """A catalogue that hosts the Datasets or Data Services being described."""

    # Mandatory properties
    title = models.CharField(max_length=255)
    description = models.TextField()
    publisher = models.ForeignKey("Agent", on_delete=models.CASCADE)

    # Recommended properties
    licence = models.ForeignKey("LicenceDocument", on_delete=models.SET_NULL, blank=True, null=True)
    themes = models.ManyToManyField("DataTheme", blank=True)
    homepage = models.URLField(blank=True)

    def __str__(self):
        return self.title


# class CatalogRecord(models.Model):
#     """A description of a Dataset's entry in the Catalogue.

#     It exists for catalogs where a distinction is made between metadata about a dataset or
#     service and metadata about the entry in the catalog about the dataset or
#     service. For example, the publication date property of the dataset reflects
#     the date when the information was originally made available by the
#     publishing agency, while the publication date of the catalog record is
#     the date when the dataset was added to the catalog.
#     """
#     pass


class Dataset(models.Model):
    """A conceptual entity that represents the information published."""

    # Mandatory properties
    title = models.CharField(max_length=255)
    catalog = models.ForeignKey("Catalog", on_delete=models.CASCADE)

    # Recommended properties
    description = models.TextField(blank=True)
    publisher = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True)
    themes = models.ManyToManyField("DataTheme", blank=True)
    keywords = models.ManyToManyField("Keyword", blank=True)

    # Optional properties
    modified = models.DateField(blank=True, null=True)
    issued = models.DateField(blank=True, null=True)
    landing_page = models.URLField(blank=True)

    def __str__(self):
        return self.title


# class DatasetInSeries(models.Model):
#     """Capture the case when a Dataset is a member of a Dataset Series."""
#     pass


# class DatasetSeries(models.Model):
#     """Datasets that are published separately, but share some characteristics."""
#     pass


class Distribution(models.Model):
    """A physical embodiment of the Dataset in a particular format.

    Example: A CSV file, an RDF file, etc.
    """

    def _get_storage_path(instance, filename):
        """Return the storage path of the file.

        The OS can complain if we store thousands of files in
        the same directory. So I'm inventing something to avoid
        this problem.
        """
        return f"files/datasets/{instance.dataset.pk}/{filename}"

    # Mandatory properties
    dataset = models.ForeignKey("Dataset", on_delete=models.CASCADE)
    @property
    def access_url(self):
        """Return the access url of the file.

        If the file is hosted in another portal, the access_url is provided
        in the distribution. Otherwise, the access_url is the URL to the
        distribution.
        """
        pass

    # Recomened properties
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=_get_storage_path, blank=True)
    format = models.ForeignKey(
        "MediaType", on_delete=models.SET_NULL, blank=True, null=True
    )
    licence = models.ForeignKey(
        "LicenceDocument", on_delete=models.SET_NULL, blank=True, null=True
    )

    external_download_url = models.URLField(blank=True, default="")
    external_access_url = models.URLField(blank=True, default="")

    # Optional properties
    checksum = models.OneToOneField(
        "Checksum", on_delete=models.SET_NULL, blank=True, null=True
    )

    @property
    def download_url(self):
        """Return the download url of the file.

        If the file is hosted in another portal, the download_url is provided
        in the distribution. Otherwise, the download_url is generated from the
        file field.
        """
        if self.external_download_url:
            return self.external_download_url
        return self.file.url

    def calculate_md5_checksum(self):
        """Calculates the md5 checksum of the file."""
        md5_hash = hashlib.md5()
        with self.file.open(mode="rb") as f:
            while chunk := f.read(4096):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def __str__(self):
        return self.title


class DataService(models.Model):
    """Operations that provides access to datasets or data processing functions.

    Example: APIs, Web Services, SPARQL endpoints, etc.
    """

    # Mandatory properties
    title = models.CharField(max_length=255)
    endpoint_url = models.URLField()
    catalog = models.ForeignKey("Catalog", on_delete=models.CASCADE)

    # Optional properties
    description = models.TextField(blank=True)
    format = models.ManyToManyField("MediaType", blank=True)
    licence = models.ForeignKey("LicenceDocument", on_delete=models.SET_NULL, null=True)


class MediaType(models.Model):
    """A set of media types from the DCAT-AP vocabulary."""

    extension = models.CharField(max_length=10)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    media_type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.extension


class LicenceDocument(models.Model):
    """A set of licences from the DCAT-AP vocabulary."""

    # Recommended properties
    @property
    def type(self):
        return self.url_general or self.label

    label = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    url_general = models.URLField(blank=True, default="")
    url_document = models.URLField(blank=True, default="")

    def __str__(self):
        return self.label


class DataTheme(models.Model):
    """Themes used for dataset classification.

    This is the mandatory controlled vocabulary for
    the themeTaxonomy field of Catalogue. (As defined
    by DCAT-AP).

    https://op.europa.eu/s/y52L
    """

    code = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.label


class Checksum(models.Model):
    """A value that allows the contents of a file to be authenticated."""

    checksum_value = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.checksum_value} ({self.algorithm})"


class Keyword(models.Model):
    """A keyword or tag describing the Dataset."""

    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name
