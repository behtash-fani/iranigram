# Generated by Django 4.1.5 on 2023-03-28 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
    ]
