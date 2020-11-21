from django.db import models
from postgres_copy import CopyManager


class CashierTicketProducts(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.CharField(max_length=100)
    product = models.BigIntegerField()
    reviewed = models.BooleanField(default=False, null=True)

    objects = CopyManager()

    class Meta:
        verbose_name = 'CashierTicketProducts'
        verbose_name_plural = 'CashierTicketProducts'

    def __str__(self):
        return "Participant ID: "+str(self.participant_id)


class MonitoringData(models.Model):
    participant_id = models.BigIntegerField()
    timestamp = models.DateTimeField()
    activity_name = models.CharField(max_length=100)
    metadata = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Monitoring Data'
        verbose_name_plural = 'Monitoring Data'

    def __str__(self):
        return "Participant ID: "+str(self.participant_id)


class ProductReviews(models.Model):
    participant_id = models.BigIntegerField()
    product_ean = models.BigIntegerField()
    timestamp = models.DateTimeField(null=True, blank=True)
    selected_indicator_main_id = models.CharField(max_length=100)
    selected_indicator_secondary_id = models.CharField(max_length=100)
    free_text_indicator = models.TextField()
    price_checkbox_selected = models.BooleanField()

    class Meta:
        verbose_name = 'Product Reviews'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return "Participant ID: "+str(self.participant_id)


class Users(models.Model):
    participant_id = models.BigIntegerField()
    STATUS = (
        ('requested', 'requested'),
        ('valid', 'valid')
    )
    status = models.CharField(max_length=100, default='requested', choices=STATUS)
    product_category_1 = models.CharField(max_length=100, null=True)
    product_category_2 = models.CharField(max_length=100, null=True)
    product_category_3 = models.CharField(max_length=100, null=True)
    product_category_4 = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return "Participant ID: "+str(self.participant_id)


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

    def __str__(self):
        return self.name


class StaticIndicators(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    category_id = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    general_description = models.TextField()

    class Meta:
        verbose_name = 'StaticIndicators'
        verbose_name_plural = 'StaticIndicators'

    def __str__(self):
        return self.name


class StaticIndicatorCategories(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'StaticIndicatorCategories'
        verbose_name_plural = 'StaticIndicatorCategories'

    def __str__(self):
        return self.name
