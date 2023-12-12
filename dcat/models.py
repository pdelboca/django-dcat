""" Models for the DCAT application.

The models are based on the DCAT specification:
https://www.w3.org/TR/vocab-dcat-3/

Initial Mandatory/Recommended/Optional properties are based on the DCAT-AP
specification: https://semiceu.github.io/DCAT-AP/releases/3.0.0/

"""

from django.db import models


class Resource(models.Model):
    """Anything described by RDF."""

    pass


class Agent(models.Model):
    """Any entity carrying out actions with respect to the (Core) entities.

    Example: Publishers, Creators, etc.
    """

    # Mandatory properties
    name = models.CharField(max_length=255)

    # Recommended properties
    type = models.CharField(max_length=20)

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
    license = models.ForeignKey("LicenceDocument", on_delete=models.SET_NULL, null=True)

    # Recommended properties
    themes = models.ManyToManyField("DataTheme")

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


class Dataset(Resource):
    """A conceptual entity that represents the information published."""

    # Mandatory properties
    title = models.CharField(max_length=255)
    catalog = models.ForeignKey("Catalog", on_delete=models.CASCADE)

    # Recommended properties
    description = models.TextField()
    publisher = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True)
    themes = models.ManyToManyField("DataTheme")

    def __str__(self):
        return self.title


# class DatasetInSeries(Resource):
#     """Capture the case when a Dataset is a member of a Dataset Series."""
#     pass


# class DatasetSeries(Resource):
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
    @property
    def access_url(self):
        pass

    # Recomened properties
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=_get_storage_path)
    dataset = models.ForeignKey("Dataset", on_delete=models.CASCADE)
    format = models.ForeignKey("MediaType", on_delete=models.SET_NULL, null=True)
    license = models.ForeignKey("LicenceDocument", on_delete=models.SET_NULL, null=True)
    external_download_url = models.URLField(blank=True, null=True)

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

    def __str__(self):
        return self.title


# class DataService(Resource):
#     """Operations that provides access to datasets or data processing functions.

#     Example: APIs, Web Services, SPARQL endpoints, etc.
#     """
#     pass


# class Checksum(models.Model):
#     """A value that allows the contents of a file to be authenticated."""
#     pass


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
    url_general = models.URLField(null=True)
    url_document = models.URLField(null=True)

    def __str__(self):
        return self.label


class DataTheme(models.Model):
    """Themes used for dataset classification.

    This is the mandatory controlled vocabulary for
    the themeTaxonomy field of Catalogue. (As defined
    by DCAT-AP).

    https://op.europa.eu/s/y52L
    """

    code = models.CharField(max_length=10)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.label
