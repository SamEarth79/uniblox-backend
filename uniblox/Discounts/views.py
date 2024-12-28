from django.shortcuts import render
from .models import Discount
from rest_framework.views import APIView
from .serializers import DiscountSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User

def create_discount_after_nth_order(user_id):
    user = User.objects.get(id=user_id)
    discount = Discount(discount_code="UNI10", discount_percentage=10, user_id=user, status=False)
    discount.save()

class DiscountView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return JsonResponse(serializer.data, safe=False)