from rest_framework import serializers
from .models import *



class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceProvider
        fields='__all__'


class QuotationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    service_provider = serializers.CharField(source="service_by.name", required=False)
    service_provider_img = serializers.CharField(source="service_by.image", required=False)
    class Meta:
        model=Quotation
        fields='__all__'

class GetFrieghtRateSerializer(serializers.ModelSerializer):
    # service_provider_name = serializers.CharField(source="service_Provider_id.name")
    customer_name = serializers.CharField(source="customer_id.company_name")
    class Meta:
        model=Quotation
        fields='__all__'


class B2CQuotationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer_id.customer_name", required=False)
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    service_provider = serializers.CharField(source="service_by.name", required=False)
    service_provider_img = serializers.ImageField(source="service_by.image", required=False)
    class Meta:
        model=B2CQuotation
        fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'


class OrderSaveSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    customer_name = serializers.CharField(source="customer_id.company_name", required=False)
    serviceProvider = serializers.CharField(source="service_by.name", required=False)
    class Meta:
        model=Order
        fields='__all__'


class CashBookingSerializer(serializers.ModelSerializer):
    serviceProvider = serializers.CharField(source="service_by.name", required=False)
    class Meta:
        model=CashBooking
        fields='__all__'


class PaymentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    customer_name = serializers.CharField(source="customer_id.customer_name", required=False)
    class Meta:
        model=Payment
        fields='__all__'

    
class CodPaymentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    customer_name = serializers.CharField(source="customer_id.customer_name", required=False)
    class Meta:
        model=CodPayment
        fields='__all__'


class LedgerSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer_id.company_name", required=False)
    company_name = serializers.CharField(source="customer_id.customer_name", required=False)
    order_ID = serializers.CharField(source="order_id.order_id", required=False)
    payment_mode = serializers.CharField(source="payment_id.payment_mode", required=False)
    payment_amount = serializers.CharField(source="payment_id.amount", required=False)
    order_amount = serializers.CharField(source="order_id.freight_amount", required=False)
    class Meta:
        model=Ledger
        fields='__all__'


class BillSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    customer_name = serializers.CharField(source="customer_id.customer_name", required=False)
    class Meta:
        model=Bill
        fields='__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=Zone
        fields='__all__'


class B2CZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=B2CZone
        fields='__all__'


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Setting
        fields='__all__'

class ShipmentChargesSerializer(serializers.ModelSerializer):
    service_provider = serializers.CharField(source="service_by.name", required=False)
    customer_name = serializers.CharField(source="customer_id.customer_name", required=False)
    company_name = serializers.CharField(source="customer_id.company_name", required=False)
    class Meta:
        model=ShipmentCharges
        fields='__all__'