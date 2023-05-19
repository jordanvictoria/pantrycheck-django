from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pantryapi.models import List, PantryUser




class ListView(ViewSet):
    """List view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single lists

        Returns:
            Response -- JSON serialized lists
        """

        try:
            list = List.objects.get(pk=pk)
            serializer = ListSerializer(list)
            return Response(serializer.data)

        except List.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all lists

        Returns:
            Response -- JSON serialized list of lists
        """

        lists = List.objects.filter(user=request.auth.user.id)





        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized list instance
        """
        
        current_user = PantryUser.objects.get(user=request.auth.user)
        serializer = CreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a list

        Returns:
            Response -- Empty body with 204 status code
        """

        list = List.objects.get(pk=pk)
        list.name = request.data["name"]
        list.notes = request.data["notes"]
        list.date_created = request.data["date_created"]
        list.completed = request.data["completed"]
        list.date_completed = request.data["date_completed"]

        user = PantryUser.objects.get(pk=request.data["user"])
        list.user = user
        
        list.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a list"""
        
        list = List.objects.get(pk=pk)
        list.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name', 'notes', 'date_created', 'completed', 'date_completed']

class UserListSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = PantryUser
        fields = ('id', 'full_name')



class ListSerializer(serializers.ModelSerializer):
    """JSON serializer for lists
    """

    user = UserListSerializer(many=False)

    class Meta:
        model = List
        fields = ('id', 'user', 'name', 'notes', 'date_created', 'completed', 'date_completed')