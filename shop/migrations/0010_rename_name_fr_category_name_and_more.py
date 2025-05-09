# Generated by Django 5.0.6 on 2025-03-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_category_description_remove_category_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name_fr',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description_fr',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='name_fr',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_fr',
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_nl',
            field=models.CharField(default='', max_length=120),
        ),
    ]
