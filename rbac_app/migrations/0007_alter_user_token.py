# Generated by Django 4.2.3 on 2023-07-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0006_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="token",
            field=models.JSONField(max_length=350, null=True),
        ),
    ]
