from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from courier_app.custom_view import *
from copy import deepcopy
from .authViews import *



class TableCountAPI(APIView) :
    def post(self, request) :
        requestData = request.data
        if requestData["tableName"] :
            if requestData["tableName"] == "Bill" :
                objCount = Bill.objects.count()
            elif requestData["tableName"] == "Order" :
                objCount = Order.objects.count()
            elif requestData["tableName"] == "Ledger" :
                billCount = Bill.objects.count()
                paymentCount = Payment.objects.count()
                objCount = billCount + paymentCount
            elif requestData["tableName"] == "Zone" :
                objCount = Zone.objects.count()
            elif requestData["tableName"] == "B2CZone" :
                objCount = B2CZone.objects.count()
            elif requestData["tableName"] == "Quotation" :
                objCount = Quotation.objects.count()
            elif requestData["tableName"] == "B2CQuotation" :
                objCount = B2CQuotation.objects.count()
            elif requestData["tableName"] == "Customer" :
                objCount = Customer.objects.count()
            elif requestData["tableName"] == "CashBooking" :
                objCount = CashBooking.objects.count()
            elif requestData["tableName"] == "COD-Order" :
                objCount = Order.objects.filter(payment_mode="COD").count()
            elif requestData["tableName"] == "CodPayment" :
                objCount = CodPayment.objects.count()
            else :
                objCount = 0
            return Response({"msg":"success", "tableCount":objCount})


