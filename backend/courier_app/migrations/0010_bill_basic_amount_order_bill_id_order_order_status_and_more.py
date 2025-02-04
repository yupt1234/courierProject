# Generated by Django 4.1.10 on 2024-03-07 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courier_app', '0009_rename_east_rate_quotation_central_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='basic_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courier_app.bill'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Billed', 'Billed'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='reciept_upload',
            field=models.ImageField(blank=True, null=True, upload_to='paymentReciept/'),
        ),
        migrations.AddField(
            model_name='shipmentcharges',
            name='min_charge_weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='b2cquotation',
            name='weight',
            field=models.FloatField(default=5.5),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipped_throw',
            field=models.CharField(choices=[('AIR', 'AIR'), ('SURFACE', 'SURFACE'), ('PREMIUM', 'PREMIUM')], default='SURFACE', max_length=30),
        ),
    ]
