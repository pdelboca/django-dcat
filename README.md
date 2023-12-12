
# DCAT

django-dcat is a Django app that provides a model layer for DCAT 3.0 metadata and
some command line tools to import data to it from different vocabularies.

## Quick start

1. Add "dcat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "dcat",
    ]

2. Run ``python manage.py migrate`` to create the DCAT models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to start adding data (you'll need the Admin app enabled).

4. Run ``python manage.py --help`` to see the available commands.

## Implementation notes
The Django models in this package are inspired by the diagram presented in DCAT profiles. For example:

![UML diagram illustrating the DCAT-AP specification](https://semiceu.github.io/DCAT-AP/releases/3.0.0/html/overview.jpg)

For more information on DCAT:

 - [Data Catalog Vocabulary (DCAT) - Version 3.0](https://www.w3.org/TR/vocab-dcat-3/)
 - [DCAT-AP profile](https://semiceu.github.io/DCAT-AP/releases/3.0.0/)
