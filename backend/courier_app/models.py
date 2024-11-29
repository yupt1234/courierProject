from typing import Iterable
from django.db import models
from datetime import datetime

# Create your models here.

"""
Model for service provider store
"""
class ServiceProvider(models.Model) :
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    website_link = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to='serviceByImg/', null=True, blank=True)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

"""
Model for store customer record
"""
class Customer(models.Model) :
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, blank=True, null=True)
    gst_no = models.CharField(max_length=15, default="")
    # fsc = models.FloatField(default=0.0)
    # min_fov = models.FloatField(default=0.0)
    # fov = models.FloatField(default=0.0)
    # docket = models.FloatField(default=0.0)
    # min_cod_to_pay_charge = models.FloatField(default=0.0)
    # cod_to_pay_charge = models.FloatField(default=0.0)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.company_name
    
ZONES = (
    ('CENTRAL', 'CENTRAL'),
    ('N1', 'N1'),
    ('N2', 'N2'),
    ('S1', 'S1'),
    ('S2', 'S2'),
    ('E', 'E'),
    ('NE', 'NE'),
    ('W1', 'W1'),
    ('W2', 'W2'),
)
"""
Table for Store the Ledger data
"""
class Zone(models.Model) :
    id = models.AutoField(primary_key=True)
    zone = models.CharField(choices=ZONES, max_length=30, default="CENTRAL")
    state = models.CharField(default="", max_length=30)
    date_created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.state
    

B2CZONES = (
    ('SPECIAL DESTINATION', 'SPECIAL DESTINATION'),
    ('WITHIN ZONE', 'WITHIN ZONE'),
    ('REST OF INDIA', 'REST OF INDIA'),
    ('METRO', 'METRO'),
    ('WITHIN CITY', 'WITHIN CITY'),
)
"""
Table for Store the b2c zone data
"""
class B2CZone(models.Model) :
    id = models.AutoField(primary_key=True)
    zone = models.CharField(choices=B2CZONES, max_length=30, default="WITHIN ZONE")
    state = models.CharField(default="", max_length=30)
    # within_zone = models.CharField(max_length = 50)
    # special_destination = models.CharField(max_length = 50)
    date_created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.zone
    

WEIGHT = (
    (250, '250'),
    (500, '500'),
    (1000, '1000'),
    (1500, '1500'),
    (2000, '2000'),
    (2500, '2500'),
    (3000, '3000'),
    (3500, '3500'),
    (4000, '4000'),
    (4500, '4500'),
    (5000, '5000'),
    ('Per Kg', 'Per Kg')
)
DELIVER_MODE_CHOICES = (
    ('AIR', 'AIR'),
    ('SURFACE', 'SURFACE'),
    ('PREMIUM', 'PREMIUM')
)
"""
Model for store rate for b2c 
"""
class B2CQuotation(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, default="",blank=True,  null=True, related_name="bq_customer", on_delete=models.CASCADE)
    service_by = models.ForeignKey(ServiceProvider, default="", related_name="bq_serviceby", on_delete=models.CASCADE)
    deliver_mode = models.CharField(choices=DELIVER_MODE_CHOICES, max_length=50, default="SURFACE")
    from_zone = models.CharField(choices=B2CZONES, max_length=30, default="WITHIN ZONE")
    weight = models.FloatField(default=5.5)
    min_weight= models.FloatField(default=0.0)
    within_city_rate = models.FloatField(null=True, blank=True)
    within_zone_rate = models.FloatField(null=True, blank=True)
    rest_india_rate = models.FloatField(null=True, blank=True)
    metro_rate = models.FloatField(null=True, blank=True)
    special_destination_rate = models.FloatField(null=True, blank=True)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kargs):
        if self.weight == 0.25 :
            self.min_weight = 0.0
        elif self.weight == 0.5 :
            self.min_weight = 0.25
        elif self.weight == 1.0 :
            self.min_weight = 0.5
        elif self.weight == 1.5 :
            self.min_weight = 1.0
        elif self.weight == 2.0 :
            self.min_weight = 1.5
        elif self.weight == 2.5 :
            self.min_weight = 2.0
        elif self.weight == 3.0 :
            self.min_weight = 2.5
        elif self.weight == 3.5 :
            self.min_weight = 3.0
        elif self.weight == 4.0 :
            self.min_weight = 3.5
        elif self.weight == 4.5 :
            self.min_weight = 4.0
        elif self.weight == 5.0 :
            self.min_weight = 4.5
        elif self.weight > 5.0 :
            self.min_weight = 5.0
        return super().save(*args, **kargs)

    def __str__(self):
        return f"{self.customer_id.company_name}, {self.weight}"
    

