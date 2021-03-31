# Generated by Django 3.1 on 2020-09-14 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_failed_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата Рождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='failed_attempt',
            field=models.IntegerField(default=0),
        ),
    ]
