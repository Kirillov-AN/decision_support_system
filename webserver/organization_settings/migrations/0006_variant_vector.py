# Generated by Django 5.1.4 on 2025-02-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization_settings", "0005_model_parameters"),
    ]

    operations = [
        migrations.AddField(
            model_name="variant",
            name="vector",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
