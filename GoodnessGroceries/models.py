from django.db import models
from postgres_copy import CopyManager


class Products(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.CharField(max_length=100)
    products = models.BigIntegerField()

    objects = CopyManager()

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'


class MonitoringData(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.DateTimeField()
    activity_name = models.CharField(max_length=100)
    metadata_os = models.CharField(max_length=100)
    metadata_ean = models.BigIntegerField()

    class Meta:
        verbose_name = 'Monitoring Data'
        verbose_name_plural = 'Monitoring Data'


class ProductReviews(models.Model):
    participant_id = models.BigIntegerField()
    product_ean = models.BigIntegerField()
    selected_indicator_main_id = models.CharField(max_length=100)
    selected_indicator_secondary_id = models.CharField(max_length=100)
    free_text_indicator = models.TextField()
    price_checkbox_selected = models.BooleanField()

    class Meta:
        verbose_name = 'Product Reviews'
        verbose_name_plural = 'Product Reviews'


class Users(models.Model):
    participant_id = models.BigIntegerField()
    status = models.CharField(max_length=100, default='requested')
    product_category_1 = models.CharField(max_length=100, null=True)
    product_category_2 = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
