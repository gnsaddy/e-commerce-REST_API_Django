from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer
from .models import Order
from django.views.decorators.csrf import csrf_exempt


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False

    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({
            'error': 'Plase re-login',
            'code': '500'
        })
    if request.nethod == 'POST':
        user_id = id
        transaction_id = request.POST['transaction_id']
        amout = request.POST['amount']
        products = request.POST['products']

        total_pro = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)

        except UserModel.DoesNotExist:
            return JsonResponse({
                'error': 'User does not exist'
            })

        ordr = Order(user=user, product_name=products,
                     total_products=total_pro, transaction_id=transaction_id, total_amout=amout)

        ordr.save()
        return JsonResponse({
            'success': True,
            'error': False,
            'message': 'Order placed successfully'
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
