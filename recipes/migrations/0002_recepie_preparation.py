# Generated by Django 4.2.5 on 2023-09-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="preparation",
            field=models.TextField(blank=True),
        ),
    ]
