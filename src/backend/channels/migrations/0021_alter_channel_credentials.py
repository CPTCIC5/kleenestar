# Generated by Django 5.0.2 on 2024-05-25 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0020_remove_blocknote_note_note_blocknote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='credentials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channels.apicredentials'),
        ),
    ]