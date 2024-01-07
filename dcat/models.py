""" Models for the DCAT application.

The models are based on the DCAT specification:
https://www.w3.org/TR/vocab-dcat-3/

Initial Mandatory/Recommended/Optional properties are based on the DCAT-AP
specification: https://semiceu.github.io/DCAT-AP/releases/3.0.0/

For the help_text we are copying the description of the properties from
the DCAT-AP specification.

"""
import hashlib

from django.db import models


class Agent(models.Model):
    """Any entity carrying out actions with respect to the (Core) entities.

    Example: Publishers, Creators, etc.
    """

    # Mandatory properties
    name = models.CharField(max_length=255, help_text="A name of the Agent.")

    # Recommended properties
    type = models.CharField(
        max_length=20,
        blank=True,
        help_text="A type of the agent that makes the Catalogue or Dataset available.",
    )

    # Optional properties
    mbox = models.EmailField(
        blank=True, null=True, help_text="An email address of the Agent."
    )

    def __str__(self):
        return self.name


class Catalog(models.Model):
    """A catalogue that hosts the Datasets or Data Services being described."""

    # Mandatory properties
    title = models.CharField(max_length=255, help_text="A name given to the Catalogue.")
    description = models.TextField(help_text="A free-text account of the Catalogue.")
    publisher = models.ForeignKey(
        "Agent",
        on_delete=models.CASCADE,
        help_text="An entity (organisation) responsible for making the Catalogue available.",
    )

    # Recommended properties
    licence = models.ForeignKey(
        "LicenceDocument",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="A licence under which the Catalogue can be used or reused.",
    )
    themes = models.ManyToManyField(
        "DataTheme",
        blank=True,
        help_text="A knowledge organization system used to classify the Catalogue's Datasets.",
    )
    homepage = models.URLField(
        blank=True, help_text="A web page that acts as the main page for the Catalogue."
    )

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
    title = models.CharField(max_length=255, help_text="A name given to the Dataset.")
    catalog = models.ForeignKey("Catalog", on_delete=models.CASCADE)

    # Recommended properties
    description = models.TextField(
        blank=True, help_text="A free-text account of the Dataset."
    )
    publisher = models.ForeignKey(
        "Agent",
        on_delete=models.SET_NULL,
        null=True,
        help_text="An entity (organisation) responsible for making the Dataset available.",
    )
    themes = models.ManyToManyField(
        "DataTheme",
        blank=True,
        help_text="A category of the Dataset. A Dataset may be associated with multiple themes.",
    )
    keywords = models.ManyToManyField(
        "Keyword", blank=True, help_text="A keyword or tag describing the Dataset."
    )

    # Optional properties
    modified = models.DateField(
        blank=True,
        null=True,
        help_text="The most recent date on which the Dataset was changed or modified.",
    )
    issued = models.DateField(blank=True, null=True)
    landing_page = models.URLField(
        blank=True,
        help_text="A web page that provides access to the Dataset, its Distributions and/or additional information. It is intended to point to a landing page at the original data provider, not to a page on a site of a third party, such as an aggregator.",
    )

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
    title = models.CharField(
        max_length=255, blank=True, help_text="A name given to the Distribution."
    )
    description = models.TextField(
        blank=True, help_text="A free-text account of the Distribution."
    )
    file = models.FileField(upload_to=_get_storage_path, blank=True)
    format = models.ForeignKey(
        "MediaType",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The file format of the Distribution.",
    )
    licence = models.ForeignKey(
        "LicenceDocument",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="A licence under which the Distribution is made available. ",
    )

    external_download_url = models.URLField(
        blank=True,
        default="",
        help_text="A URL that is a direct link to a downloadable file in a given format.",
    )
    external_access_url = models.URLField(
        blank=True,
        default="",
        help_text="A URL that gives access to a Distribution of the Dataset. The resource at the access URL may contain information about how to get the Dataset.",
    )

    # Optional properties
    checksum = models.OneToOneField(
        "Checksum",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="A mechanism that can be used to verify that the contents of a distribution have not changed. The checksum is related to the download_url.",
    )

    @property
    def download_url(self):
        """Return the download url of the file.

        If the file is hosted in another portal, the download_url is provided
        in the distribution. Otherwise, the download_url is generated from the
        file field.

        This field is not mandatory so it can return an empty string (a distrubution
        can contain only an access_url.)
        """
        if self.external_download_url:
            return self.external_download_url
        if self.file:
            return self.file.url
        return ""

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
    title = models.CharField(max_length=255, help_text="A name given to the DataService.")
    endpoint_url = models.URLField(
        help_text="The root location or primary endpoint of the service (an IRI)."
    )
    catalog = models.ForeignKey("Catalog", on_delete=models.CASCADE)

    # Optional properties
    description = models.TextField(
        blank=True, help_text="A free-text account of the DataService."
    )
    format = models.ManyToManyField(
        "MediaType",
        blank=True,
        help_text="The structure that can be returned by querying the endpointURL.",
    )
    licence = models.ForeignKey(
        "LicenceDocument",
        on_delete=models.SET_NULL,
        null=True,
        help_text="A licence under which the Data service is made available.",
    )


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
