# Generated by Django 5.0 on 2023-12-18 20:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dcat", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="catalog",
            old_name="license",
            new_name="licence",
        ),
        migrations.RenameField(
            model_name="distribution",
            old_name="license",
            new_name="licence",
        ),
    ]