class ServiceProviderAPI(APIView):
    '''
    Get all records of service provider
    '''
    # @authenticate_request
    def get(self,request):
        sericeProviderList = ServiceProvider.objects.all().order_by('date_create_at')
        serializedData = ServiceProviderSerializer(sericeProviderList, many=True)
        return Response({"sericeProviderList": serializedData.data})

    '''
    create new service provider record
    '''
    def post(self,request):
        if "id" in request.data :
            spObj = ServiceProvider.objects.get(id = request.data.get("id"))
            serializedData = ServiceProviderSerializer(spObj, data=request.data)
        else :
            spCount = ServiceProvider.objects.filter(name=request.data["name"]).count()
            if spCount > 0 :
                return Response({"duplicate": "Data With This Name Already Exist"})            
            serializedData = ServiceProviderSerializer(data=request.data)
        sericeProviderData = ServiceProvider.objects.all().order_by('date_create_at')
        sericeProviderList = ServiceProviderSerializer(sericeProviderData, many=True)
        if serializedData.is_valid():
            serializedData.save()
            return Response({"successMsg": "Saved Successfully", "sericeProviderList": sericeProviderList.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    '''
    update the perticular record
    '''
    def put(self, request,tenant, pk):
        id = pk
        ServiceProviderObj = ServiceProvider.objects.get(id = id)
        serializedData = ServiceProviderSerializer(ServiceProviderObj, data=request.data)
        if serializedData.is_valid(raise_exception=True):
            serializedData.save()
            return Response({"msg": "Updated Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    '''
    delete the perticular record
    '''
    def delete(self, request, pk):
        id = pk
        ServiceProviderObj = ServiceProvider.objects.get(id=id)
        if ServiceProviderObj :
            ServiceProviderObj.delete()
            sericeProviderList = ServiceProvider.objects.all().order_by('date_create_at').values()
            return Response({"msg": "Deleted Successfully", "sericeProviderList": sericeProviderList})
        return Response({"error": "error"})


class QuotationAPI(APIView):
    '''
    Get all records of Frieght Rate
    '''
    def get(self,request):
        frieghtRateList = Quotation.objects.all().order_by('date_create_at')
        serializedData = GetFrieghtRateSerializer(frieghtRateList, many=True)
        return Response({"frieghtRateList": serializedData.data})

    '''
    create new Frieght Rate record
    '''
    def post(self,request):
        if "id" in request.data :
            frObj = Quotation.objects.get(id = request.data.get("id"))
            serializedData = QuotationSerializer(frObj, data=request.data)
        else :
            serializedData = QuotationSerializer(data=request.data)
        frieghtRateList = Quotation.objects.all().order_by('date_create_at')
        getFrieghtRateSerializers = QuotationSerializer(frieghtRateList, many=True)
        if serializedData.is_valid():
            serializedData.save()
            return Response({"successMsg": "Saved Successfully", "frieghtRateList": getFrieghtRateSerializers.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    '''
    delete the perticular record
    '''
    def delete(self, request, pk):
        id = pk
        frieghtRateObj = Quotation.objects.get(id=id)
        if frieghtRateObj :
            frieghtRateObj.delete()
            frieghtRateList = Quotation.objects.all().order_by('date_create_at')
            getFrieghtRateSerializers = GetFrieghtRateSerializer(frieghtRateList, many=True)
            return Response({"msg": "Deleted Successfully", "frieghtRateList": getFrieghtRateSerializers.data})
        return Response({"error": "error"})

"""
CUSTOMER API CRUD OPERATION
"""
class CustomerAPI(APIView):
    '''
    Get all records of Customer
    '''
    def get(self,request):
        customerList = Customer.objects.all().order_by('date_create_at')
        serializedData = CustomerSerializer(customerList, many=True)
        return Response({"customerList": serializedData.data})

    '''
    create and update Customer record
    '''
    def post(self,request):
        if "id" in request.data :
            customerObj = Customer.objects.get(id = request.data.get("id"))
            serializedData = CustomerSerializer(customerObj, data=request.data)
        else :
            serializedData = CustomerSerializer(data=request.data)
        # customerList = Customer.objects.all().order_by('date_create_at').values()
        if serializedData.is_valid():
            serializedData.save()
            # return Response({"successMsg": "Saved Successfully", "customerList": customerList}, status=status.HTTP_201_CREATED)
            return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    '''
    delete the perticular record
    '''
    def delete(self, request, pk):
        id = pk
        customerObj = Customer.objects.get(id=id)
        if customerObj :
            customerObj.delete()
            customerList = Customer.objects.all().order_by('date_create_at')
            getCustomerSerializers = CustomerSerializer(customerList, many=True)
            return Response({"msg": "Deleted Successfully", "customerList": getCustomerSerializers.data})
        return Response({"error": "error"})


"""
ORDER SELECTION API
"""
class OrderSelectionAPI(APIView):
    '''
    Get all customers and service provider for selection in order entry form
    '''
    def get(self,request):
        customerList = Customer.objects.all().order_by('date_create_at').values()
        serviceByList = ServiceProvider.objects.all().order_by('date_create_at').values()
        return Response({"customerList": customerList, "serviceByList": serviceByList})
    

"""
ORDER API CRUD OPERATION
"""
class OrderAPI(APIView):
    '''
    Get all records of Orders
    '''
    def get(self,request):
        orderList = Order.objects.all().order_by('date_create_at')
        serializedData = OrderSaveSerializer(orderList, many=True)
        return Response({"orderList": serializedData.data})

    '''
    create and update Order record
    '''
    # def post(self,request):
    #     print(request.data)
    #     if "id" in request.data :
    #         orderObj = Order.objects.get(id = request.data.get("id"))
    #         serializedData = OrderSaveSerializer(orderObj, data=request.data)
    #     else :
    #         serializedData = OrderSaveSerializer(data=request.data)
    #     orderList = Order.objects.all().order_by('date_create_at').values()
    #     if serializedData.is_valid():
    #         serializedData.save()
    #         if "id" not in request.data :
    #             order_id = serializedData.data.get("id")
    #             date = serializedData.data.get("shipment_date")
    #             customer_id = request.data.get("customer_id")
    #             ledgerData = {
    #                 "order_id": order_id,
    #                 "customer_id": customer_id,
    #                 "date": date
    #             }
    #             ledgerSerializer = LedgerSerializer(data=ledgerData)
    #             if ledgerSerializer.is_valid() :
    #                 ledgerSerializer.save()
    #                 return Response({"successMsg": "Saved Successfully", "orderList": orderList}, status=status.HTTP_201_CREATED)
    #     return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})

    def post(self,request):
        orders = request.data
        # Use a list to store invailid instances
        orderErrors = []
        if len(orders) > 0 :
            for order in orders :
                fromStateQuery = order["from_state"].replace(" ", "").upper()
                toStateQuery = order["shipped_to_state"].replace(" ", "").upper()
                paymentMode = order["payment_mode"].upper()

                order.update({'payment_mode': paymentMode, 'order_mode': order["order_mode"].upper(), 'from_state': fromStateQuery, 'shipped_to_state': toStateQuery, "order_type": order["order_type"].upper(), 'deliver_mode': order["deliver_mode"].upper(), 'balance_cod_amount': Decimal(order['invoice_value'])})

                print(order["customer_id"], "order-customer_id")
                print(order["service_by"], "order-service_by")
                print(order["order_mode"], "order-order_mode")
                shipmentChargesObj = ShipmentCharges.objects.filter(customer_id=order["customer_id"], service_by=order["service_by"], order_mode=order["order_mode"]).first()

                if shipmentChargesObj :

                    if order["order_mode"].upper() == "B2B" :
                        fromCityQuery = order["from_city"].replace(" ", "").upper()
                        toCityQuery = order["shipped_to_city"].replace(" ", "").upper()
                        getFromState = Zone.objects.filter(state=fromStateQuery)
                        getShippedState = Zone.objects.filter(state=toStateQuery)
                        if getFromState.first() and getShippedState.first() :
                            from_zone = getFromState.first().zone
                            to_zone = getShippedState.first().zone
                            quotationData = Quotation.objects.filter(customer_id=order["customer_id"], from_zone=from_zone, service_by=order["service_by"]).first()
                    elif order["order_mode"].upper() == "B2C" :
                        fromCityQuery = order["from_city"].replace(" ", "").upper()
                        toCityQuery = order["shipped_to_city"].replace(" ", "").upper()

                        fromStateQuery = order["from_state"].replace(" ", "").upper()
                        toStateQuery = order["shipped_to_state"].replace(" ", "").upper()

                        getFromState = B2CZone.objects.filter(state=fromStateQuery)
                        getShippedState = B2CZone.objects.filter(state=toStateQuery)

                        if getFromState.first() and getShippedState.first() :
                            from_zone = getFromState.first().zone
                            to_zone = getShippedState.first().zone
                            # if from_zone == to_zone and fromCityQuery == toCityQuery :
                            print(order["charged_weight"], "charged_weight")
                            # quotationData = B2CQuotation.objects.filter(Q(Q(min_weight__gt=order["charged_weight"]) & Q(weight__lte=order["charged_weight"])) | Q(weight__gt=order["charged_weight"])).filter(customer_id=order["customer_id"], deliver_mode=order["deliver_mode"], from_zone=from_zone, service_by=order["service_by"]).first()
                            quotationData = B2CQuotation.objects.filter(Q(Q(min_weight__lt=order["charged_weight"]) & Q(weight__gte=order["charged_weight"])) | Q(weight__lte=order["charged_weight"])).filter(customer_id=order["customer_id"], deliver_mode=order["deliver_mode"], from_zone=from_zone, service_by=order["service_by"]).order_by('weight').last()
                            # elif 
                    if getFromState and getShippedState:

                        allowSave = False

                        if quotationData and getFromState :
                            calculatedOrder = b2bOrderSave(order, quotationData, from_zone, to_zone, fromCityQuery, toCityQuery, shipmentChargesObj)
                            allowSave = True

                            if allowSave :

                                if "id" in order :
                                    orderObj = Order.objects.get(id=order["id"])
                                    serializedData = OrderSaveSerializer(orderObj, data=calculatedOrder)
                                else :
                                    serializedData = OrderSaveSerializer(data=calculatedOrder)
                                if serializedData.is_valid():
                                    print("saved", order["shipped_to_name"])
                                    serializedData.save()
                                else :
                                    print(serializedData.errors, "serializedData.errors")
                                    orderErrors.append({"index":orders.index(order)+1, "error": serializedData.errors})
                            else :
                                orderErrors.append({"index":orders.index(order)+1, "error": "Quotation Rate Not Exist For This Zone! Please Add Rate"})
                        else :
                            orderErrors.append({"index":orders.index(order)+1, "error": "Quotation Not Exist For This Zone! Please Add Quotation and Rate"})
                    else :
                        orderErrors.append({"index":orders.index(order)+1, "error": "Zone Not Declair For This State! Please Add State In The Zone Section"})
                else : orderErrors.append({"index":orders.index(order)+1, "error": "Shipment Charges Not Added! Please Add Shipment Charges"})
            if len(orderErrors) > 0 :
                return Response({'info':'Saved and Errors', "orderErrors": orderErrors})
            else :
                return Response({'success':'successfully data saved'})
        else :
            return Response({'error':'Order not Exist! Please Check Your Data'})

            # print(validated_orders, "llllllllll")
            # try:
            #     # Use bulk_create to efficiently save all instances in one go
            #     Order.objects.bulk_create(validated_orders)
            #     return Response({"success": "Orders created successfully"}, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     # Handle any exceptions that may occur during bulk_create
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    '''
    delete the perticular record
    '''
    def delete(self, request, pk):
        id = pk
        orderObj = Order.objects.get(id=id)
        if orderObj :
            orderObj.delete()
            # orderList = Order.objects.all().order_by('date_create_at')
            # getOrderSerializers = OrderSaveSerializer(orderList, many=True)
            return Response({"msg": "Deleted Successfully"})
        return Response({"error": "error"})
    

"""
CASH ORDER API CRUD OPERATION
"""
class CashOrderAPI(APIView):
    def post(self,request):
        orders = request.data
        # Use a list to store invailid instances
        orderErrors = []
        if len(orders) > 0 :
            for order in orders :
                fromStateQuery = order["origin_state"].replace(" ", "").upper()
                toStateQuery = order["destination_state"].replace(" ", "").upper()

                counter = order["counter"].replace(" ", "").upper()

                if counter == "WALLFORTCITY" or counter == "PANDRI" :

                    payMode = order["mode"].replace(" ", "").upper()

                    if Decimal(order['freight_amount']) <= Decimal(order['paid_amount']) or Decimal(order['freight_amount']) <= Decimal(order['balance_amount']) :
                        order.update({'order_status': "Completed"})
                    else :
                        order.update({'order_status': "Pending"})

                    order.update({'counter': counter, 'mode': payMode, 'order_mode': order["order_mode"].upper(), 'origin_state': fromStateQuery, 'destination_state': toStateQuery, 'deliver_mode': order["deliver_mode"].upper()})

                    if "id" in order :
                        orderObj = CashBooking.objects.get(id=order["id"])
                        serializedData = CashBookingSerializer(orderObj, data=order)
                    else :
                        serializedData = CashBookingSerializer(data=order)

                    if serializedData.is_valid():
                        serializedData.save()
                    else :
                        orderErrors.append({"index":orders.index(order)+1, "error": serializedData.errors})

                else :
                    orderErrors.append({"index":orders.index(order)+1, "error": "Please Give Proper Counter Name"})
                
                # print(serializedData.errors, "errors----------")

            if len(orderErrors) > 0 :
                return Response({'info':'Saved and Errors', "orderErrors": orderErrors})
            else :
                return Response({'success':'successfully data saved'})
        else :
            return Response({'error':'Order not Exist! Please Check Your Data'})
        
    def put(self, request) :
        print(request.data)
        CashBooking.objects.filter(id__in=request.data).update(order_status='Completed')
        return Response({'msg':"Updated Successfully"})
    

"""
PAYMENT API CRUD OPERATION
"""
class PaymentAPI(APIView):
    '''
    Get all records of Payments
    '''
    def get(self,request):
        paymentList = Payment.objects.all().order_by('date_create_at')
        serializedData = PaymentSerializer(paymentList, many=True)
        return Response({"paymentList": serializedData.data})

    '''
    create and update Payment record
    '''
    # def post(self,request):
    #     if "id" in request.data :
    #         paymentObj = Payment.objects.get(id = request.data.get("id"))
    #         serializedData = PaymentSerializer(paymentObj, data=request.data)
    #     else :
    #         serializedData = PaymentSerializer(data=request.data)
    #     if serializedData.is_valid() :
    #         newPayment = serializedData.save()
    #         # if "id" not in request.data :
    #         # This statement for bill Payment Complition status
    #         unPaidBills = Bill.objects.filter(
    #             customer_id=request.data.get("customer_id"),
    #             is_paid=False,
    #             balance_amount__gte=0.00
    #         ).order_by("date")
            
    #         balanceAmount = Decimal(request.data.get("amount"))
    #         for bill in unPaidBills :
    #             if bill.balance_amount < balanceAmount :
    #                 balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
    #                 bill.balance_amount = Decimal(0.00)
    #                 bill.is_paid = True
    #                 bill.payment_id = newPayment
    #                 bill.save()
    #             else :
    #                 bill.balance_amount = bill.balance_amount - balanceAmount
    #                 if bill.balance_amount == 0.00 :
    #                     bill.is_paid = True
    #                 bill.payment_id = newPayment
    #                 bill.save()
    #                 break
    #         print("lllllllllll")
    #         return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
    #     return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    def post(self,request):
        customerObj = Customer.objects.get(id=request.data.get("customer_id"))
        serializedData = PaymentSerializer(data=request.data)
        if serializedData.is_valid() :
            newPayment = serializedData.save()
            unPaidBills = Bill.objects.filter(
                customer_id=request.data.get("customer_id"),
                is_paid=False,
                balance_amount__gte=0.00
            ).order_by("id")
            
            balanceAmount = Decimal(request.data.get("amount"))
            for bill in unPaidBills :
                if bill.balance_amount < balanceAmount :
                    BillPayment.objects.create(
                        customer_id=customerObj,
                        bill_id=bill,
                        payment_id=newPayment,
                        amount=Decimal(bill.balance_amount)
                    )
                    balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
                    bill.balance_amount = Decimal(0.00)
                    bill.is_paid = True
                    bill.payment_id = newPayment
                    bill.save()
                else :
                    BillPayment.objects.create(
                        customer_id=customerObj,
                        bill_id=bill,
                        payment_id=newPayment,
                        amount=balanceAmount
                    )
                    bill.balance_amount = bill.balance_amount - balanceAmount
                    if bill.balance_amount == 0.00 :
                        bill.is_paid = True
                    bill.payment_id = newPayment
                    bill.save()
                    print("lllll", bill.balance_amount)
                    break
                    
            print("lllllllllll")
            return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    def put(self,request, pk=None):
        if pk is not None :
            paymentObj = Payment.objects.get(id=pk)
            customerObj = Customer.objects.get(id=request.data.get("customer_id"))
            serializedData = PaymentSerializer(paymentObj, request.data)
            if serializedData.is_valid() :
                newPayment = serializedData.save()
                unPaidBills = Bill.objects.filter(
                    customer_id=request.data.get("customer_id"),
                    is_paid=False,
                    balance_amount__gte=0.00
                ).order_by("id")
                # paidBillPayments = BillPayment.objects.filter(payment_id=newPayment.id).order_by('id')
                paidBills = Bill.objects.filter(payment_id=newPayment.id).order_by('id')
                
                balanceAmount = Decimal(request.data.get("amount"))

                for bill in paidBills :
                    print("inside paidBills")
                    billPaymentObj = BillPayment.objects.filter(payment_id=newPayment.id, bill_id=bill.id).first()
                    bill.balance_amount = bill.balance_amount + billPaymentObj.amount
                    if bill.balance_amount < balanceAmount :
                        print("bill.balance_amount < balanceAmount")
                        billClearAmt = Decimal(bill.balance_amount)
                        balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
                        bill.balance_amount = Decimal(0.00)
                        bill.is_paid = True
                        bill.payment_id = newPayment
                        bill.save()

                        billPaymentObj.amount = billClearAmt
                        print(billPaymentObj.amount, "billPaymentObj.amount")
                        billPaymentObj.save()
                    else :
                        print("not --- bill.balance_amount < balanceAmount")
                        print(balanceAmount, "balanceAmount")
                        print(bill.balance_amount, "bill.balance_amount")
                        if balanceAmount == 0.00 :
                            billPaymentObj.delete()
                            bill.payment_id = None
                            bill.is_paid = False
                            bill.save()
                        else :
                            billClearAmt = Decimal(balanceAmount)
                            bill.balance_amount = bill.balance_amount - Decimal(balanceAmount)
                            balanceAmount = 0.00
                            if bill.balance_amount <= 0.00 :
                                bill.is_paid = True
                            else :
                                bill.is_paid = False
                            bill.payment_id = newPayment
                            print("bill.balance_amount", bill.balance_amount)
                            bill.save()

                            billPaymentObj.amount = billClearAmt
                            print(billPaymentObj.amount, "billPaymentObj.amount")
                            billPaymentObj.save()
                    # if balanceAmount <= 0.00 :
                    #     break
                
                if balanceAmount > 0.00 :
                    print(balanceAmount, "balanceAmount")
                    print("hhhhhhhhhhhhh")
                    for bill in unPaidBills :
                        if bill.balance_amount < balanceAmount :
                            BillPayment.objects.create(
                                customer_id=customerObj,
                                bill_id=bill,
                                payment_id=newPayment,
                                amount=Decimal(bill.balance_amount)
                            )
                            balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
                            bill.balance_amount = Decimal(0.00)
                            bill.is_paid = True
                            bill.payment_id = newPayment
                            bill.save()
                        else :
                            BillPayment.objects.create(
                                customer_id=customerObj,
                                bill_id=bill,
                                payment_id=newPayment,
                                amount=balanceAmount
                            )
                            bill.balance_amount = bill.balance_amount - balanceAmount
                            if bill.balance_amount == 0.00 :
                                bill.is_paid = True
                            bill.payment_id = newPayment
                            bill.save()
                            print("lllll", bill.balance_amount)
                            break
                return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    # def put(self, request, pk=None) :
    #     if pk is not None :
    #         paymentObj = Payment.objects.get(id=pk)
    #         if paymentObj :
    #             paymentSerializer = PaymentSerializer(paymentObj, request.data)
    #             if paymentSerializer.is_valid() :
    #                 newPaymentObj = paymentSerializer.save()

    #                 paidPaymentBilles = Bill.objects.filter(is_paid = True, payment_id = paymentObj.id, customer_id=request.data.get("customer_id"))

    #                 pendingPaymentBilles = Bill.objects.filter(is_paid = False, payment_id = paymentObj.id, customer_id=request.data.get("customer_id"))

    #                 pendingOtherPaymentBilles = Bill.objects.filter(
    #                                             Q(payment_id__isnull=False) & ~Q(payment_id=newPaymentObj.id),
    #                                             customer_id=request.data.get("customer_id")
    #                 )

    #                 unPaidBills = Bill.objects.filter(payment_id=None, customer_id=request.data.get("customer_id")
    #                 ).order_by("date")

    #                 joinedBills = pendingPaymentBilles | unPaidBills

    #                 print(joinedBills, "joinedBills")

    #                 diffAmount = paymentObj.amount - newPaymentObj.amount 
    #                 remainingAmount = 0
    #                 balanceAmount = Decimal(request.data.get("amount"))

    #                 for i in range(0, 3) :
    #                     print("2222")
    #                     if balanceAmount > 0.0 :

    #                         for bill in paidPaymentBilles :
    #                             print("pppppppppppppppp")
    #                             bill.is_paid = False
    #                             bill.balance_amount = bill.bill_amount
    #                             bill.payment_id = None
    #                             if bill.balance_amount < balanceAmount :
    #                                 print("vvvvvvvvvvvvvvvvvv")
    #                                 balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
    #                                 bill.balance_amount = Decimal(0.00)
    #                                 bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                             else :
    #                                 print("aaaaaaaaaaaaaaaaaaaa")
    #                                 balanceAmount = 0.0
    #                                 bill.balance_amount = Decimal(bill.balance_amount) - Decimal(balanceAmount)
    #                                 if bill.balance_amount == 0.00 :
    #                                     bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                                 break

    #                         for bill in pendingPaymentBilles :
    #                             print("pppppppppppppppp")
    #                             bill.is_paid = False
    #                             bill.balance_amount = bill.bill_amount
    #                             bill.payment_id = None
    #                             if bill.balance_amount < balanceAmount :
    #                                 print("vvvvvvvvvvvvvvvvvv")
    #                                 balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
    #                                 bill.balance_amount = Decimal(0.00)
    #                                 bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                             else :
    #                                 print("aaaaaaaaaaaaaaaaaaaa")
    #                                 balanceAmount = 0.0
    #                                 bill.balance_amount = Decimal(bill.balance_amount) - Decimal(balanceAmount)
    #                                 if bill.balance_amount == 0.00 :
    #                                     bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                                 break

    #                         for bill in pendingOtherPaymentBilles :
    #                             print("pppppppppppppppp")
    #                             if bill.balance_amount < balanceAmount :
    #                                 print("vvvvvvvvvvvvvvvvvv")
    #                                 balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
    #                                 bill.balance_amount = Decimal(0.00)
    #                                 bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                             else :
    #                                 print("aaaaaaaaaaaaaaaaaaaa")
    #                                 balanceAmount = 0.0
    #                                 bill.balance_amount = Decimal(bill.balance_amount) - Decimal(balanceAmount)
    #                                 if bill.balance_amount == 0.00 :
    #                                     bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                                 break

    #                         for bill in unPaidBills :
    #                             print("pppppppppppppppp")
    #                             bill.is_paid = False
    #                             bill.balance_amount = bill.bill_amount
    #                             bill.payment_id = None
    #                             if bill.balance_amount < balanceAmount :
    #                                 print("vvvvvvvvvvvvvvvvvv")
    #                                 balanceAmount = Decimal(balanceAmount) - Decimal(bill.balance_amount)
    #                                 bill.balance_amount = Decimal(0.00)
    #                                 bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                             else :
    #                                 print("aaaaaaaaaaaaaaaaaaaa")
    #                                 balanceAmount = 0.0
    #                                 bill.balance_amount = bill.balance_amount - balanceAmount
    #                                 if bill.balance_amount == 0.00 :
    #                                     bill.is_paid = True
    #                                 bill.payment_id = newPaymentObj
    #                                 bill.save()
    #                                 break
    #                     else :
    #                         break
    #                 return Response({'successMsg': "Data Saved Successfully"})
    #             else :
    #                 return Response({'error':paymentSerializer.errors})
    #         else :
    #             return Response({'error':'Data not Selected! Please Try Again'})
    #     else :
    #         return Response({'error':'Data not Selected! Please Try Again'})



"""
COD PAYMENT API CRUD OPERATION
"""
class CodPaymentAPI(APIView):
    '''
    create cod Payment record
    '''
    def post(self,request):
        customerObj = Customer.objects.get(id=request.data.get("customer_id"))
        serializedData = CodPaymentSerializer(data=request.data)
        if serializedData.is_valid() :
            newPayment = serializedData.save()

            unPaidshipments = Order.objects.filter(customer_id=request.data.get("customer_id"), payment_mode="COD", shipment_status="DELIVERED", cod_status="Pending").order_by('id')
            
            balanceAmount = Decimal(request.data.get("amount"))
            print(unPaidshipments)
            for shipment in unPaidshipments :
                print('kkkkkkkkkkkkkkkkkkk')
                if shipment.balance_cod_amount < balanceAmount :
                    OrderCodPayment.objects.create(
                        customer_id=customerObj,
                        order_id=shipment,
                        cod_payment_id=newPayment,
                        amount=Decimal(shipment.balance_cod_amount)
                    )
                    balanceAmount = Decimal(balanceAmount) - Decimal(shipment.balance_cod_amount)
                    shipment.balance_cod_amount = Decimal(0.00)
                    shipment.cod_status = 'Paid'
                    shipment.cod_payment_id = newPayment
                    shipment.save()
                else :
                    OrderCodPayment.objects.create(
                        customer_id=customerObj,
                        order_id=shipment,
                        cod_payment_id=newPayment,
                        amount=balanceAmount
                    )
                    shipment.balance_cod_amount = shipment.balance_cod_amount - balanceAmount
                    if shipment.balance_cod_amount == 0.00 :
                        shipment.cod_status = 'Paid'
                    shipment.cod_payment_id = newPayment
                    print("lll")
                    shipment.save()
                    break
                    
            return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    
    def put(self,request, pk=None):
        from django.db.models import F
        if pk is not None :
            paymentObj = CodPayment.objects.get(id=pk)
            customerObj = Customer.objects.get(id=request.data.get("customer_id"))
            serializedData = CodPaymentSerializer(paymentObj, request.data)
            if serializedData.is_valid() :
                newPayment = serializedData.save()

                unPaidshipments = Order.objects.filter(customer_id=request.data.get("customer_id"), cod_payment_id=None, payment_mode="COD", shipment_status='DELIVERED').order_by('id')

                paidshipments = Order.objects.filter(customer_id=request.data.get("customer_id"), cod_payment_id=pk, payment_mode="COD",shipment_status='DELIVERED').order_by('id')

                # shipments.update(cod_payment_id=None, cod_status='Pending', balance_cod_amount=F('invoice_value'))

                # unPaidshipments = Order.objects.filter(customer_id=request.data.get("customer_id"), payment_mode="COD", shipment_status="DELIVERED", cod_status="Pending").order_by('id')

                balanceAmount = Decimal(request.data.get("amount"))

                for shipment in paidshipments :
                    print("inside paidBills")
                    orderCodPaymentObj = OrderCodPayment.objects.filter(cod_payment_id=newPayment.id, order_id=shipment.id).first()

                    shipment.balance_cod_amount = shipment.balance_cod_amount + orderCodPaymentObj.amount

                    if shipment.balance_cod_amount < balanceAmount :
                        print("bill.balance_amount < balanceAmount")
                        orderClearAmt = Decimal(shipment.balance_cod_amount)
                        balanceAmount = Decimal(balanceAmount) - Decimal(shipment.balance_cod_amount)
                        shipment.balance_cod_amount = Decimal(0.00)
                        shipment.cod_status = 'Paid'
                        shipment.cod_payment_id = newPayment
                        shipment.save()

                        orderCodPaymentObj.amount = orderClearAmt
                        print(orderCodPaymentObj.amount, "billPaymentObj.amount")
                        orderCodPaymentObj.save()
                    else :
                        print("not --- bill.balance_amount < balanceAmount")
                        print(balanceAmount, "balanceAmount")
                        print(shipment.balance_cod_amount, "bill.balance_amount")
                        if balanceAmount == 0.00 :
                            orderCodPaymentObj.delete()
                            shipment.cod_payment_id = None
                            shipment.cod_status = 'Pending'
                            shipment.save()
                        else :
                            orderClearAmt = Decimal(balanceAmount)
                            shipment.balance_cod_amount = shipment.balance_cod_amount - Decimal(balanceAmount)
                            balanceAmount = 0.00
                            if shipment.balance_cod_amount <= 0.00 :
                                shipment.cod_status = 'Paid'
                            else :
                                shipment.cod_status = 'Pending'
                            shipment.cod_payment_id = newPayment
                            print("bill.balance_amount", shipment.balance_cod_amount)
                            shipment.save()

                            orderCodPaymentObj.amount = orderClearAmt
                            print(orderCodPaymentObj.amount, "billPaymentObj.amount")
                            orderCodPaymentObj.save()
                
                if balanceAmount > 0.00 :
                    print(balanceAmount, "balanceAmount")
                    print("hhhhhhhhhhhhh")
                    for shipment in unPaidshipments :
                        if shipment.balance_cod_amount < balanceAmount :
                            OrderCodPayment.objects.create(
                                customer_id=customerObj,
                                order_id=shipment,
                                cod_payment_id=newPayment,
                                amount=Decimal(shipment.balance_cod_amount)
                            )
                            balanceAmount = Decimal(balanceAmount) - Decimal(shipment.balance_cod_amount)
                            shipment.balance_cod_amount = Decimal(0.00)
                            shipment.cod_status = 'Paid'
                            shipment.cod_payment_id = newPayment
                            shipment.save()
                        else :
                            OrderCodPayment.objects.create(
                                customer_id=customerObj,
                                order_id=shipment,
                                cod_payment_id=newPayment,
                                amount=balanceAmount
                            )
                            shipment.balance_cod_amount = shipment.balance_cod_amount - balanceAmount
                            if shipment.balance_cod_amount == 0.00 :
                                shipment.cod_status = 'Paid'
                            shipment.cod_payment_id = newPayment
                            shipment.save()
                            print("lllll", shipment.balance_cod_amount)
                            break

                return Response({"successMsg": "Saved Successfully"}, status=status.HTTP_201_CREATED)
            print(serializedData.errors, "serializedData.errors")
            return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})


"""
LEDGER API CRUD OPERATION
"""
class LedgerAPI(APIView):
    '''
    Get all records of Ledger
    '''
    def get(self, request, pk=None):
        # id = pk
        if id is not None :
            ledgerList = Ledger.objects.filter(customer_id=id).order_by('date')
        else :
            ledgerList = Ledger.objects.all().order_by('date')
        serializedData = LedgerSerializer(ledgerList, many=True)
        return Response({"ledgerList": serializedData.data})

    
    '''
    Get all records of Ledger with pagination detail
    '''
    def post(self, request) :
        from operator import itemgetter

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        # if 'searchText' in request.data :
        #     searchText=request.data['searchText']
        filterCriteria = request.data["filterCriteria"]
        # if 'customer' or ('startDate' and 'endDate') in filterCriteria :
        #     startDate = request.data["filterCriteria"]
        print("filterCriteria", filterCriteria)

        ledgerList = []

        if 'customer' in filterCriteria and 'startDate' in filterCriteria and 'endDate' in filterCriteria :
            billList=Bill.objects.filter(Q(customer_id=filterCriteria["customer"]) & Q(date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
            paymentList=Payment.objects.filter(Q(customer_id=filterCriteria["customer"]) & Q(date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
        elif 'customer' in filterCriteria :
            billList=Bill.objects.filter(Q(customer_id=filterCriteria["customer"]))
            paymentList=Payment.objects.filter(Q(customer_id=filterCriteria["customer"]))
        elif 'startDate' in filterCriteria and 'endDate' in filterCriteria :
            billList=Bill.objects.filter(Q(date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
            paymentList=Payment.objects.filter(Q(date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
        else :
            billList = Bill.objects.all().order_by('-id')
            paymentList = Payment.objects.all().order_by('-id')

        billSerializers = BillSerializer(billList, many=True)
        paymentSerializers = PaymentSerializer(paymentList, many=True)

        # ledgerList.extend(billList)
        # ledgerList.extend(paymentList)
        ledgerList.extend(billSerializers.data)
        ledgerList.extend(paymentSerializers.data)

        ledgerListCount=len(ledgerList)
        paginator = Paginator(ledgerList, listPerPage)
        filteredledgerList = paginator.page(currentPage)

        serializedData = list(filteredledgerList)
        sorted_list = sorted(serializedData, key=itemgetter('date'), reverse=True)

        return Response({"ledgerList": sorted_list, "ledgerListCount": ledgerListCount})


"""
GENERATE BILL
"""
class GenerateBillApiView(APIView):
    '''
    Get all record of bill like no. of orders
    '''
    def post(self, request, pk=None) :
        customerId = pk
        if customerId :
            orderList = Order.objects.filter(
                customer_id=customerId,
                shipment_date__range=[request.data['startDate'], request.data['endDate']],
                # is_bill_generated=False
                order_status = "Pending",
            ).exclude(Q(Q(payment_mode="TO PAY") & Q(shipment_status="IN TRANSIT")) | 
            Q(Q(payment_mode="TO PAY") & Q(shipment_status="DELIVERED"))).order_by('id')

            orders = list(orderList)

            if orderList.count() >= 1 :
                orderAmount = orderList.aggregate(total_order_amount=Sum('freight_amount'))
                print(orderAmount, "orderAmount")
                total_order_amount = orderAmount['total_order_amount']
                orderCount = orderList.count()

                b2bCount = orderList.filter(order_mode="B2B").count()
                b2cCount = orderList.filter(order_mode="B2C").count()

                bill_amount = total_order_amount + (total_order_amount*18)/100

                bill_amount = round(bill_amount, 2)

                billData = {
                    "customer_id": customerId,
                    "start_date": request.data['startDate'],
                    "end_date": request.data['endDate'],
                    "no_of_orders": orderCount,
                    "no_of_b2b": b2bCount,
                    "no_of_b2c": b2cCount,
                    "basic_amount": total_order_amount,
                    "bill_amount": bill_amount,
                    "balance_amount": bill_amount
                }

                billSerializer = BillSerializer(data=billData)
                if billSerializer.is_valid() :
                    billObj = billSerializer.save()

                    serializedBillObj = BillSerializer(billObj)

                    # orderList.update(is_bill_generated=True)
                    orderList.update(order_status="Billed", bill_id=billObj.id)

                    billOrders = Order.objects.filter(bill_id=billObj.id)

                    serializedData = OrderSaveSerializer(billOrders, many=True)

                    customerDetail = Customer.objects.get(id=customerId)
                    customerSerializer = CustomerSerializer(customerDetail)

                    return Response({
                        "orderCount": orderCount,
                        "b2bCount": b2bCount,
                        "b2cCount": b2cCount,
                        # "basic_amount": total_order_amount,
                        # "total_order_amount": bill_amount,
                        "basic_amount": billObj.basic_amount,
                        "total_order_amount": billObj.bill_amount,
                        "orders": serializedData.data,
                        "customerDetail": customerSerializer.data,
                        "billData": serializedBillObj.data
                    })
                else :
                    print(billSerializer.errors)
                    return Response({"error": "Something went Wrong"})
            else :
                return Response({"error": "Pending Bill Orders not exist"})
        else :
            return Response({"error": "Customer not Present! Please Check Your Data"})
        

"""
GET THE SERVICE BY AND CUSTOMER DETAIL
"""
class ServiceCustomerApiView(APIView):
    '''
    Get all records of Serice providers and customer detail for save the rate 
    '''
    def get(self, request, pk=None):
        serviceByList = ServiceProvider.objects.all().order_by('-id').values()
        customerList = Customer.objects.all().order_by('-id').values()
        # serializedData = LedgerSerializer(ledgerList, many=True)
        return Response({"serviceByList": serviceByList, "customerList": customerList})
    

"""
GET THE GENERATED BILL LIST
"""
class BillListApiView(APIView):
    '''
    Get all records of Bill
    '''
    def post(self, request, status=None) :
        # if status == "Paid" :
        #     billList = Bill.objects.filter(is_paid=True).order_by('-id')
        # else :
        #     billList = Bill.objects.filter(is_paid=False).order_by('-id')
        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        # billList = Bill.objects.all().order_by('-id')

        billList = []

        if searchText:
            billList=Bill.objects.filter(Q(customer_id__customer_name__icontains=searchText) | Q(customer_id__company_name__icontains=searchText))
        else:
            billList = Bill.objects.all().order_by('-id')

        billListCount=billList.count()
        paginator = Paginator(billList, listPerPage)
        filteredCutomerList = paginator.page(currentPage)
        
        billSerializer = BillSerializer(filteredCutomerList, many=True)

        return Response({"billList": billSerializer.data, "billListCount": billListCount})


"""
GET BILL DETAIL AND DOWNLOAD THE GENERATED BILL ORDERS
"""
class GetBillApiView(APIView):
    '''
    Get all record of bill like no. of orders
    '''
    def post(self, request, pk=None) :
        billID = pk
        if billID :
            billObj = Bill.objects.get(id=billID)
            if billObj :
                customerDetail = Customer.objects.get(id=billObj.customer_id.id)
                customerSerializer = CustomerSerializer(customerDetail)

                # orderList = Order.objects.filter(
                #     customer_id=billObj.customer_id,
                #     shipment_date__range=[billObj.start_date, billObj.end_date],
                #     order_status="Billed"
                # )

                orderList = Order.objects.filter(bill_id=billID)

                total_order_amount = billObj.bill_amount
                orderCount = orderList.count()
                b2bCount = orderList.filter(order_mode="B2B").count()
                b2cCount = orderList.filter(order_mode="B2C").count()

                print(orderList, "orderList")

                serializedData = OrderSaveSerializer(orderList, many=True)

                return Response({
                    "orderCount": orderCount,
                    "b2bCount": b2bCount,
                    "b2cCount": b2cCount,
                    "basic_amount": billObj.basic_amount,
                    "total_order_amount": billObj.bill_amount,
                    "orders": serializedData.data,
                    "customerDetail": customerSerializer.data
                })
        else :
            return Response({"error": "Bill not Selected! Please Check Your Data"})
   

"""
get the order detail with list 
"""
class GetOrderDetailAPI(APIView) :
    '''
    Get all records of Order with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']
        
        orderStatus = request.data['order_status']

        orderList = []

        if searchText:
            orderList=Order.objects.filter(Q(customer_id__customer_name__icontains=searchText) | Q(customer_id__company_name__icontains=searchText) | 
                                           Q(awb_no__icontains=searchText)
            )
        else:
            orderList = Order.objects.all().order_by('-id')

        if orderStatus == "All" :
            pass
        else :
            orderList = orderList.filter(order_status=orderStatus).order_by('-id')

        orderListCount=orderList.count()
        paginator = Paginator(orderList, listPerPage)
        filteredOrderList = paginator.page(currentPage)
        
        orderSerializer = OrderSaveSerializer(filteredOrderList, many=True)

        return Response({"orderList": orderSerializer.data, "orderListCount": orderListCount})
    

"""
get the cod order detail with list 
"""
class GetCodOrderDetailAPI(APIView) :
    '''
    Get all records of COD Order with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']
        
        # orderStatus = request.data['order_status']

        orderList = []

        if searchText:
            orderList=Order.objects.filter(payment_mode="COD", shipment_status="DELIVERED").filter(Q(customer_id__customer_name__icontains=searchText) | Q(customer_id__company_name__icontains=searchText) | 
                                           Q(awb_no__icontains=searchText)
            ).order_by('-id')
        else:
            orderList = Order.objects.filter(payment_mode="COD", shipment_status="DELIVERED").order_by('-id')

        totalCodShipment = Order.objects.filter(payment_mode="COD", shipment_status="DELIVERED").order_by('-id')

        remittanceValue = dict()
        if orderList.count() > 0 :
            total_cod_remittance = totalCodShipment.aggregate(total_cod_remittance=Sum('invoice_value'))
            balance_cod_remittance = totalCodShipment.aggregate(balance_cod_remittance=Sum('balance_cod_amount'))
            cod_remitted = Decimal(total_cod_remittance['total_cod_remittance']) - Decimal(balance_cod_remittance['balance_cod_remittance'])

            remittanceValue.update({
                'total_cod_remittance': total_cod_remittance['total_cod_remittance'],
                'balance_cod_remittance': balance_cod_remittance['balance_cod_remittance'],
                'cod_remitted': cod_remitted
            })
        # remittanceValue = {
        #     'total_cod_remittance': total_cod_remittance['total_cod_remittance'],
        #     'balance_cod_remittance': balance_cod_remittance['balance_cod_remittance'],
        #     'cod_remitted': cod_remitted
        # }


        # if orderStatus == "All" :
        #     pass
        # else :
        #     orderList = orderList.filter(order_status=orderStatus).order_by('-id')

        orderListCount=orderList.count()
        paginator = Paginator(orderList, listPerPage)
        filteredOrderList = paginator.page(currentPage)
        
        orderSerializer = OrderSaveSerializer(filteredOrderList, many=True)

        return Response({"orderList": orderSerializer.data, "orderListCount": orderListCount, 'remittanceDetail': remittanceValue})
    

"""
get the cash booking detail with list 
"""
class GetCashBookingDetailAPI(APIView) :
    '''
    Get all records of cash booking with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        filterCriteria = request.data["filterCriteria"]
        
        orderStatus = request.data['order_status']

        cashBookingList = CashBooking.objects.all()

        # if 'counter' in filterCriteria and 'startDate' in filterCriteria and 'endDate' in filterCriteria :
        #     cashBookingList=CashBooking.objects.filter(Q(counter=filterCriteria["counter"]) & Q(shipment_date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
        # elif 'counter' in filterCriteria :
        #     cashBookingList=CashBooking.objects.filter(Q(counter=filterCriteria["counter"]))
        # elif 'startDate' in filterCriteria and 'endDate' in filterCriteria :
        #     cashBookingList=CashBooking.objects.filter(Q(shipment_date__range=(filterCriteria['startDate'], filterCriteria['endDate'])))
        # else :
        #     cashBookingList = CashBooking.objects.all().order_by('-id')

        # Build the filter conditions
        filter_conditions = Q()  # Initialize an empty Q object

        if 'counter' in filterCriteria:
            print('counter')
            filter_conditions &= Q(counter=filterCriteria['counter'])

        if 'mode' in filterCriteria:
            print("mode", filterCriteria['mode'])
            filter_conditions &= Q(mode=filterCriteria['mode'])

        if 'startDate' in filterCriteria and 'endDate' in filterCriteria:
            print("dates")
            filter_conditions &= Q(shipment_date__range=(filterCriteria['startDate'], filterCriteria['endDate']))

        # Apply the filter conditions if any are present
        if filter_conditions:
            cashBookingList = cashBookingList.filter(filter_conditions)


        if searchText:
            cashBookingList=cashBookingList.filter(Q(customer_name__icontains=searchText) | Q(awb_no__icontains=searchText) | Q(mode__icontains=searchText))
        else:
            cashBookingList = cashBookingList.order_by('-id')

        if orderStatus == "All" :
            pass
        else :
            cashBookingList = cashBookingList.filter(order_status=orderStatus).order_by('-id')

        cashBookingListCount=cashBookingList.count()
        paginator = Paginator(cashBookingList, listPerPage)
        filteredCashBookingList = paginator.page(currentPage)
        
        orderSerializer = CashBookingSerializer(filteredCashBookingList, many=True)

        return Response({"cashBookingList": orderSerializer.data, "cashBookingListCount": cashBookingListCount})


"""
Api to integrate crud operation in zones
"""
class ZoneApiView(APIView):
    def post(self,request):
        print(request.data)
        states = request.data["states"]
        # Use a list to store validated instances
        zoneErrors = []
        if len(states) > 0 :
            for state in states :
                zones = Zone.objects.filter(zone=request.data["zone"], state=state)
                print(zones, "sdfghj")
                if (len(zones) > 0): 
                    print("ppppp")
                    zoneErrors.append({"index":states.index(state)+1, "state": state, "error": "Data Already Given"})
                else :
                    print("nnnn")
                    data = {"zone": request.data["zone"], "state": state}
                    serializedData = ZoneSerializer(data=data)
                    if serializedData.is_valid():
                        serializedData.save()
                    else :
                        zoneErrors.append({"index":states.index(state)+1, "state": state, "error": serializedData.errors})
            if len(zoneErrors) > 0 :
                return Response({'info':'Saved and Errors', "zoneErrors": zoneErrors})
            else :
                return Response({'success':'successfully data saved'})
        else :
            return Response({'error':'States not Exist! Please Check Your Data'})
        

"""
Api to integrate crud operation in b2c zones
"""
class B2CZoneApiView(APIView):
    def post(self,request):
        print(request.data)
        states = request.data["states"]
        # Use a list to store validated instances
        zoneErrors = []
        if len(states) > 0 :
            for state in states :
                zones = B2CZone.objects.filter(zone=request.data["zone"], state=state)
                print(zones, "sdfghj")
                if (len(zones) > 0): 
                    print("ppppp")
                    zoneErrors.append({"index":states.index(state)+1, "state": state, "error": "Data Already Given"})
                else :
                    print("nnnn")
                    data = {"zone": request.data["zone"], "state": state}
                    serializedData = B2CZoneSerializer(data=data)
                    if serializedData.is_valid():
                        serializedData.save()
                    else :
                        zoneErrors.append({"index":states.index(state)+1, "state": state, "error": serializedData.errors})
            if len(zoneErrors) > 0 :
                return Response({'info':'Saved and Errors', "zoneErrors": zoneErrors})
            else :
                return Response({'success':'successfully data saved'})
        else :
            return Response({'error':'States not Exist! Please Check Your Data'})
        
        

"""
get the zones detail with list 
"""
class GetZoneDetailsAPI(APIView) :
    '''
    Get all records of Zones with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        zoneList = []

        if searchText:
            zoneList=Zone.objects.filter(Q(state__icontains=searchText) | Q(zone__icontains=searchText)).order_by('-id')
        else:
            zoneList = Zone.objects.all().order_by('-id')

        zoneListCount=zoneList.count()
        paginator = Paginator(zoneList, listPerPage)
        filteredZonesList = paginator.page(currentPage)
        
        zoneSerializer = ZoneSerializer(filteredZonesList, many=True)

        return Response({"zoneList": zoneSerializer.data, "zoneCounts": zoneListCount})
    

"""
get the b2c zones detail with list 
"""
class GetB2CZoneDetailsAPI(APIView) :
    '''
    Get all records of B2C Zones with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        zoneList = []

        if searchText:
            zoneList=B2CZone.objects.filter(Q(state__icontains=searchText) | Q(zone__icontains=searchText)).order_by('-id')
        else:
            zoneList = B2CZone.objects.all().order_by('-id')

        zoneListCount=zoneList.count()
        paginator = Paginator(zoneList, listPerPage)
        filteredZonesList = paginator.page(currentPage)
        
        zoneSerializer = B2CZoneSerializer(filteredZonesList, many=True)

        return Response({"zoneList": zoneSerializer.data, "zoneCounts": zoneListCount})
        

"""
Api to integrate crud operation in quotation
"""
class QuotationApiView(APIView):
    def post(self,request):
        print(request.data)
        rates = request.data["rates"]
        # Use a list to store errors instances
        existingQuotation = []
        rateErrors = []
        if len(rates) > 0 :
            for rate in rates :
                quotations = Quotation.objects.filter(customer_id=request.data["customer_id"], from_zone=rate["from_zone"], service_by=request.data["service_by"]).values()
                if len(quotations) > 0 :
                    existingQuotation.append(quotations[0])
                else :
                    rate.update({"customer_id": request.data["customer_id"], "service_by": request.data["service_by"]})
                    print(rate)
                    serializedData = QuotationSerializer(data=rate)
                    if serializedData.is_valid() :
                        serializedData.save()
                    else :
                        rateErrors.append({"from_zone":rate["from_zone"], "error": serializedData.errors})
            if len(rateErrors) > 0 :
                return Response({'info':'Saved and Errors', "rateErrors": rateErrors, "existingQuotation": existingQuotation})
            else :
                return Response({'success':'successfully data saved', "existingQuotation": existingQuotation})
        else :
            return Response({'dataError':'Rate You have not Given! Please Enter Your Rate'})
        
    def put(self, request, pk=None) :
        if pk is not None :
            quotationObj = Quotation.objects.get(id=request.data["id"])
            if quotationObj :
                quotationSerializer = QuotationSerializer(quotationObj, request.data)
                if quotationSerializer.is_valid() :
                    quotationSerializer.save()
                    return Response({'success': "Data Saved Successfully"})
                else :
                    return Response({'error':quotationSerializer.errors})
            else :
                return Response({'error':'Data not Selected! Please Try Again'})
        else :
            return Response({'error':'Data not Selected! Please Try Again'})

        

"""
Api to integrate crud operation in b2c quotation
"""
class B2CQuotationApiView(APIView):
    def post(self,request):
        print(request.data)
        rates = request.data["rates"]
        # Use a list to store errors instances
        existingQuotation = []
        rateErrors = []
        if len(rates) > 0 :
            for rate in rates :

                quotations = B2CQuotation.objects.filter(customer_id=request.data["customer_id"], deliver_mode=request.data["deliver_mode"], service_by=request.data["service_by"], from_zone=request.data["from_zone"], weight=rate["weight"])
                b2cQuotations = B2CQuotationSerializer(quotations, many=True)

                if len(b2cQuotations.data) > 0 :
                    existingQuotation.append(b2cQuotations.data[0])
                else :
                    rate.update({"customer_id": request.data["customer_id"], "service_by": request.data["service_by"], "deliver_mode": request.data["deliver_mode"], "from_zone": request.data["from_zone"]})
                    serializedData = B2CQuotationSerializer(data=rate)
                    if serializedData.is_valid() :
                        serializedData.save()
                    else :
                        rateErrors.append({"weight":rate["weight"], "error": serializedData.errors})
            if len(rateErrors) > 0 :
                return Response({'info':'Saved and Errors', "rateErrors": rateErrors, "existingQuotation": existingQuotation})
            else :
                return Response({'success':'successfully data saved', "existingQuotation": existingQuotation})
        else :
            return Response({'dataError':'Rate You have not Given! Please Enter Your Rate'})
        
    def put(self, request, pk=None) :
        if pk is not None :
            quotationObj = B2CQuotation.objects.get(id=request.data["id"])
            if quotationObj :
                quotationSerializer = B2CQuotationSerializer(quotationObj, request.data)
                if quotationSerializer.is_valid() :
                    quotationSerializer.save()
                    return Response({'success': "Data Saved Successfully"})
                else :
                    return Response({'error':quotationSerializer.errors})
            else :
                return Response({'error':'Data not Selected! Please Try Again'})
        else :
            return Response({'error':'Data not Selected! Please Try Again'})
        

"""
get the quotation detail with list 
"""
class GetQuotationDetailsAPI(APIView) :
    '''
    Get all records of Quotations with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        quotationList = []

        if searchText:
            quotationList=Quotation.objects.filter(Q(customer_id__company_name__icontains=searchText) | Q(customer_id__customer_name__icontains=searchText)).order_by('-id')
        else:
            quotationList = Quotation.objects.all().order_by('-id')

        quotationListCount=quotationList.count()
        paginator = Paginator(quotationList, listPerPage)
        filteredQuotationsList = paginator.page(currentPage)
        
        zoneSerializer = QuotationSerializer(filteredQuotationsList, many=True)

        return Response({"quotationList": zoneSerializer.data, "quotationCounts": quotationListCount})
    

"""
get the b2c quotation detail with list 
"""
class GetB2CQuotationDetailsAPI(APIView) :
    '''
    Get all records of b2c Quotations with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']
        # customerID=request.data['customerID']
        # serviceByID=request.data['serviceByID']

        quotationList = []

        # if customerID and serviceByID:
        #     quotationList=B2CQuotation.objects.filter(Q(customer_id=customerID) & Q(service_by=serviceByID)).order_by('-id')
        # else:
        #     quotationList = B2CQuotation.objects.all().order_by('-id')

        if searchText:
            quotationList=B2CQuotation.objects.filter(Q(customer_id__company_name__icontains=searchText) | Q(customer_id__customer_name__icontains=searchText)).order_by('-id')
        else:
            quotationList = B2CQuotation.objects.all().order_by('-id')

        quotationListCount=quotationList.count()
        paginator = Paginator(quotationList, listPerPage)
        filteredQuotationsList = paginator.page(currentPage)
        
        zoneSerializer = B2CQuotationSerializer(filteredQuotationsList, many=True)

        return Response({"quotationList": zoneSerializer.data, "quotationCounts": quotationListCount})
    

"""
Api to integrate crud operation in setting
"""
class SettingApiView(APIView):
    def post(self,request):
        if "id" in request.data :
            settingObj = Setting.objects.get(id=request.data["id"])
            serializedData = SettingSerializer(settingObj, data=request.data)
        else :
            serializedData = SettingSerializer(data=request.data)
        if serializedData.is_valid():
            serializedData.save()
            settingData = Setting.objects.all().values()[0]
            return Response({'success': 'Data Updated Seccessfully', "settingData": settingData})
        else :
            return Response({'error': serializedData.data})
        
    def get(self, format=None) :
        settingDatas = Setting.objects.all().values()
        if len(settingDatas) > 0 :
            return Response({"settingData": settingDatas[0]})
        else :
            return Response({"settingData": {}})


"""
To get the quotation format row data
"""
class QuotationFormatAPI(APIView):
    '''
    Get all record of Customer and and their rate
    '''
    def post(self, request):
        QuotationList = Quotation.objects.filter(customer_id=request.data["customer_id"], service_by=request.data["service_id"]).order_by('-id')
        quotationSerializers = QuotationSerializer(QuotationList, many=True)

        ZoneList = Zone.objects.all().order_by('-id')
        zoneSerializersData = ZoneSerializer(ZoneList, many=True)

        customerObj = Customer.objects.get(id=request.data["customer_id"])
        customerSerializer = CustomerSerializer(customerObj)

        # settingObj = Setting.objects.all().first()
        # settingSerializer = SettingSerializer(settingObj)

        shipmentChargesObj = ShipmentCharges.objects.filter(customer_id=request.data["customer_id"], service_by=request.data["service_id"], order_mode=request.data["order_mode"]).first()
        shipmentChargesSerializer = ShipmentChargesSerializer(shipmentChargesObj)
        
        return Response({
            "quotationList": quotationSerializers.data,
            "zoneList": zoneSerializersData.data,
            "customerData": customerSerializer.data,
            "shipmentChargesData": shipmentChargesSerializer.data
        })


"""
To get the b2c quotation format row data
"""
class B2CQuotationFormatAPI(APIView):
    '''
    Get all record of Customer and and their rate from b2c quotation
    '''
    def post(self, request):
        print(request.data, "sdfghjk")
        QuotationList = B2CQuotation.objects.filter(customer_id=request.data["customer_id"], service_by=request.data["service_id"], from_zone="WITHIN ZONE").order_by('weight')
        quotationSerializers = B2CQuotationSerializer(QuotationList, many=True)

        ZoneList = B2CZone.objects.all().order_by('-id')
        zoneSerializersData = B2CZoneSerializer(ZoneList, many=True)

        customerObj = Customer.objects.get(id=request.data["customer_id"])
        customerSerializer = CustomerSerializer(customerObj)

        # settingObj = Setting.objects.all().first()
        # settingSerializer = SettingSerializer(settingObj)

        shipmentChargesObj = ShipmentCharges.objects.filter(customer_id=request.data["customer_id"], service_by=request.data["service_id"], order_mode=request.data["order_mode"]).first()
        shipmentChargesSerializer = ShipmentChargesSerializer(shipmentChargesObj)
        
        return Response({
            "quotationList": quotationSerializers.data,
            "zoneList": zoneSerializersData.data,
            "customerData": customerSerializer.data,
            "shipmentChargesData": shipmentChargesSerializer.data
        })
        

"""
get the customer detail with list 
"""
class GetCustomerDetailsAPI(APIView) :
    '''
    Get all records of Customers with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        customerList = []

        if searchText:
            customerList=Customer.objects.filter(Q(company_name__icontains=searchText) | Q(customer_name__icontains=searchText) | Q(gst_no__icontains=searchText) | Q(state__icontains=searchText)).order_by('-id')
        else:
            customerList = Customer.objects.all().order_by('-id')

        customerListCount=customerList.count()
        paginator = Paginator(customerList, listPerPage)
        filteredCustomersList = paginator.page(currentPage)
        
        customerSerializer = CustomerSerializer(filteredCustomersList, many=True)

        return Response({"customerList": customerSerializer.data, "customerCounts": customerListCount})
    

"API for having crud operation for b2c quotation"
class QuotationAPI(APIView):
    '''
    Get all records of Frieght Rate
    '''
    def get(self,request):
        frieghtRateList = Quotation.objects.all().order_by('date_create_at')
        serializedData = GetFrieghtRateSerializer(frieghtRateList, many=True)
        return Response({"frieghtRateList": serializedData.data})

    '''
    create new Frieght Rate record
    '''
    def post(self,request):
        if "id" in request.data :
            frObj = Quotation.objects.get(id = request.data.get("id"))
            serializedData = QuotationSerializer(frObj, data=request.data)
        else :
            serializedData = QuotationSerializer(data=request.data)
        frieghtRateList = Quotation.objects.all().order_by('date_create_at')
        getFrieghtRateSerializers = QuotationSerializer(frieghtRateList, many=True)
        if serializedData.is_valid():
            serializedData.save()
            return Response({"successMsg": "Saved Successfully", "frieghtRateList": getFrieghtRateSerializers.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    

"""
API for having crud operation for Shipment Charges
"""
class ShipmentChargesAPI(APIView):
    '''
    update the shipment charges
    '''
    def post(self,request):
            if "id" in request.data :
                shipmentChargesObj = ShipmentCharges.objects.get(id = request.data.get("id"))
                serializedData = ShipmentChargesSerializer(shipmentChargesObj, data=request.data)
            else :
                chagesExistance = ShipmentCharges.objects.filter(customer_id = request.data.get("customer_id"), service_by=request.data.get("service_by"), order_mode=request.data.get("order_mode"))
                if len(chagesExistance) > 0 :
                    return Response({"duplicate": "Data Already Exist"})
                serializedData = ShipmentChargesSerializer(data=request.data)
            if serializedData.is_valid() :
                serializedData.save()
                return Response({"success": "Saved Successfully"}, status=status.HTTP_201_CREATED)
            return Response({"error": serializedData.errors, "errorMsg": "Something Went Wrong"})
    

"""
get the shipment charges detail with list 
"""
class GetShipmentChargesAPI(APIView) :
    '''
    Get all records of shipment charges with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']
        order_mode=request.data['order_mode']

        shipmentChargesList = []

        if searchText:
            shipmentChargesList=ShipmentCharges.objects.filter(Q(order_mode=order_mode) & Q(customer_id__customer_name__icontains=searchText) | Q(service_by__name__icontains=searchText)).order_by('-id')
        else :
            shipmentChargesList = ShipmentCharges.objects.filter(Q(order_mode=order_mode)).order_by('-id')

        shipmentChargesListCount=shipmentChargesList.count()
        paginator = Paginator(shipmentChargesList, listPerPage)
        filteredshipmentChargesList = paginator.page(currentPage)
        
        chragesSerializer = ShipmentChargesSerializer(filteredshipmentChargesList, many=True)

        return Response({"shipmentChargesList": chragesSerializer.data, "shipmentChargesCounts": shipmentChargesListCount})
    

"""
get the payment detail with list 
"""
class GetPaymentDetailAPI(APIView) :
    '''
    Get all records of Payment with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        paymentList = []

        if searchText:
            paymentList=Payment.objects.filter(Q(customer_id__customer_name__icontains=searchText) | Q(customer_id__company_name__icontains=searchText)).order_by('-id')
        else:
            paymentList = Payment.objects.all().order_by('-id')

        paymentListCount=paymentList.count()
        paginator = Paginator(paymentList, listPerPage)
        filteredPaymentList = paginator.page(currentPage)
        
        paymentSerializer = PaymentSerializer(filteredPaymentList, many=True)

        return Response({"paymentList": paymentSerializer.data, "paymentListCount": paymentListCount})
    

"""
get the cod payment detail with list 
"""
class GetCodPaymentDetailAPI(APIView) :
    '''
    Get all records of Cod Payment with pagination detail
    '''
    def post(self, request) :

        paginationDetails=request.data['paginationDetails']
        currentPage=paginationDetails['currentPage']
        listPerPage=paginationDetails['listPerPage']
        searchText=request.data['searchText']

        paymentList = []

        if searchText:
            paymentList=CodPayment.objects.filter(Q(customer_id__customer_name__icontains=searchText) | Q(customer_id__company_name__icontains=searchText)).order_by('-id')
        else:
            paymentList = CodPayment.objects.all().order_by('-id')

        paymentListCount=paymentList.count()
        paginator = Paginator(paymentList, listPerPage)
        filteredPaymentList = paginator.page(currentPage)
        
        paymentSerializer = CodPaymentSerializer(filteredPaymentList, many=True)

        return Response({"paymentList": paymentSerializer.data, "paymentListCount": paymentListCount})