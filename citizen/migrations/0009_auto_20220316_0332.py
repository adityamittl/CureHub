# Generated by Django 3.1.6 on 2022-03-15 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0008_auto_20220316_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
