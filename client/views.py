from datetime import datetime

from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from company.models import CarParts
from company.serializers import CarPartsSerializer
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer


class ClientApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_part_id=None, *args, **kwargs):
        """An overview of all the products or if car part id mention then give specific part details"""
        if car_part_id:
            car_part = CarParts.objects.filter(id=car_part_id).values()[0]
            serializer = CarPartsSerializer(data=car_part)
        else:

            car_parts = CarParts.objects.values()
            paginator = Paginator(car_parts, 10)
            page = request.GET.get('page')
            paged_cars = paginator.get_page(page)

            data = {'car_parts': list(paged_cars)}
            serializer = CarPartsSerializer(data=data.get('car_parts'), many=True)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """Add items to the cart"""
        car_part_id = request.data.get('part_id')
        data = {'quantity': request.data.get('quantity'), 'customer': request.user.id,
                'car_part': CarParts.objects.get(id=car_part_id).id}

        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, car_part_id, *args, **kwargs):
        """Deletes the item with given part_id if exists"""
        cart_instance = ShoppingCart.objects.filter(customer=request.user.id,
                                                    car_part=car_part_id).first()
        if not cart_instance:
            return Response(
                {"res": "Object with car part id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_instance.delete()
        return Response(
            {"res": "Cart item deleted!"},
            status=status.HTTP_200_OK
        )

    def patch(self, request, car_part_id, *args, **kwargs):
        """Update delivery date and time with given part_id if exists"""
        cart_instance = ShoppingCart.objects.filter(customer=request.user.id,
                                                    car_part=car_part_id).first()
        if not cart_instance:
            return Response(
                {"res": "Object with car part id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cart_instance.status != 'Purchased':
            return Response(
                {"res": "Object with car part id does not purchased status"},
                status=status.HTTP_409_CONFLICT
            )

        cart_instance.delivery_datetime = datetime.fromtimestamp(request.data.get('delivery_datetime'))
        cart_instance.save()
        return Response(
            {"res": "Cart item updated with delivery datetime!"},
            status=status.HTTP_202_ACCEPTED
        )


class ClientApiPurchasedView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Order the current contents in my shopping cart"""
        cart_instance = ShoppingCart.objects.filter(customer=request.user.id).all()
        if not cart_instance:
            return Response(
                {"res": "Your shopping cart empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        car_part_ids = request.data.get('part_ids')

        for item in cart_instance:
            if item.car_part.id in car_part_ids:
                item.status = 'Purchased'
                item.save()
        return Response(
            {"res": "All selected cart items purchased"},
            status=status.HTTP_202_ACCEPTED
        )
