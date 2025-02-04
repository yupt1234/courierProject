# Generated by Django 4.1.10 on 2024-03-05 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier_app', '0008_b2czone_customer_cod_to_pay_charge_customer_docket_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='east_rate',
            new_name='central_rate',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='north_rate',
            new_name='e_rate',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='south_rate',
            new_name='n1_rate',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='special_dest_rate',
            new_name='n2_rate',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='west_rate',
            new_name='ne_rate',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='within_zone_rate',
            new_name='s1_rate',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='cod_to_pay_charge',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='docket',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='fov',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='fsc',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='min_cod_to_pay_charge',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='min_fov',
        ),
        migrations.AddField(
            model_name='b2cquotation',
            name='metro_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='s2_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='w1_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='w2_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='b2cquotation',
            name='from_zone',
            field=models.CharField(choices=[('SPECIAL DESTINATION', 'SPECIAL DESTINATION'), ('WITHIN ZONE', 'WITHIN ZONE'), ('REST OF INDIA', 'REST OF INDIA'), ('METRO', 'METRO'), ('WITHIN CITY', 'WITHIN CITY')], default='WITHIN ZONE', max_length=30),
        ),
        migrations.AlterField(
            model_name='b2czone',
            name='zone',
            field=models.CharField(choices=[('SPECIAL DESTINATION', 'SPECIAL DESTINATION'), ('WITHIN ZONE', 'WITHIN ZONE'), ('REST OF INDIA', 'REST OF INDIA'), ('METRO', 'METRO'), ('WITHIN CITY', 'WITHIN CITY')], default='WITHIN ZONE', max_length=30),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='from_zone',
            field=models.CharField(choices=[('CENTRAL', 'CENTRAL'), ('N1', 'N1'), ('N2', 'N2'), ('S1', 'S1'), ('S2', 'S2'), ('E', 'E'), ('NE', 'NE'), ('W1', 'W1'), ('W2', 'W2')], default='CENTRAL', max_length=30),
        ),
        migrations.AlterField(
            model_name='zone',
            name='zone',
            field=models.CharField(choices=[('CENTRAL', 'CENTRAL'), ('N1', 'N1'), ('N2', 'N2'), ('S1', 'S1'), ('S2', 'S2'), ('E', 'E'), ('NE', 'NE'), ('W1', 'W1'), ('W2', 'W2')], default='CENTRAL', max_length=30),
        ),
    ]
