# Generated by Django 5.0.2 on 2024-04-25 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_alter_convo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='promptfeedback',
            name='category',
            field=models.CharField(default='xyz', max_length=60),
            preserve_default=False,
        ),
    ]