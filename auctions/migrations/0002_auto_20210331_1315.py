# Generated by Django 3.1.5 on 2021-03-31 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.CharField(max_length=400),
        ),
    ]