"""
Model for store rate of frieght according to service provider
"""
class Quotation(models.Model) :
    id = models.AutoField(primary_key=True)
    service_by = models.ForeignKey(ServiceProvider, null=True, related_name="ft_service_provider", on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, default="",blank=True,  null=True, related_name="ft_customer", on_delete=models.CASCADE)
    from_zone = models.CharField(choices=ZONES, max_length=30, default="CENTRAL")
    n1_rate = models.FloatField(null=True, blank=True)
    n2_rate = models.FloatField(null=True, blank=True)
    s1_rate = models.FloatField(null=True, blank=True)
    s2_rate = models.FloatField(null=True, blank=True)
    e_rate = models.FloatField(null=True, blank=True)
    ne_rate = models.FloatField(null=True, blank=True)
    w1_rate = models.FloatField(null=True, blank=True)
    w2_rate = models.FloatField(null=True, blank=True)
    # special_dest_rate = models.FloatField(null=True, blank=True)
    # within_zone_rate = models.FloatField(null=True, blank=True)
    central_rate = models.FloatField(null=True, blank=True)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.customer_id.company_name}, {self.from_zone}"


"""
Table for storing a payment detail
"""
PAY_MODE = (
    ('BANK', 'BANK'),
    ('CASH', 'CASH'),
    ('UPI', 'UPI'),
)
class Payment(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, related_name="customer_payment", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    payment_mode = models.CharField(choices=PAY_MODE, default="BANK", max_length=10)
    amount = models.FloatField(default=0.0)
    reciept_upload = models.ImageField(upload_to='paymentReciept/', null=True, blank=True)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def delete(self, *args, **kwargs):
        # Set order_status to "Pending" before deleting the object
        orderList = Order.objects.filter(bill_id__payment_id=self.id)
        print(orderList, "orderList")
        orderList.update(order_status="Pending")
        super().delete(*args, **kwargs)


"""
Table for storing a COD payment detail
"""
class CodPayment(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, related_name="customer_cod_payment", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True, null=True)
    payment_mode = models.CharField(choices=PAY_MODE, default="BANK", max_length=10)
    amount = models.FloatField(default=0.0)
    reciept_upload = models.ImageField(upload_to='codPaymentReciept/', null=True, blank=True)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)


"""
TABLE TO STORE THE GENRATED BILL DETAIL
"""
class Bill(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_orders = models.IntegerField(default=0)
    no_of_b2b = models.IntegerField(default=0)
    no_of_b2c = models.IntegerField(default=0)
    basic_amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    bill_amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    balance_amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    is_paid = models.BooleanField(default=False)
    payment_id = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)


"""
TABLE TO STORE THE GENRATED BILL and PAYMENT DETAIL
"""
class BillPayment(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    bill_id = models.ForeignKey(Bill, null=True, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    date = models.DateTimeField(auto_now_add=True, null=True)


"""
Model for store all order details
"""
ORDER_TYPE = (
    ('CREDIT', 'CREDIT'),
    ('CASH', 'CASH'),
)
ORDER_MODE = (
    ('B2B', 'B2B'),
    ('B2C', 'B2C'),
)
PAYMENT_MODE = (
    ('PREPAID', 'PREPAID'),
    ('COD', 'COD'),
    ('TO PAY', 'TO PAY'),
)
SHIPMENT_STATUS = (
    ('IN TRANSIT', 'IN TRANSIT'),
    ('DELIVERED', 'DELIVERED'),
    ('RTO IN TRANSIT', 'RTO IN TRANSIT'),
    ('RTO DELIVERED', 'RTO DELIVERED'),
)
ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Billed', 'Billed'),
    ('Completed', 'Completed')
)
COD_STATUS = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid')
)
# DELIVER_MODE_CHOICES = (
#     ('BY AIR', 'BY AIR'),
#     ('BY SURFACE', 'BY SURFACE'),
#     ('PREMIUM SERVICE', 'PREMIUM SERVICE')
# )
class Order(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, related_name="o_customer", default="", on_delete=models.CASCADE)
    order_type = models.CharField(choices=ORDER_TYPE, default="CREDIT", max_length=20)
    order_mode = models.CharField(choices=ORDER_MODE, default="B2C", max_length=10)
    service_by = models.ForeignKey(ServiceProvider, default="", related_name="o_service_provider", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    shipment_date = models.DateTimeField(null=True, blank=True)
    invoice_value = models.FloatField(default=0.0)
    cod_value = models.FloatField(default=0.0)
    payment_mode = models.CharField(choices=PAYMENT_MODE, default="PREPAID", max_length=20)
    awb_no = models.CharField(max_length=20, null=True, blank=True)
    from_city = models.CharField(max_length=30, null=True, blank=True)
    from_state = models.CharField(max_length=30, null=True, blank=True)
    shipped_to_name = models.CharField(max_length=50, null=True, blank=True)
    shipped_to_phone = models.CharField(max_length=10, null=True, blank=True)
    shipped_to_city = models.CharField(max_length=30, null=True, blank=True)
    shipped_to_state = models.CharField(max_length=30, null=True, blank=True)
    shipment_status = models.CharField(choices=SHIPMENT_STATUS, default="IN TRANSIT", max_length=20)
    shipped_throw = models.CharField(choices=DELIVER_MODE_CHOICES, default="SURFACE", max_length=30)
    no_of_box = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(default=1.0, null=True, blank=True)
    apply_weight = models.FloatField(null=True, blank=True)
    charged_weight = models.FloatField(null=True, blank=True)
    basic_amount = models.FloatField(default=0.0)
    freight_amount = models.FloatField(default=0.0)
    mannual_frieght = models.FloatField(default=0.0)
    remark = models.TextField(max_length=255, null=True, blank=True)
    receipt_upload = models.ImageField(upload_to='orderReciept/', null=True, blank=True)
    # balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # is_paid = models.BooleanField(default=False)
    is_bill_generated = models.BooleanField(default=False)
    bill_id = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.SET_NULL)
    order_status = models.CharField(choices=ORDER_STATUS, default="Pending", max_length=20)

    cod_payment_id = models.ForeignKey(CodPayment, null=True, blank=True, on_delete=models.SET_NULL)
    cod_status = models.CharField(choices=COD_STATUS, default="Pending", max_length=20)
    balance_cod_amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)

    date_create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.customer_id.customer_name
    

