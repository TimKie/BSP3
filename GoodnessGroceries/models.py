from django.db import models
from postgres_copy import CopyManager


class CashierTicketProducts(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.CharField(max_length=100)
    product = models.BigIntegerField()
    reviewed = models.BooleanField(default=False)

    objects = CopyManager()

    class Meta:
        verbose_name = 'CashierTicketProducts'
        verbose_name_plural = 'CashierTicketProducts'


class MonitoringData(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.DateTimeField()
    activity_name = models.CharField(max_length=100)
    metadata = models.CharField(max_length=100)

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
    product_category_3 = models.CharField(max_length=100, null=True)
    product_category_4 = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'


# ------------------------------ Static Data ------------------------------------------------------

class StaticProducts(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    image_url = models.TextField()
    indicators_0_indicator_id = models.CharField(max_length=100)
    indicators_0_indicator_description = models.TextField()
    indicators_1_indicator_id = models.CharField(max_length=100)
    indicators_1_indicator_description = models.TextField()
    indicators_2_indicator_id = models.CharField(max_length=100)
    indicators_2_indicator_description = models.TextField()

    class Meta:
        verbose_name = 'StaticProducts'
        verbose_name_plural = 'StaticProducts'


class StaticIndicators(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    category_id = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    general_description = models.TextField()

    class Meta:
        verbose_name = 'StaticIndicators'
        verbose_name_plural = 'StaticIndicators'


class StaticIndicatorCategories(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'StaticIndicatorCategories'
        verbose_name_plural = 'StaticIndicatorCategories'
