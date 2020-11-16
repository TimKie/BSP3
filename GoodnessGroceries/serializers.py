from rest_framework import serializers
from.models import CashierTicketProducts, MonitoringData, ProductReviews, Users


class CashierTicketProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashierTicketProducts
        fields = (
            'product',
            'timestamp'
        )


class MonitoringDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringData
        fields = (
            'participant_id',
            'timestamp',
            'activity_name',
            'metadata'
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
            'product_category_1',
            'product_category_2',
            'product_category_3',
            'product_category_4'
        )
