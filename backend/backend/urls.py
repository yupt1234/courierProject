"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from courier_app.views import *
from courier_app import authViews
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
# from django.conf.urls import url

urlpatterns = [

    path('api/login/',authViews.UserLoginView.as_view()),

    path('admin/', admin.site.urls),
    path('api/table-count/',TableCountAPI.as_view()),
    path('api/service-provider-detail/',ServiceProviderAPI.as_view()),
    path('api/service-provider-detail/<int:pk>',ServiceProviderAPI.as_view()),
    path('api/frieght-rate-detail/',QuotationAPI.as_view()),
    path('api/frieght-rate-detail/<int:pk>',QuotationAPI.as_view()),
    path('api/customer-detail/',CustomerAPI.as_view()),
    path('api/customer-detail/<int:pk>',CustomerAPI.as_view()),
    path('api/order-detail/',OrderAPI.as_view()),
    path('api/order-detail/<int:pk>',OrderAPI.as_view()),
    path('api/order-selection/',OrderSelectionAPI.as_view()),
    path('api/payment-detail/',PaymentAPI.as_view()),
    path('api/payment-detail/<int:pk>',PaymentAPI.as_view()),
    path('api/ledger-detail/',LedgerAPI.as_view()),
    path('api/ledger-detail/<int:pk>',LedgerAPI.as_view()),
    path('api/save-bill-detail/<int:pk>',GenerateBillApiView.as_view()),
    path('api/service-customer-detail/',ServiceCustomerApiView.as_view()),
    path('api/bill-list/<str:status>',BillListApiView.as_view()),
    path('api/get-bill-detail/<int:pk>',GetBillApiView.as_view()),

    path('api/get-orders-detail/',GetOrderDetailAPI.as_view()),
    path('api/get-cash-bookings-detail/',GetCashBookingDetailAPI.as_view()),
    path('api/zone-detail/',ZoneApiView.as_view()),
    path('api/quotation-detail/',QuotationApiView.as_view()),
    path('api/quotation-detail/<int:pk>',QuotationApiView.as_view()),
    path('api/get-zones-detail/',GetZoneDetailsAPI.as_view()),
    path('api/get-quotation-detail/',GetQuotationDetailsAPI.as_view()),
    path('api/setting-detail/', SettingApiView.as_view()),
    path('api/get-quotation-list/',QuotationFormatAPI.as_view()),
    path('api/get-customer-detail/',GetCustomerDetailsAPI.as_view()),
    path('api/b2c-zone-detail/',B2CZoneApiView.as_view()),
    path('api/get-b2c-zone-detail/',GetB2CZoneDetailsAPI.as_view()),
    path('api/b2c-quotation-detail/',B2CQuotationApiView.as_view()),
    path('api/b2c-quotation-detail/<int:pk>',B2CQuotationApiView.as_view()),
    path('api/get-b2c-quotation-detail/',GetB2CQuotationDetailsAPI.as_view()),
    path('api/get-b2c-quotation-list/',B2CQuotationFormatAPI.as_view()),
    path('api/get-shipment-charges/',GetShipmentChargesAPI.as_view()),
    path('api/shipment-charges/',ShipmentChargesAPI.as_view()),

    path('api/get-payment-list/',GetPaymentDetailAPI.as_view()),
    path('api/get-cod-payment-list/',GetCodPaymentDetailAPI.as_view()),
    path('api/cash-order-detail/',CashOrderAPI.as_view()),
    path('api/get-cod-orders-detail/',GetCodOrderDetailAPI.as_view()),
    path('api/cod-payment-detail/',CodPaymentAPI.as_view()),
    path('api/cod-payment-detail/<int:pk>',CodPaymentAPI.as_view()),

    # Define a catch-all pattern for frontend routes
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    # re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)