from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whohaswhatapi.models import RentedItem
from whohaswhatapi.models.Lender import Lender


class RentedItemView(ViewSet):
    
    
    def list(self, request):
        """
        Handle GET requests to get all items
        """
        rented = RentedItem.objects.all()
        serializer = RentedItemSerializer(rented, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """handles the GET for a single rentedItem"""
        try:
            rented = RentedItem.objects.get(pk=pk)
            serializer = RentedItemSerializer(rented)
            return Response(serializer.data)
        except RentedItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Owner creates a new rentedItem"""
        renter = Lender.objects.get(user=request.auth.user)
        try:
            serializer = CreateRentedItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(renter=renter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        """update an individual rentedItem"""
        try:
            rented = RentedItem.objects.get(pk=pk)
            serializer = CreateRentedItemSerializer(rented, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """delete an rentedItem"""
        rented = RentedItem.objects.get(pk=pk)
        rented.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class RentedItemSerializer(serializers.ModelSerializer):
    """
    JSON serializer for all rentedItems
    """
    class Meta:
        model = RentedItem
        fields = "__all__"
        depth = 2
        
class CreateRentedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentedItem
        fields = ('renter', 'rented_on', 'rental_item', 'return_by')