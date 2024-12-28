from django.shortcuts import render
from rest_framework.views import APIView
import random
import string
from django.http import JsonResponse
from .serializers import OrderSerializer

"""
The transaction id is usually derived from payment gateway such as Razorpay if used.
Here I am generating a random transaction id for the sake of this project.
"""
def get_unique_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class OrdersView(APIView):
    def post(self, request):
        try:
            new_order_data = request.data.get("new_order_data", None)
            if new_order_data is None:
                raise Exception("No data provided")
            
            transaction_id = get_unique_transaction_id()
            for order in new_order_data:
                data = {
                    "user_id": 1,       # For now 1, can be replaced by user_id from request.user_id if authentication is implemented
                    # "discount_id": order.get("discount_id"),
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

            return JsonResponse({"message": "Order placed successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
