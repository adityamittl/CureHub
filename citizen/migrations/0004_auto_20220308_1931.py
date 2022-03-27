# Generated by Django 3.1.6 on 2022-03-08 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0003_auto_20220308_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosis_center',
            name='available_tests',
        ),
        migrations.AddField(
            model_name='diagnosis_center',
            name='available_tests',
            field=models.ManyToManyField(to='citizen.tests'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='Diagnosis_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citizen.diagnosis'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='bill_breakdown',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citizen.bill'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='claimed_ammount',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='meds',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citizen.prescription'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='meds_duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='need_diagnosis',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='next_followup',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='required_tests',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citizen.tests'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='viewed_report',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]