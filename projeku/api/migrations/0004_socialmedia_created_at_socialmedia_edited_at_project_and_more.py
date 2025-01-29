# Generated by Django 5.1.5 on 2025-01-27 09:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_socialmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialmedia',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=225)),
                ('file_url', models.CharField(max_length=225)),
                ('image_url', models.CharField(max_length=225)),
                ('views', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('id_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='id_user')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='id_user')),
                ('id_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project', verbose_name='id_project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('id_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user', verbose_name='id_user')),
                ('id_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project', verbose_name='id_project')),
            ],
        ),
    ]
