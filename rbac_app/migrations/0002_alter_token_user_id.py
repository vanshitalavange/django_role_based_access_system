# Generated by Django 4.2.3 on 2023-07-27 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="user_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="rbac_app.user"
            ),
        ),
    ]
