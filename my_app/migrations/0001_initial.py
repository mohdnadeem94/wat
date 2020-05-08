# Generated by Django 3.0.5 on 2020-05-08 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=500)),
                ('created', models.DateTimeField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Searches',
            },
        ),
    ]
