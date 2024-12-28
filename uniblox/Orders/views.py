from rest_framework.views import APIView
import random
import string
from django.http import JsonResponse
from Discounts.views import check_and_create_discount, set_discount_inactive
from uniblox.utils.db import run_sql_query
from .models import Orders
from .serializers import OrderSerializer

"""
The transaction id is usually derived from payment gateway such as Razorpay if used.
Here I am generating a random transaction id for the sake of this project.
"""
def get_unique_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def create_orders(new_order_data, discount):
    if new_order_data is None:
        raise Exception("No data provided")
    
    transaction_id = get_unique_transaction_id()
    for order in new_order_data:
        data = {
            "user_id": 1,       # For now 1, can be replaced by user_id from request.user_id if authentication is implemented
            "discount_id": discount.get("discount_id") if discount else None,
            "transaction_id": transaction_id,
            "product_id": order.get("product_id"),
            "order_total": order.get("total"),
            "order_qty": order.get("qty"),
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)


class OrdersView(APIView):
    def get(self, request):
        try:
            query = """
                SELECT transaction_id, order_total, product_name, product_price, order_qty, order_date 
                FROM `Orders_orders` as o JOIN `Products_product` AS p
                ON o.product_id_id=p.product_id
                ORDER BY order_id LIMIT 100
            """
            results = run_sql_query(query)
            orders_data = {}
            for result in results:
                transaction_id = result[0]
                if transaction_id not in orders_data:
                    orders_data[transaction_id] = {
                        "transaction_id": transaction_id,
                        "order_total": 0,
                        "order_date": result[5].strftime("%b %d, %I:%M %p"),
                        "products": []
                    }
                orders_data[transaction_id]["order_total"] += result[1]
                orders_data[transaction_id]["products"].append({
                    "product_name": result[2],
                    "product_price": result[3],
                    "order_qty": result[4],
                })
            
                
            return JsonResponse(orders_data, safe=False)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
    
    def post(self, request):
        try:
            new_order_data = request.data.get("new_order_data", None)
            discount = request.data.get("discount", None)
            
            create_orders(new_order_data, discount) 
            
            if discount:
                set_discount_inactive(discount["discount_id"])
            
            check_and_create_discount(user_id=1)
            
            return JsonResponse({"message": "Order placed successfully"}, status=201)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
        
