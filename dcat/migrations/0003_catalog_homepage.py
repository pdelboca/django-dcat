# Generated by Django 5.0 on 2023-12-20 22:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dcat", "0002_rename_license_catalog_licence_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="catalog",
            name="homepage",
            field=models.URLField(blank=True),
        ),
    ]
