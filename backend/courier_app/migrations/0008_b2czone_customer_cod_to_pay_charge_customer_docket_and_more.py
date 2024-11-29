# Generated by Django 4.1.10 on 2024-03-02 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courier_app', '0007_quotation_setting_zone_order_basic_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='B2CZone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('zone', models.CharField(choices=[('SPECIAL DESTINATION', 'SPECIAL DESTINATION'), ('WITHIN ZONE', 'WITHIN ZONE'), ('REST OF INDIA', 'REST OF INDIA')], default='WITHIN ZONE', max_length=30)),
                ('state', models.CharField(default='', max_length=30)),
                ('date_created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='cod_to_pay_charge',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='docket',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='fov',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='fsc',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='min_cod_to_pay_charge',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customer',
            name='min_fov',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='from_city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_bill_generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='shipped_throw',
            field=models.CharField(choices=[('AIR', 'AIR'), ('SURFACE', 'SURFACE'), ('PREMIUM', 'PREMIUM')], default='BY SURFACE', max_length=30),
        ),
        migrations.AddField(
            model_name='quotation',
            name='service_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ft_service_provider', to='courier_app.serviceprovider'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='serviceByImg/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipment_status',
            field=models.CharField(choices=[('IN TRANSIT', 'IN TRANSIT'), ('DELIVERED', 'DELIVERED'), ('RTO IN TRANSIT', 'RTO IN TRANSIT'), ('RTO DELIVERED', 'RTO DELIVERED')], default='IN TRANSIT', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='ShipmentCharges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_mode', models.CharField(choices=[('B2B', 'B2B'), ('B2C', 'B2C')], default='B2C', max_length=10)),
                ('fsc', models.FloatField(default=0.0)),
                ('min_fov', models.FloatField(default=0.0)),
                ('fov', models.FloatField(default=0.0)),
                ('docket', models.FloatField(default=0.0)),
                ('min_cod_to_pay_charge', models.FloatField(default=0.0)),
                ('cod_to_pay_charge', models.FloatField(default=0.0)),
                ('date_created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courier_app.customer')),
                ('service_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courier_app.serviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='B2CQuotation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('deliver_mode', models.CharField(choices=[('AIR', 'AIR'), ('SURFACE', 'SURFACE'), ('PREMIUM', 'PREMIUM')], default='SURFACE', max_length=50)),
                ('from_zone', models.CharField(choices=[('SPECIAL DESTINATION', 'SPECIAL DESTINATION'), ('WITHIN ZONE', 'WITHIN ZONE'), ('REST OF INDIA', 'REST OF INDIA')], default='WITHIN ZONE', max_length=30)),
                ('weight', models.FloatField(default=5500.0)),
                ('min_weight', models.FloatField(default=0.0)),
                ('within_city_rate', models.FloatField(blank=True, null=True)),
                ('within_zone_rate', models.FloatField(blank=True, null=True)),
                ('rest_india_rate', models.FloatField(blank=True, null=True)),
                ('special_destination_rate', models.FloatField(blank=True, null=True)),
                ('date_create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer_id', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bq_customer', to='courier_app.customer')),
                ('service_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='bq_serviceby', to='courier_app.serviceprovider')),
            ],
        ),
    ]
