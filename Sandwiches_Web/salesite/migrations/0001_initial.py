# Generated by Django 3.2.5 on 2021-08-01 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_descripcion', models.CharField(max_length=100)),
                ('ingredient_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_total', models.FloatField()),
                ('order_date', models.DateField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesite.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Sandwich_Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_descripcion', models.CharField(max_length=100)),
                ('size_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sandwich',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sandwich_price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesite.order')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesite.sandwich_size')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient_Sandwich',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesite.ingredient')),
                ('sandwich', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesite.sandwich')),
            ],
        ),
    ]