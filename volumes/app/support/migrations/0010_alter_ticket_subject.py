# Generated by Django 4.1.5 on 2023-04-07 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_alter_ticket_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.CharField(max_length=50, verbose_name='Subject'),
        ),
    ]
