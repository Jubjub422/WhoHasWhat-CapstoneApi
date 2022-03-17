from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from whohaswhatapi.models import RequestQueue, Lender


class RentalQueueView(ViewSet):
    def list(self, request):
        """handles the GET for single requestQueues"""

        try:
            owner_id = request.query_params.get('item_owner', None)
            owner = Lender.objects.get(pk=owner_id)
            request_queue = RequestQueue.objects.filter(owner=owner)
            serializer = RequestQueueSerializer(request_queue, many=True)
            return Response(serializer.data)
        except Lender.DoesNotExist:
            return Response("No current requests")


    def create(self, request):
        """Creates the request"""
        requester = Lender.objects.get(user=request.auth.user)
        try:
            serializer = CreateRequestQueueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(requester=requester)
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

class RequestQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQueue
        fields ="__all__"


class CreateRequestQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQueue
        fields = ('owner', 'renter', 'item')
