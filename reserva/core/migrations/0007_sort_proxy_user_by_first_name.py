# Generated by Django 3.1.2 on 2020-10-15 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_creates_proxy_user_model"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("first_name", "last_name", "username")},
        ),
    ]