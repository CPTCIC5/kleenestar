# Generated by Django 5.0.2 on 2024-05-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0002_remove_workspace_challenges_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspaceinvite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
