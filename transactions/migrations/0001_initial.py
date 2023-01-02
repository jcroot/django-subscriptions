# Generated by Django 3.2 on 2022-12-19 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0008_alter_code_session_and_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('currency', models.CharField(max_length=4)),
                ('number_of_payments', models.IntegerField(default=1)),
                ('additional_data', models.CharField(blank=True, max_length=100, null=True)),
                ('preauthorization', models.CharField(default='S', max_length=2)),
                ('response', models.CharField(blank=True, max_length=2, null=True)),
                ('response_details', models.CharField(blank=True, max_length=50, null=True)),
                ('authorization_number', models.CharField(blank=True, max_length=50, null=True)),
                ('ticket_number', models.CharField(blank=True, max_length=50, null=True)),
                ('iva_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('iva_ticket_number', models.CharField(blank=True, max_length=50, null=True)),
                ('response_code', models.CharField(blank=True, max_length=50, null=True)),
                ('response_description', models.CharField(blank=True, max_length=50, null=True)),
                ('security_information', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customers.orders')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
