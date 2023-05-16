from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pantryapi.models import Item




class ItemView(ViewSet):
    """Item view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single items

        Returns:
            Response -- JSON serialized items
        """

        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)

        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all items

        Returns:
            Response -- JSON serialized list of items
        """

        items = Item.objects.filter(user=request.auth.user.id)





        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized item instance
        """
        
        current_user = request.auth.user.id
        serializer = CreateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an item

        Returns:
            Response -- Empty body with 204 status code
        """

        item = Item.objects.get(pk=pk)
        item.name = request.data["name"]
        item.category = request.data["category"]
        item.price = request.data["price"]
        
        item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a list"""
        
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items
    """

    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'price')

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'price']