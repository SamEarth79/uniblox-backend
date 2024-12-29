from django.shortcuts import render
from rest_framework.views import APIView

from uniblox.utils.db import run_sql_query
from .models import Product
from .serializers import ProductSerializer
from django.http import JsonResponse
from Discounts.models import Discount
from Discounts.serializers import DiscountSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ProductView(APIView):
    """
    Get all products for product page along with available coupons
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        # Get the latest discount (currently not handling multiple discounts)
        try:
            available_discounts = Discount.objects.filter(user_id=1, status=False).values('discount_code')
            discount_data = []
            for discount in available_discounts:
                discount_data.append(discount.get('discount_code'))
            
        except Exception as e:
            print(str(e))
            discount_data = []
        
        data = {
            "products": serializer.data,
            "discount": discount_data
        }
        return JsonResponse(data, safe=False)

"""
Get all products and their sales for Admin Summary
"""
@api_view(['GET'])
@csrf_exempt
def get_admin_products(request):
    try:
        query = """
            SELECT product_id, product_name, COUNT(order_id), SUM(order_qty) AS total_ordered_qty, SUM(order_total)
            FROM `Orders_orders` as o 
            JOIN `Products_product` AS p ON o.product_id_id=p.product_id
            GROUP BY product_id
            ORDER BY total_ordered_qty DESC
        """
        results = run_sql_query(query)
        products_data = []
        for result in results:
            product_data = {
                "product_id": result[0],
                "product_name": result[1],
                "total_orders": result[2],
                "total_ordered_qty": result[3],
                "total_sales": result[4],
            }
            products_data.append(product_data)
        return JsonResponse(products_data, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=400)