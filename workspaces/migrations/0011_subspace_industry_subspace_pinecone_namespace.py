# Generated by Django 5.0.2 on 2024-06-25 05:26

import workspaces.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0010_subspace'),
    ]

    operations = [
        migrations.AddField(
            model_name='subspace',
            name='industry',
            field=models.CharField(choices=[('\u2060Retail', '\u2060Retail'), ('\u2060Hospitality', '\u2060Hospitality'), ('\u2060Media', '\u2060Media'), ('\u2060Technology', '\u2060Technology'), ('\u2060Finance', '\u2060Finance'), ('\u2060Sport', '\u2060Sport'), ('\u2060Beauty', '\u2060Beauty'), ('\u2060Automotive', '\u2060Automotive')], default=1, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subspace',
            name='pinecone_namespace',
            field=models.CharField(default=workspaces.models.create_namespace_id, max_length=11),
        ),
    ]