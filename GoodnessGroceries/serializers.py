from rest_framework import serializers
from.models import Users, Products


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'participant_id',
            'status'
        )


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'participant_id',
            'products'
        )

