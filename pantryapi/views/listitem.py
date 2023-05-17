from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pantryapi.models import ListItem, List, Item, PantryUser




class ListItemView(ViewSet):
    """ListItem view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single list items

        Returns:
            Response -- JSON serialized list items
        """

        try:
            list_item = ListItem.objects.get(pk=pk)
            serializer = ListItemSerializer(list_item)
            return Response(serializer.data)

        except ListItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all list items

        Returns:
            Response -- JSON serialized list of list items
        """

        list_items = ListItem.objects.filter(user=request.auth.user.id)


        # list_id = request.query_params.get('listId', None)
        # # filteredListItems = []
        # if list_id is not None:
        #     list = List.objects.get(pk=list_id)
        #     list_items = list_items.filter(list=list)






        serializer = ListItemSerializer(list_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized list item instance
        """
        
        user = PantryUser.objects.get(user=request.auth.user.id)

        serializer = CreateListItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a list item

        Returns:
            Response -- Empty body with 204 status code
        """

        list_item = ListItem.objects.get(pk=pk)
        list_item.quantity = request.data["quantity"]
        list_item.priority = request.data["priority"]

        item = Item.objects.get(pk=request.data["item"])
        list_item.item = item

        list = List.objects.get(pk=request.data["list"])
        list_item.list = list
        
        list_item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a list"""
        
        list_item = ListItem.objects.get(pk=pk)
        list_item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class CreateListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ['id', 'list', 'item', 'quantity', 'priority']


class ItemSerializer(serializers.ModelSerializer):
    """For items."""
    class Meta:
        model = Item
        fields = ('id', 'user', 'name', 'category', 'price')

class ListSerializer(serializers.ModelSerializer):
    """For lists."""
    class Meta:
        model = List
        fields = ('id', 'user', 'name', 'notes', 'date_created', 'completed', 'date_completed')

class UserListItemSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = PantryUser
        fields = ('id', 'full_name')




class ListItemSerializer(serializers.ModelSerializer):
    """JSON serializer for list items
    """
    item = ItemSerializer(many=False)
    user = UserListItemSerializer(many=False)
    list = ListSerializer(many=False)

    class Meta:
        model = ListItem
        fields = ('id', 'user', 'list', 'item', 'quantity', 'priority')
        depth = 1