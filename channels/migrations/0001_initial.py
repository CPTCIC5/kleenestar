# Generated by Django 5.0.2 on 2024-07-04 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workspaces', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APICredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_1', models.CharField(blank=True, max_length=255, null=True)),
                ('key_2', models.CharField(blank=True, max_length=255, null=True)),
                ('key_3', models.CharField(blank=True, max_length=255, null=True)),
                ('key_4', models.CharField(blank=True, max_length=255, null=True)),
                ('key_5', models.CharField(blank=True, max_length=255, null=True)),
                ('key_6', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlockNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.subspace')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Convo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_id', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(default='New Chat', max_length=100)),
                ('archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.subspace')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KnowledgeBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subspace', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workspaces.subspace')),
                ('knowledge_source', models.ManyToManyField(blank=True, null=True, to='channels.knowledgesource')),
            ],
            options={
                'verbose_name_plural': 'KnowledgeBase',
                'ordering': ['subspace', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_query', models.TextField(max_length=10000)),
                ('file_query', models.FileField(blank=True, null=True, upload_to='Prompts-File/')),
                ('response_text', models.TextField(blank=True, max_length=10000, null=True)),
                ('response_file', models.FileField(blank=True, null=True, upload_to='Response-File/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('convo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.convo')),
            ],
            options={
                'ordering': ['author', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_text', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('color', models.CharField(choices=[('#90EE90', '#90EE90'), ('#FFCCCC', '#FFCCCC'), ('#D3D3D3', '#D3D3D3'), ('#E6E6FA', '#E6E6FA'), ('#ADD8E6', '#ADD8E6')], default='#ADD8E6', max_length=30)),
                ('blocknote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.blocknote')),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.prompt')),
            ],
        ),
        migrations.CreateModel(
            name='PromptFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(1, "Don't like the style"), (2, 'Not factually correct'), (3, 'Being Lazy'), (4, 'Other')])),
                ('note', models.TextField()),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.prompt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_type', models.IntegerField(choices=[(1, 'Google ads'), (2, 'Meta'), (3, 'X (Twitter)'), (4, 'Linkedin'), (5, 'TikTok'), (6, 'Reddit'), (7, 'Shopify'), (8, 'Google-Analytics'), (9, 'MailChimp'), (10, 'Instagram')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('credentials', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channels.apicredentials')),
                ('subspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.subspace')),
            ],
            options={
                'unique_together': {('subspace', 'channel_type')},
            },
        ),
    ]