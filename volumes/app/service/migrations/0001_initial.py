# Generated by Django 4.1.5 on 2023-04-19 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نوع سرویس')),
            ],
            options={
                'verbose_name': 'نوع سرویس',
                'verbose_name_plural': 'نوع سرویس ها',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_type', models.CharField(choices=[('instagram_profile', 'Instagram Profile(ID)'), ('instagram_post_link', 'Instagram Post Link')], max_length=20, verbose_name='نوع لینک')),
                ('server', models.CharField(choices=[('parsifollower', 'Parsifollower'), ('mifa', 'Mifa')], max_length=20, verbose_name='سرور')),
                ('server_service_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد سرویس متناظر')),
                ('service_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد سرویس')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان')),
                ('amount', models.CharField(blank=True, max_length=10, null=True, verbose_name='قیمت به ازای هر ۱ عدد')),
                ('min_order', models.CharField(blank=True, max_length=10, null=True, verbose_name='حداقل سفارش')),
                ('max_order', models.CharField(blank=True, max_length=10, null=True, verbose_name='حداکثر سفارش')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('available_for_user', models.BooleanField(default=True, verbose_name='فعال برای کاربر')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='service.servicetype', verbose_name='نوع سرویس')),
            ],
            options={
                'verbose_name': 'سرویس',
                'verbose_name_plural': 'سرویس ها',
            },
        ),
    ]
