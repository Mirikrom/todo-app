# Generated by Django 5.2.1 on 2025-05-16 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_rename_is_completed_todo_is_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='todo',
            name='category',
            field=models.ForeignKey(default=1111, on_delete=django.db.models.deletion.CASCADE, to='todo.category'),
            preserve_default=False,
        ),
    ]
