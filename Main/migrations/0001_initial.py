# Generated by Django 2.2.6 on 2019-10-18 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdTable',
            fields=[
                ('uuid', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('id', models.IntegerField()),
            ],
        ),
    ]
