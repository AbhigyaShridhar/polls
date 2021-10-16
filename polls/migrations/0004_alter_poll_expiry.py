# Generated by Django 3.2.3 on 2021-10-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20211016_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expiry',
            field=models.DateTimeField(help_text='Format: YYYY-MM-DD HOURS:MINUTES:SECONDS, example - 2021-10-16 19:30:51'),
        ),
    ]