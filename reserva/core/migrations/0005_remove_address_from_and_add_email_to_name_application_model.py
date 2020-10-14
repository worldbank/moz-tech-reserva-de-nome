# Generated by Django 3.1.2 on 2020-10-14 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_change_dob_label"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nameapplication",
            name="address1",
        ),
        migrations.RemoveField(
            model_name="nameapplication",
            name="address2",
        ),
        migrations.AddField(
            model_name="nameapplication",
            name="email",
            field=models.EmailField(
                default="no-reply@inage.gov.mz", max_length=254, verbose_name="E-mail"
            ),
            preserve_default=False,
        ),
    ]
