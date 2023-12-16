# Generated by Django 5.0 on 2023-12-16 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dcat", "0002_alter_agent_type_alter_distribution_file_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Checksum",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("checksum_value", models.CharField(max_length=255)),
                ("algorithm", models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name="distribution",
            name="checksum",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="dcat.checksum",
            ),
        ),
    ]