# Generated by Django 5.0.2 on 2024-05-24 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0016_remove_prompt_blocknote_prompt_blocknote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicredentials',
            name='key_1',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='blocknote',
            field=models.ManyToManyField(blank=True, null=True, to='channels.blocknote'),
        ),
    ]