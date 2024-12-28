from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from django.http import JsonResponse
from Discounts.models import Discount
from Discounts.serializers import DiscountSerializer

# Create your views here.
class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        discount = Discount.objects.filter(user_id=1, status=False).latest('discount_id')         # Get the latest discount (currently not handling multiple discounts)
        discount_serializer = DiscountSerializer(discount)
        
        data = {
            "products": serializer.data,
            "discount": discount_serializer.data
        }
        return JsonResponse(data, safe=False)