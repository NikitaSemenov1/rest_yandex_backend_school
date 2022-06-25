from django.http import JsonResponse, HttpResponse, Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions

from .models import ShopUnit
from .serializers import ShopUnitSerializer, ShopUnitImportRequestSerializer


class ShopUnitAPIView(APIView):
    """
    Get, delete, put ShopUnit
    """

    def get(self, request, uuid):
        unit = ShopUnit.get_unit(uuid)
        if not unit:
            raise exceptions.NotFound
        serializer = ShopUnitSerializer(unit)
        return Response(serializer.data)

    def post(self, request):

        serializer = ShopUnitImportRequestSerializer(data=request.data)  # create ShopUnit
        # print(repr(serializer))

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        unit = ShopUnit.get_unit(uuid)
        unit.delete()
        return Response(status=status.HTTP_200_OK)
