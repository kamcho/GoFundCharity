# Generated by Django 4.0.2 on 2023-04-01 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_project_expiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.TextField(max_length=100)),
                ('answer', models.TextField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('answered_on', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
