
# DCAT

django-dcat is a Django app that provides a model layer for DCAT 3.0 metadata and
some command line tools to import data to it from different vocabularies.

## Quick start

1. Add `dcat` to your `INSTALLED_APPS` setting like this:
```
    INSTALLED_APPS = [
        ...,
        "dcat",
    ]
```
2. Run ``python manage.py migrate`` to create the DCAT models in your database.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to start adding data (you'll need the Admin app enabled).

4. Run ``python manage.py --help`` to see the available commands.

## CLI utilities

#### Migrating from CKAN

`django-dcat` provides two command lines that allows to:
 1) Make a dump of data from a CKAN data portal (that has [ckanext-datajson](https://github.com/GSA/ckanext-datajson) installed)
 2) Create a Catalog with its related entities (datasets, distributions, etc)

 ```
 # Download the data.json file from the portal
 $ wget -o data.json https://www.ckan-example.org/data.json

 # Download all files from the portal (by default in a data/ folder)
 $ python manage.py dump_from_datajson

 # Import all data and files into a local catalog
 $ python manage.py import_from_datajson
 ```

#### Controlled vocabularies for standardise metadata

Commands to import controlled vocabularies used in the EU Open Data Portal in order to standardise the metadata.

```
# Populate records for the MediaType model (CSV, PDF, etc)
$ python manage.py import_filetypes

# Populate records for Licences (MIT, Apache, etc)
$ python manage.py import_licences
```

The goal of these commands is to provide data publishers with pre-filled options for the metadata fields. This will improve
data quality and avoid common problems like duplicated metadata values for typos or inconsistent data entry (like distributions with
`.csv`, `.CSV`, `CSV`, etc)

## Implementation notes
The Django models in this package are inspired by the diagram presented in DCAT profiles. For example:

![UML diagram illustrating the DCAT-AP specification](https://semiceu.github.io/DCAT-AP/releases/3.0.0/html/overview.jpg)

For more information on DCAT:

 - [Data Catalog Vocabulary (DCAT) - Version 3.0](https://www.w3.org/TR/vocab-dcat-3/)
 - [DCAT-AP profile](https://semiceu.github.io/DCAT-AP/releases/3.0.0/)
