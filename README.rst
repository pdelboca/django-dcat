
===========
django-dcat
===========

django-dcat is a Django app that provides a model layer for `DCAT 3.0 <https://www.w3.org/TR/vocab-dcat-3/>`_
metadata and some command line tools to import data to it, to create vocabularies and more.

**Note:** This is a work in progress and it is not stable for production. If you wanna see an example of what can
be done checkout `Catalogo Social <https://catalogosocial.fly.dev/>`_, a data catalog implemented with django-dcat.

Quick start
###########

1. Install the package using pip::

    pip install django-dcat

2. Add "dcat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "dcat",
    ]

3. Run ``python manage.py migrate`` to create the DCAT models in your database.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to start adding data (you'll need the Admin app enabled).

5. Run ``python manage.py --help`` to see the available commands.

CLI utilities
#############

Migrating from CKAN
*******************

There are two commands that allows you to:

1) Make a dump of data from a CKAN data portal (that has `ckanext-datajson <https://github.com/GSA/ckanext-datajson>`_ installed)
2) Create a Catalog with its related entities (datasets, distributions, etc)

.. code:: bash

    # Download the data.json file from the portal
    $ wget -O data.json https://www.ckan-example.org/data.json

    # Download all files from the portal (by default in a data/ folder)
    $ python manage.py dump_from_datajson

    # Import all data and files into a local catalog
    $ python manage.py import_from_datajson


Controlled vocabularies for standardise metadata
************************************************

There are two commands to import controlled vocabularies used in the EU Open Data Portal in order to standardise the metadata.

.. code:: bash

    # Populate records for the MediaType model (CSV, PDF, etc)
    $ python manage.py import_filetypes

    # Populate records for Licences (MIT, Apache, etc)
    $ python manage.py import_licences


The goal of these commands is to provide data publishers with pre-filled options for the metadata fields. This will improve
data quality and avoid common problems like duplicated metadata values for typos or inconsistent data entry (like distributions with
.csv, .CSV, CSV, etc)


Extending the model
###################

``django-dcat`` focuses on providing a model layer for DCAT metadata. However, if you require custom fields in your application,
you can extend any model using a OneToOneField pattern (similar to what you use to extend Django's User model).

.. code:: python

    from django.db import models
    from dcat.models import Distribution


    class DistributionExtras(Distribution):
        distribution = models.OneToOneField(Distribution, on_delete=models.CASCADE, related_name='extras')
        my_extra_field = models.CharField(max_length=255, blank=True, null=True)

And then you can call this fields from your code using the related name attribute:

.. code:: python

    from dcat.models import Distribution

    distribution = Distribution.objects.get(pk=1)
    print(distribution.extras.my_extra_field)


Note: Instead of calling it ``extras`` You can play with more semantic names for the related_name
attribute like the name of your app.


Implementation notes
####################

The Django models in this package are inspired by the diagram presented in DCAT profiles.

See the diagram: `UML diagram illustrating the DCAT-AP specification <https://semiceu.github.io/DCAT-AP/releases/3.0.0/html/overview.jpg>`_

For more information on DCAT:
 - `Data Catalog Vocabulary (DCAT) - Version 3.0 <https://www.w3.org/TR/vocab-dcat-3/>`_
 - `DCAT-AP profile <https://semiceu.github.io/DCAT-AP/releases/3.0.0/>`_


Publishing a new Version
########################

The project uses twine to publish to PyPi:

 - Update the version in ``setup.cfg``
 - Create a new release in Github.
 - Build the package: ``python -m build``
 - Upload to PyPi ``twine upload dist/*``
