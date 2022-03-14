from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whohaswhatapi.models import Lender

class LenderView(ViewSet):
    def list(self, request):
        """Handles GET for all users"""
        lenders = Lender.objects.all()
        serializer = LenderSerializer(lenders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handles GET for single user"""
        try:
            lender= Lender.objects.get(pk=pk)
            serializer = LenderSerializer(lender)
            return Response(serializer.data)
        except Lender.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        


class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = "__all__"
        depth = 1
        
class CreateLenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = ('user', 'address', 'is_owner', 'is_renter', 'profile_img_url')