from rest_framework.views import APIView
import random
import string
from django.http import JsonResponse
from Discounts.views import DiscountService
from uniblox.utils.db import run_sql_query
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

"""
The transaction id is usually derived from payment gateway such as Razorpay if used.
Here I am generating a random transaction id for the sake of this project.
"""
def get_unique_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

"""
Add orders to the database
"""
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
    """
    Get orders summary for admin page
    """
    def get(self, request):
        try:
            query = """
                SELECT transaction_id, order_total, product_name, product_price, order_qty, order_date, discount_id, discount_code, discount_percentage
                FROM `Orders_orders` as o 
                JOIN `Products_product` AS p ON o.product_id_id=p.product_id
                LEFT JOIN `Discounts_discount` AS d ON o.discount_id_id=d.discount_id
                ORDER BY order_id
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
                        "discount": {
                            "discount_id": result[6],
                            "discount_code": result[7],
                            "discount_percentage": result[8]
                        },
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
    
    """
    Place new order/Checkout API
    """
    def post(self, request):
        try:
            new_order_data = request.data.get("new_order_data", None)
            discount = request.data.get("discount", None)
            
            create_orders(new_order_data, discount) 
            
            discount_service = DiscountService()
            if discount:
                discount_service.set_discount_inactive(discount["discount_id"])
            
            discount_service.check_and_create_discount(user_id=1)
            
            return JsonResponse({"message": "Order placed successfully"}, status=201)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
        
"""
Get all discounts and applied discounts for Admin Summary
"""
@api_view(['GET'])
@csrf_exempt
def get_admin_orders(request):
    try:
        query = """
            SELECT id, email, transaction_id, order_total, product_name, product_price, order_qty, order_date, discount_percentage
            FROM `Orders_orders` as o 
            JOIN `Products_product` AS p ON o.product_id_id=p.product_id
            JOIN `auth_user` AS u ON o.user_id_id=u.id
            LEFT JOIN `Discounts_discount` AS d ON o.discount_id_id=d.discount_id
            ORDER BY id, order_id
        """
        results = run_sql_query(query)
        orders_data = []
        for result in results:
            order_data = {
                "id": result[0],
                "email": result[1],
                "transaction_id": result[2],
                "order_total": result[3],
                "product_name": result[4],
                "product_price": result[5],
                "order_qty": result[6],
                "order_date": result[7].strftime("%b %d, %I:%M %p"),
                "discount_percentage": result[8],
            }
            orders_data.append(order_data)
            
        return JsonResponse(orders_data, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=400)


