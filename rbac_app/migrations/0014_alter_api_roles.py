# Generated by Django 4.2.3 on 2023-08-01 10:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0013_alter_api_roles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="api",
            name="roles",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), size=None
            ),
        ),
    ]