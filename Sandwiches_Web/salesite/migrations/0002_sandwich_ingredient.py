# Generated by Django 3.2.5 on 2021-08-02 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sandwich',
            name='ingredient',
            field=models.ManyToManyField(to='salesite.Ingredient'),
        ),
    ]