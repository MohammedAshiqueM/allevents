# Generated by Django 5.2 on 2025-04-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artists',
            name='mbid',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
