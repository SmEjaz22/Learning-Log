# Generated by Django 5.1.1 on 2024-10-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_logs', '0010_alter_entry_date_added_alter_entry_last_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
