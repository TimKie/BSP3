from django.db import models


class Users(models.Model):
    participant_id = models.CharField(max_length=13, primary_key=True)
    STATUS = (
        ('requested', 'requested'),
        ('valid', 'valid')
    )
    status = models.CharField(
        max_length=100, default='requested', choices=STATUS)
    PLATFORM = (
        ('ios', 'ios'),
        ('android', 'android')
    )
    platform = models.CharField(
        max_length=100, null=True, choices=PLATFORM)
    product_category_1 = models.CharField(
        max_length=100, blank=True, null=True)
    product_category_2 = models.CharField(
        max_length=100, blank=True, null=True)
    product_category_3 = models.CharField(
        max_length=100, blank=True, null=True)
    product_category_4 = models.CharField(
        max_length=100, blank=True, null=True)
    indicator_category_1 = models.CharField(
        max_length=100, blank=True, null=True)
    indicator_category_2 = models.CharField(
        max_length=100, blank=True, null=True)
    indicator_category_3 = models.CharField(
        max_length=100, blank=True, null=True)
    indicator_category_4 = models.CharField(
        max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    def __str__(self):
        return "Participant ID: " + str(self.participant_id)

    def getDevices(self):
        return Devices.objects.filter(participant=self)


class CashierTicketProducts(models.Model):
    participant = models.ForeignKey(Users, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True, blank=True)
    product = models.BigIntegerField()
    reviewed = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = 'Cashier Ticket Product'
        verbose_name_plural = 'Cashier Ticket Products'

    def __str__(self):
        return str(self.participant)


class ProductReviews(models.Model):
    participant = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_ean = models.BigIntegerField()
    timestamp = models.DateTimeField(null=True, blank=True)
    selected_indicator_main_id = models.CharField(
        max_length=100, null=True, blank=True)
    selected_indicator_secondary_id = models.CharField(
        max_length=100, null=True, blank=True)
    free_text_indicator = models.TextField(null=True, blank=True)
    price_checkbox_selected = models.BooleanField()

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return str(self.participant)


class Devices(models.Model):
    participant = models.ForeignKey(
        Users, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=100, primary_key=True)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return "Device token: " + str(self.device_token)

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
