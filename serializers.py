from rest_framework import serializers
from rest_framework import exceptions

# from django.core import exceptions

from .models import ShopUnit


class ShopUnitSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        if obj.type == 'OFFER':
            return None
        return self.__class__(obj.shopunit_set.all(), many=True).data

    parentId = serializers.PrimaryKeyRelatedField(source='parent', queryset=ShopUnit.objects.all(), allow_null=True)

    class Meta:
        model = ShopUnit
        exclude = ['parent', 'tree_products_count', 'tree_total_price']


class ShopUnitRequest(object):
    def __init__(self, items, updateDate):
        self.items = updateDate
        self.items = items


class ShopUnitImportRequestSerializer(serializers.Serializer):
    # items = ShopUnitImportSerializer(many=True)
    # items = serializers.ModelField(model_field=ShopUnit(), many)
    items = serializers.ListField(allow_empty=True)
    updateDate = serializers.DateTimeField()

    def create(self, validated_data):
        instance = ShopUnitRequest(**validated_data)  # returning instance
        for item in validated_data.get('items'):

            unit = ShopUnit.get_unit(pk=item.get('id'))
            item['date'] = validated_data['updateDate']

            if unit:
                item_serializer = ShopUnitSerializer(unit, data=item)
            else:
                item_serializer = ShopUnitSerializer(data=item)
            if not item_serializer.is_valid():
                raise exceptions.ValidationError(item_serializer.errors)
            instance = item_serializer.save()
            instance.update()
        return instance