"""
TABLE TO STORE THE ORDER and COD PAYMENT DETAIL
"""
class OrderCodPayment(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order_id = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    cod_payment_id = models.ForeignKey(CodPayment, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    date = models.DateTimeField(auto_now_add=True, null=True)


PAY_MODE = (
    ('CASH', 'CASH'),
    ('BANK', 'BANK'),
    ('UPI', 'UPI')
)
class CashBooking(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(default='', max_length=50)
    counter = models.CharField(default="", max_length=50)
    order_mode = models.CharField(choices=ORDER_MODE, default="B2C", max_length=10)
    deliver_mode = models.CharField(choices=DELIVER_MODE_CHOICES, default="SURFACE", max_length=30)
    service_by = models.ForeignKey(ServiceProvider, default="", related_name="cash_service_provider", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    shipment_date = models.DateTimeField(null=True, blank=True)
    invoice_value = models.FloatField(default=0.0)
    cod_value = models.FloatField(default=0.0)
    payment_mode = models.CharField(choices=PAYMENT_MODE, default="PREPAID", max_length=20)
    awb_no = models.CharField(max_length=20, null=True, blank=True)
    origin_city = models.CharField(max_length=30, null=True, blank=True)
    origin_state = models.CharField(max_length=30, null=True, blank=True)
    consignee = models.CharField(max_length=50, null=True, blank=True)
    consignee_phone = models.CharField(max_length=10, null=True, blank=True)
    destination_city = models.CharField(max_length=30, null=True, blank=True)
    destination_state = models.CharField(max_length=30, null=True, blank=True)
    shipment_status = models.CharField(choices=SHIPMENT_STATUS, default="IN TRANSIT", max_length=20)
    no_of_box = models.IntegerField(null=True, blank=True)
    charged_weight = models.FloatField(null=True, blank=True)
    freight_amount = models.FloatField(default=0.0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remark = models.TextField(max_length=255, null=True, blank=True)
    receipt_upload = models.ImageField(upload_to='orderReciept/', null=True, blank=True)
    mode = models.CharField(choices=PAY_MODE, default="CASH", max_length=20)
    # is_paid = models.BooleanField(default=False)
    is_bill_generated = models.BooleanField(default=False)
    bill_id = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.SET_NULL)
    order_status = models.CharField(choices=ORDER_STATUS, default="Pending", max_length=20)
    date_create_at = models.DateTimeField(auto_now_add=True, null=True)


"""
Table for Store the Ledger data
"""
class Ledger(models.Model) :
    id = models.AutoField(primary_key=True)
    bill_id = models.ForeignKey(Bill, related_name="bill_ledger", on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.ForeignKey(Payment, related_name="payment_ledger", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(null=True)


"""
Table for Store the Shipment charges data
"""
class ShipmentCharges(models.Model) :
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    service_by = models.ForeignKey(ServiceProvider, null=True, on_delete=models.CASCADE)
    order_mode = models.CharField(choices=ORDER_MODE, default="B2C", max_length=10)
    fsc = models.FloatField(default=0.0)
    min_fov = models.FloatField(default=0.0)
    fov = models.FloatField(default=0.0)
    docket = models.FloatField(default=0.0)
    min_cod_to_pay_charge = models.FloatField(default=0.0)
    cod_to_pay_charge = models.FloatField(default=0.0)
    min_charge_weight = models.FloatField(null=True, blank=True)
    date_created_at = models.DateTimeField(auto_now_add=True, null=True)


"""
Table for Store the Setting data
"""
class Setting(models.Model) :
    id = models.AutoField(primary_key=True)
    fsc = models.FloatField(default=0.0)
    fov = models.FloatField(default=0.0)
    docket = models.FloatField(default=0.0)
    date_created_at = models.DateTimeField(auto_now_add=True, null=True)