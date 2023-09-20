from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pantryapi.models import Item, Category, PantryUser




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

        search = request.query_params.get('search', None)
        filteredItems = []
        if search is not None:
            items = items.filter(name__icontains = search)





        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized item instance
        """
        
        current_user = PantryUser.objects.get(user=request.auth.user)
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
        item.price = request.data["price"]
        
        item_category = Category.objects.get(pk=request.data["category"])
        item.category = item_category

        user = PantryUser.objects.get(pk=request.data["user"])
        item.user = user

        item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a list"""
        
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'price']



class CategoryItemSerializer(serializers.ModelSerializer):
    """For categories."""
    class Meta:
        model = Category
        fields = ('id', 'name')

class UserItemSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = PantryUser
        fields = ('id', 'full_name')


class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items
    """
    user = UserItemSerializer(many=False)
    category = CategoryItemSerializer(many=False)

    class Meta:
        model = Item
        fields = ('id', 'user', 'name', 'category', 'price')
        depth = 1