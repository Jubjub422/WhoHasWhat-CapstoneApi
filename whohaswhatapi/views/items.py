from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whohaswhatapi.models import Item
from whohaswhatapi.models.Lender import Lender
from rest_framework.decorators import action


class ItemView(ViewSet):
    
    
    def list(self, request):
        """
        Handle GET requests to get all items
        """
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """handles the GET for a single item"""
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Owner creates a new item"""
        owner = Lender.objects.get(user=request.auth.user)
        try:
            serializer = CreateItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(owner=owner)
            post.categories.set(request.data["categories"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        """update an individual item"""
        try:
            items = Item.objects.get(pk=pk)
            serializer = CreateItemSerializer(items, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """delete an item"""
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def approve_rent(self, request, pk):
        """lender can rent item from owner"""
        item=Item.objects.get(pk=pk)
        item.rented_currently=True
        item.save()
        return Response({'message': 'Item rental has been approved'})
    
    @action(methods=['put'], detail=True)
    def return_item(self, request, pk):
        """renter can return item to owner"""
        item = Item.objects.get(pk=pk)
        item.rented_currently=False
        item.save()
    
    
    
class ItemSerializer(serializers.ModelSerializer):
    """
    JSON serializer for all items
    """
    class Meta:
        model = Item
        fields = "__all__"
        depth = 2
        
class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'price_per_day', 'price_per_week', 'condition')