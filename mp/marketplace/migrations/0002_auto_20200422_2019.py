# Generated by Django 3.0.5 on 2020-04-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='seller_id',
        ),
        migrations.RemoveField(
            model_name='image',
            name='image_address',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory_id',
        ),
        migrations.AddField(
            model_name='image',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marketplace.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=1023),
        ),
        migrations.AlterField(
            model_name='product',
            name='expose_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='reason_dev',
            field=models.TextField(max_length=1023),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]
