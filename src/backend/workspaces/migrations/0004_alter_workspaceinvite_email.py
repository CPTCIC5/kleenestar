# Generated by Django 5.0.2 on 2024-05-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0003_alter_workspaceinvite_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspaceinvite',
            name='email',
            field=models.EmailField(default='xyz@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]