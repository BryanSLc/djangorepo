# Generated by Django 5.0.6 on 2024-07-08 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_comentarioforo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarioforo',
            name='titulo',
            field=models.CharField(default='Sin titulo', max_length=200),
            preserve_default=False,
        ),
    ]