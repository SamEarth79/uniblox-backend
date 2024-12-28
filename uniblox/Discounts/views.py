from django.conf import settings
from django.shortcuts import render

from uniblox.utils.db import run_sql_query
from .models import Discount
from rest_framework.views import APIView
from .serializers import DiscountSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User

def create_discount_after_nth_order(user_id):
    user = User.objects.get(id=user_id)
    discount = Discount(discount_code="UNI10", discount_percentage=10, user_id=user, status=False)
    discount.save()

def get_total_customer_transactions(user_id):
    query = f"""
        SELECT COUNT(DISTINCT(transaction_id)) 
        FROM Orders_orders 
        WHERE user_id_id={user_id}
    """
    results = run_sql_query(query)
    return results[0][0]

def check_and_create_discount(user_id):
    total_transactions = get_total_customer_transactions(user_id)
    if (total_transactions+1) % settings.DISCOUNT_STEP == 0:        # For every nth order, discount is applied
        create_discount_after_nth_order(1)

def set_discount_inactive(discount_id):
    query = f"""
        UPDATE Discounts_discount
        SET status=1
        WHERE discount_id={discount_id}
    """
    run_sql_query(query)

class DiscountView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return JsonResponse(serializer.data, safe=False)