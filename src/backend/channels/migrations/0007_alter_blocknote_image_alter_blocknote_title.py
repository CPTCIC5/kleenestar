# Generated by Django 5.0.2 on 2024-04-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0006_blocknote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blocknote',
            name='image',
            field=models.ImageField(blank=True, upload_to='BlockNote'),
        ),
        migrations.AlterField(
            model_name='blocknote',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]