from django.db import models
from postgres_copy import CopyManager


# Q: I have to define the table. Should I add as many columns as there are products in the study
# such that the table will always have enough space to store all the products?

# I cannot make mor fields in the model than there are element in the csv file since otherwise I will get a error
# that the model violates not-null constraint -> I have to always fill the csv files with 0's such that the sizes
# will be compatible

class Products(models.Model):
    participant_id = models.BigIntegerField()
    products_0_product_ean = models.BigIntegerField()
    products_1_product_ean = models.BigIntegerField()
    products_2_product_ean = models.BigIntegerField()
    products_3_product_ean = models.BigIntegerField()
    products_4_product_ean = models.BigIntegerField()
    products_5_product_ean = models.BigIntegerField()
    products_6_product_ean = models.BigIntegerField()
    products_7_product_ean = models.BigIntegerField()
    products_8_product_ean = models.BigIntegerField()
    products_9_product_ean = models.BigIntegerField()
    products_10_product_ean = models.BigIntegerField()

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
    price_checkbox_selected = models.IntegerField()

    class Meta:
        verbose_name = 'Product Reviews'
        verbose_name_plural = 'Product Reviews'


class Users(models.Model):
    participant_id = models.BigIntegerField()
    status = models.CharField(max_length=100)
    product_type_preference = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
