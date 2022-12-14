# Generated by Django 3.2 on 2022-12-12 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_name_category_plan_products'),
        ('customers', '0005_alter_length_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_code',
            field=models.CharField(default='4F8BF722', max_length=50),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('checked_out', models.BooleanField(default=False, verbose_name='checked out')),
                ('session_code', models.CharField(default='A73FE9A6', max_length=50)),
                ('product_plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cart_plan', to='products.planproducts')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'ordering': ('-creation_date',),
            },
        ),
    ]
