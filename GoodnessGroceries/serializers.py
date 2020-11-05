from rest_framework import serializers
from.models import Products, MonitoringData, ProductReviews, Users


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'participant_id',
            'timestamp',
            'products'
        )


class MonitoringDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringData
        fields = (
            'participant_id',
            'timestamp',
            'activity_name',
            'metadata_os',
            'metadata_ean'
        )


class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = (
            'participant_id',
            'product_ean',
            'selected_indicator_main_id',
            'selected_indicator_secondary_id',
            'free_text_indicator',
            'price_checkbox_selected'

        )


class UsersStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'status',
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'participant_id',
            'status',
            'product_category_1',
            'product_category_2'
        )
