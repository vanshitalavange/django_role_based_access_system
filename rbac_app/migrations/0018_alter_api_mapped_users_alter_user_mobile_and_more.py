# Generated by Django 4.2.3 on 2023-08-03 10:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0017_alter_api_mapped_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="api",
            name="mapped_users",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(blank=True, null=True), size=None
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="mobile",
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
