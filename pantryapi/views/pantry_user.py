"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pantryapi.models import PantryUser


class PantryUserView(ViewSet):
    """Level up categories view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single pantry user

        Returns:
            Response -- JSON serialized pantry user
        """

        try:
            pantry_user = PantryUser.objects.get(pk=pk)
            serializer = PantryUserSerializer(pantry_user)
            return Response(serializer.data)
        except PantryUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all pantry users

        Returns:
            Response -- JSON serialized list of pantry users
        """

        pantry_users = PantryUser.objects.all()
        serializer = PantryUserSerializer(pantry_users, many=True)
        return Response(serializer.data)


class PantryUserSerializer(serializers.ModelSerializer):
    """JSON serializer for pantry users
    """
    class Meta:
        model = PantryUser
        fields = ('id', 'user', 'full_name')