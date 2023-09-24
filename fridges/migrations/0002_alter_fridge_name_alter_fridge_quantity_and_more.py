# Generated by Django 4.2.5 on 2023-09-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fridges", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fridge",
            name="name",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="fridge",
            name="quantity",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name="fridge",
            name="quantity_type",
            field=models.CharField(
                choices=[
                    ("kg", "kg"),
                    ("g", "g"),
                    ("l", "l"),
                    ("ml", "ml"),
                    ("szt.", "szt."),
                    ("opak.", "opak."),
                ],
                max_length=5,
                null=True,
            ),
        ),
    ]