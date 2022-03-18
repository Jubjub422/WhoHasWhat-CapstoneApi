from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from whohaswhatapi.models import RequestQueue, Lender, Item
from rest_framework.decorators import action


class RentalQueueView(ViewSet):
    def list(self, request):
        """handles the GET for single requestQueues"""

        try:
            # owner_id = request.query_params.get('owner', None)
            # owner = Lender.objects.get(pk=owner_id)
            request_queue = RequestQueue.objects.all()
            serializer = RequestQueueSerializer(request_queue, many=True)
            return Response(serializer.data)
        except Lender.DoesNotExist:
            return Response("No current requests")

    def retrieve(self, request, pk):
        """handles the GET for a single request Item"""
        try:
            request = RequestQueue.objects.get(pk=pk)
            serializer = RequestQueueSerializer(request)
            return Response(serializer.data)
        except RequestQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Creates the request"""
        renter = Lender.objects.get(user=request.auth.user)
        try:
            serializer = CreateRequestQueueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(renter=renter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """removes the request"""
        try:
            request_queue = RequestQueue.objects.get(pk=pk)
            request_queue.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except RequestQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
   
    @action(methods=['put'], detail=True)
    def approve(self, request, pk):
        """lender can rent item from owner"""
        item=Item.objects.get(pk=request.data["id"])
        request=RequestQueue.objects.get(pk=pk)
        request.approved=True
        item.rented_currently=True
        request.save()
        item.save()
        return Response({'message': 'Item rental has been approved'})
    
    @action(methods=['put'], detail=True)
    def return_item(self, request, pk):
        """renter can return item to owner"""
        item = Item.objects.get(pk=request.data["id"])
        request = RequestQueue.objects.get(pk=pk)
        request.returned=True
        item.rented_currently=False
        item.save()
        request.save()
        return Response({'message': 'Item has been returned'})
    
class RequestQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQueue
        fields ="__all__"
        depth = 2


class CreateRequestQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQueue
        fields = ('owner', 'item', 'approved', 'returned')
