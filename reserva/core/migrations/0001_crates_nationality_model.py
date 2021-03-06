# Generated by Django 3.1.1 on 2020-09-28 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Nationality",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="Nacionalidade")),
            ],
            options={
                "verbose_name": "nacionalidade",
                "ordering": ("name",),
            },
        ),
        migrations.AddIndex(
            model_name="nationality",
            index=models.Index(fields=["name"], name="core_nation_name_f32613_idx"),
        ),
    ]
