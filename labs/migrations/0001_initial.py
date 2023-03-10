# Generated by Django 4.1.3 on 2023-01-14 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('title', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('description_input', models.CharField(max_length=1000)),
                ('description_output', models.CharField(max_length=1000)),
                ('expected_output', models.CharField(max_length=1000)),
                ('laboratory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.laboratory')),
            ],
        ),
        migrations.CreateModel(
            name='LaboratoryInLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('laboratory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.laboratory')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.language')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.testcase')),
            ],
        ),
    ]
