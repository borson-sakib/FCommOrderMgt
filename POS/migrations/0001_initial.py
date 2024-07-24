# Generated by Django 3.2.13 on 2024-07-08 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255)),
                ('product_category', models.CharField(max_length=255)),
                ('stocks', models.IntegerField(null=True)),
                ('product_cost', models.IntegerField(null=True)),
                ('product_description', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POS.category')),
            ],
        ),
    ]
