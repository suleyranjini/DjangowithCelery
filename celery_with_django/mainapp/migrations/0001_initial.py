# Generated by Django 4.0.1 on 2022-01-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oper', models.CharField(choices=[('SUM', 'sum'), ('DIFF', 'diff'), ('MULT', 'mult'), ('DIV', 'div')], max_length=5)),
                ('input1', models.IntegerField()),
                ('input2', models.IntegerField()),
                ('output', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('SUCCESS', 'Success')], max_length=8)),
                ('message', models.CharField(blank=True, max_length=110)),
            ],
        ),
    ]
