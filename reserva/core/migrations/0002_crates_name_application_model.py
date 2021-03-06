# Generated by Django 3.1.1 on 2020-09-28 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_crates_nationality_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="NameApplication",
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
                (
                    "name",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="Nome da empresa"
                    ),
                ),
                (
                    "applicant",
                    models.CharField(max_length=256, verbose_name="Responsável"),
                ),
                ("dob", models.DateField(verbose_name="Data de nascimento")),
                (
                    "address1",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Endereço (linha 1)",
                    ),
                ),
                (
                    "address2",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Endereço (linha 2)",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Alterado em"),
                ),
                (
                    "nationality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.nationality",
                        verbose_name="Nacionalidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "pedido de reserva de nome",
                "verbose_name_plural": "pedidos de reserva de nome",
                "ordering": ("-created_at", "name"),
            },
        ),
        migrations.AddIndex(
            model_name="nameapplication",
            index=models.Index(
                fields=["created_at"], name="core_nameap_created_b392e3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="nameapplication",
            index=models.Index(
                fields=["updated_at"], name="core_nameap_updated_50ec12_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="nameapplication",
            index=models.Index(fields=["name"], name="core_nameap_name_fc18c5_idx"),
        ),
    ]
