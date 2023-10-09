from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import CarParts
from django.core.paginator import Paginator

from .serializers import CarPartsSerializer


class CompanyApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Get all the available parts"""
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
        """Add items to the car pats"""
        data = {'car_part_title': request.data.get('car_part_title'), 'color': request.data.get('color'),
                'model': request.data.get('model'), 'year': request.data.get('year'),
                'condition': request.data.get('condition'), 'price': request.data.get('price'),
                'description': request.data.get('description'), 'specifications': request.data.get('specifications'),
                'imported_country': request.data.get('imported_country'), 'quantity': request.data.get('quantity')}

        serializer = CarPartsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
