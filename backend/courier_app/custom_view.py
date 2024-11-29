from courier_app.models import Order, Customer, ShipmentCharges

def b2bOrderSave(order, quotationData, from_zone, to_zone, fromCityQuery, toCityQuery, shipmentChargesObj):
    # customerObj = Customer.objects.filter(id=order["customer_id"]).first()

# commented for not add this shipment for billing time only
    # if (order["payment_mode"] == "TO PAY") and (order["shipment_status"] == "IN TRANSIT" or order["shipment_status"] == "DELIVERED") :
    #     totalAmount = 0.0
    #     basicAmount = 0.0
    # else :
# end of comment on 10.05.2024

    if order['mannual_frieght'] or order['mannual_frieght'] > 0 :
        totalAmount = order['mannual_frieght']
        basicAmount = order['mannual_frieght']
    else :
        if order["order_mode"].upper() == "B2B" and quotationData :

            if order["charged_weight"] < shipmentChargesObj.min_charge_weight :
                order.update({'charged_weight': shipmentChargesObj.min_charge_weight})

            if to_zone == "N1" :
                basicAmount = order["charged_weight"]*quotationData.n1_rate
            elif to_zone == "N2" :
                basicAmount = order["charged_weight"]*quotationData.n2_rate
            elif to_zone == "S1" :
                basicAmount = order["charged_weight"]*quotationData.s1_rate
            elif to_zone == "S2" :
                basicAmount = order["charged_weight"]*quotationData.s2_rate
            elif to_zone == "E" :
                basicAmount = order["charged_weight"]*quotationData.e_rate
            elif to_zone == "NE" :
                basicAmount = order["charged_weight"]*quotationData.ne_rate
            elif to_zone == "W1" :
                basicAmount = order["charged_weight"]*quotationData.w1_rate
            elif to_zone == "W2" :
                basicAmount = order["charged_weight"]*quotationData.w2_rate
            elif to_zone == "CENTRAL" :
                basicAmount = order["charged_weight"]*quotationData.central_rate
            # elif to_zone == "SPECIAL DESTINATION" :
            #     basicAmount = order["charged_weight"]*quotationData.special_dest_rate
            else :
                basicAmount = 0

            totalAmount = basicAmount

            totalAmount = totalAmount + (totalAmount*shipmentChargesObj.fsc)/100
            fovValue = (order["invoice_value"]*shipmentChargesObj.fov)/100
            if fovValue > shipmentChargesObj.min_fov :
                totalAmount = totalAmount + fovValue
            else :
                totalAmount = totalAmount + shipmentChargesObj.min_fov

            if order["shipment_status"] == "RTO IN TRANSIT" or order["shipment_status"] == "RTO DELIVERED" :
                totalAmount = totalAmount*2
            else :
                if order["payment_mode"] != "PREPAID" :
                    codValue = (order["invoice_value"]*shipmentChargesObj.cod_to_pay_charge)/100
                    if codValue > shipmentChargesObj.min_cod_to_pay_charge :
                        totalAmount = totalAmount + codValue
                    else :
                        totalAmount = totalAmount + shipmentChargesObj.min_cod_to_pay_charge
            
            totalAmount = totalAmount + shipmentChargesObj.docket

        elif order["order_mode"].upper() == "B2C" and quotationData :

            if from_zone == to_zone and fromCityQuery == toCityQuery :
                basicAmount = order["charged_weight"]*quotationData.within_city_rate
            elif to_zone == "SPECIAL DESTINATION" :
                basicAmount = order["charged_weight"]*quotationData.special_destination_rate
            elif to_zone == "WITHIN ZONE" :
                basicAmount = order["charged_weight"]*quotationData.within_zone_rate
            elif to_zone == "REST OF INDIA" :
                basicAmount = order["charged_weight"]*quotationData.rest_india_rate
            elif to_zone == "METRO" :
                basicAmount = order["charged_weight"]*quotationData.metro_rate
            else : 
                basicAmount = 0

            totalAmount = basicAmount

            totalAmount = totalAmount + (totalAmount*shipmentChargesObj.fsc)/100

            fovValue = (order["invoice_value"]*shipmentChargesObj.fov)/100
            if fovValue > shipmentChargesObj.min_fov :
                totalAmount = totalAmount + fovValue
            else :
                totalAmount = totalAmount + shipmentChargesObj.min_fov

            totalAmount = totalAmount + shipmentChargesObj.docket
        
            if order["shipment_status"] == "RTO IN TRANSIT" or order["shipment_status"] == "RTO DELIVERED" :
                totalAmount = totalAmount*2
            else :
                codValue = (order["invoice_value"]*shipmentChargesObj.cod_to_pay_charge)/100
                if codValue > shipmentChargesObj.min_cod_to_pay_charge :
                    totalAmount = totalAmount + codValue
                else :
                    totalAmount = totalAmount + shipmentChargesObj.min_cod_to_pay_charge

    round(totalAmount, 2)
    order.update({"basic_amount":basicAmount})
    order.update({"freight_amount": totalAmount})
    
    return order