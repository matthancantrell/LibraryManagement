# Generated by Django 5.0.1 on 2024-02-01 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_rename_title_book_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='library',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='management.library'),
            preserve_default=False,
        ),
    ]
