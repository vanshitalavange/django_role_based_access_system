# Generated by Django 4.2.3 on 2023-07-27 09:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0004_rename_user_id_token_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="token",
            name="user",
        ),
        migrations.DeleteModel(
            name="API",
        ),
        migrations.DeleteModel(
            name="Token",
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
