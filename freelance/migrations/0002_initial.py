# Generated by Django 5.0.4 on 2024-06-17 05:06

import django.db.models.deletion
import django.utils.timezone
import freelance.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('freelance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='position')),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'positions',
                'db_table': '"freelance"."position"',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='status')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
                'db_table': '"freelance"."status"',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='developer')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='freelance.position', verbose_name='position')),
            ],
            options={
                'verbose_name': 'developer',
                'verbose_name_plural': 'developers',
                'db_table': '"freelance"."developer"',
                'ordering': ['developer', 'position'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, validators=[freelance.models.time_traveler_trap], verbose_name='creation time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='freelance.status', verbose_name='status')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'db_table': '"freelance"."task"',
                'ordering': ['name', 'status'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment_content', models.TextField(blank=True, verbose_name='content')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='publication time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelance.developer', verbose_name='owner')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='freelance.task', verbose_name='task')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comment',
                'db_table': '"freelance"."comment"',
                'ordering': ['publication_date'],
            },
        ),
        migrations.CreateModel(
            name='TaskDeveloper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelance.developer', verbose_name='developer')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelance.task', verbose_name='task')),
            ],
            options={
                'verbose_name': 'relationship task developer',
                'verbose_name_plural': 'relationships task developer',
                'db_table': '"freelance"."task_developer"',
                'unique_together': {('task', 'developer')},
            },
        ),
        migrations.AddField(
            model_name='task',
            name='developers',
            field=models.ManyToManyField(through='freelance.TaskDeveloper', to='freelance.developer', verbose_name='developers'),
        ),
        migrations.AddField(
            model_name='developer',
            name='tasks',
            field=models.ManyToManyField(through='freelance.TaskDeveloper', to='freelance.task', verbose_name='tasks'),
        ),
        migrations.AddConstraint(
            model_name='developer',
            constraint=models.UniqueConstraint(fields=('developer',), name='developer_unique'),
        ),
    ]
