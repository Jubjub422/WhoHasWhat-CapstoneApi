from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from whohaswhatapi.models import Condition


class ConditionView(ViewSet):

    def list(self, request):
        """handles GET for all conditions"""
        conditions = Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles GET for single condition"""
        try:
            condition = Condition.objects.get(pk=pk)
            serializer = ConditionSerializer(condition)
            return Response(serializer.data)
        except Condition.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """handles POST for a condition"""
        try:
            serializer = CreateConditionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """handles PUT for a condition"""
        try:
            condition = Condition.objects.get(pk=pk)
            serializer = CreateConditionSerializer(
                condition, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """handles DELETE for a condition"""
        condition = Condition.objects.get(pk=pk)
        condition.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = "__all__"
        depth = 1


class CreateConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('condition', 'description')
