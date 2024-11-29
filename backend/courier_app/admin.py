from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.


class ServiceProviderAdmin(admin.ModelAdmin):
    pass
admin.site.register(ServiceProvider,ServiceProviderAdmin)

class QuotationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Quotation,QuotationAdmin)

admin.site.register(Customer)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'awb_no', 'shipment_date']
    search_fields = ['awb_no']
admin.site.register(Order, OrderAdmin)

# admin.site.register(Bill)
class BillModelAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'no_of_orders', 'bill_amount', 'balance_amount', 'is_paid', 'payment_id']
    # list_filter = ['customer_id']
    search_fields = ['customer_id']
admin.site.register(Bill, BillModelAdmin)

admin.site.register(Ledger)

admin.site.register(Zone)

admin.site.register(Setting)

admin.site.register(B2CQuotation)

admin.site.register(B2CZone)

admin.site.register(ShipmentCharges)

admin.site.register(Payment)

admin.site.register(BillPayment)

admin.site.register(CashBooking)

admin.site.register(CodPayment)