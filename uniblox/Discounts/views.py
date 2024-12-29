from django.conf import settings
from uniblox.utils.db import run_sql_query
from .models import Discount
from rest_framework.views import APIView
from .serializers import DiscountSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

class DiscountService:
    def __init__(self):
        pass

    """
    Create a discount for a user
    """
    def create_discount(self, user_id, percentage):
        user = User.objects.get(id=user_id)
        discount = Discount(discount_code="UNI10", discount_percentage=percentage, user_id=user, status=False)
        discount.save()

    """
    Get total number of transactions for a user
    """
    def get_total_customer_transactions(self, user_id):
        query = f"""
            SELECT COUNT(DISTINCT(transaction_id)) 
            FROM Orders_orders 
            WHERE user_id_id={user_id}
        """
        results = run_sql_query(query)
        return results[0][0]

    """
    Check if a discount is to be created for a user after a transaction
    """
    def check_and_create_discount(self, user_id):
        total_transactions = self.get_total_customer_transactions(user_id)
        if (total_transactions+1) % settings.DISCOUNT_STEP == 0:        # For every nth order, discount is applied
            self.create_discount(1, settings.NTH_ORDER_DISCOUNT)

    """
    Sets a discount as inactive after it has been used
    """
    def set_discount_inactive(self, discount_id):
        query = f"""
            UPDATE Discounts_discount
            SET status=1
            WHERE discount_id={discount_id}
        """
        run_sql_query(query)

class DiscountView(APIView):
    """
    Gets all discounts or a specific discount by coupon code
    """
    def get(self, request):
        coupon_code = request.query_params.get('couponCode', None)
        if coupon_code:
            try:
                discount = Discount.objects.get(discount_code=coupon_code, status=False)
                serializer = DiscountSerializer(discount)
                return JsonResponse(serializer.data, safe=False)
            except Discount.DoesNotExist:
                return JsonResponse({"error": "Discount not found"}, status=404)
            

        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    """
    Creates a discount for a user, given the eamail, discount code and discount percentage
    """
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        data = {
            "discount_code": request.data.get("discount_code"),
            "discount_percentage": request.data.get("discount_percentage"),
            "user_id": user.id,
            "status": False,
        }
        serializer = DiscountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=201)
        return JsonResponse(serializer.errors, status=400)
    
"""
Get all discounts and applied discounts for Admin Summary
"""
@api_view(['GET'])
@csrf_exempt
def get_admin_discounts(request):
    try:
        query = """
            SELECT discount_id, discount_code, discount_percentage, email, status
            FROM `Discounts_discount` AS d
            JOIN `auth_user` AS u ON u.id=d.user_id_id
        """
        results = run_sql_query(query)
        all_discounts = []
        for result in results:
            all_discounts.append({
                "discount_id": result[0],
                "discount_code": result[1],
                "discount_percentage": result[2],
                "email": result[3],
                "status": result[4]
            })

        query = """
            SELECT discount_code, discount_percentage, email, order_total, transaction_id
            FROM `Discounts_discount` AS d
            JOIN `Orders_orders` AS o ON d.discount_id=o.discount_id_id
            JOIN `auth_user` AS u ON u.id=o.user_id_id
        """
        results = run_sql_query(query)
        applied_discount_data = []
        for result in results:
            applied_discount_data.append({
                "discount_code": result[0],
                "discount_percentage": result[1],
                "email": result[2],
                "order_total": result[3],
                "transaction_id": result[4],
            })

        data = {
            "discounts": all_discounts,
            "applied_discounts": applied_discount_data
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=400)