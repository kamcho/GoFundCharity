# Generated by Django 4.0.2 on 2023-04-08 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_alter_stripecardpayments_amount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mails',
        ),
        migrations.RemoveField(
            model_name='stripecardpayments',
            name='user',
        ),
        migrations.DeleteModel(
            name='Quizes',
        ),
        migrations.DeleteModel(
            name='StripeCardPayments',
        ),
    ]