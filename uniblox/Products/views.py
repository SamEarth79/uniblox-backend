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
        
        # Get the latest discount (currently not handling multiple discounts)
        try:
            discount = Discount.objects.filter(user_id=1, status=False).latest('discount_id')
            discount_serializer = DiscountSerializer(discount)
            discount_data = discount_serializer.data
        except Discount.DoesNotExist:
            discount_data = None
                 
        
        data = {
            "products": serializer.data,
            "discount": discount_data
        }
        return JsonResponse(data, safe=False)