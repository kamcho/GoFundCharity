# Generated by Django 4.0.2 on 2023-03-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='expiry',
            field=models.CharField(max_length=100),
        ),
    ]
