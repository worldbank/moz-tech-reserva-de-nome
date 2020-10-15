# Generated by Django 3.1.2 on 2020-10-15 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "core",
            "0009_migrate_data_from_approved_to_status_field_in_name_application_model",
        ),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="nameapplication",
            name="core_nameap_approve_6f8295_idx",
        ),
        migrations.RemoveIndex(
            model_name="nameapplication",
            name="core_nameap_approve_dc8387_idx",
        ),
        migrations.RemoveField(
            model_name="nameapplication",
            name="approved",
        ),
        migrations.RemoveField(
            model_name="nameapplication",
            name="approved_by",
        ),
        migrations.AddField(
            model_name="nameapplication",
            name="moderated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.user",
                verbose_name="Moderado por",
            ),
        ),
        migrations.AddIndex(
            model_name="nameapplication",
            index=models.Index(
                fields=["moderated_by"], name="core_nameap_moderat_1b2594_idx"
            ),
        ),
    ]
