# Generated by Django 5.0.6 on 2025-03-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_rename_name_fr_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_nl',
            field=models.TextField(default=''),
        ),
    ]
