# Generated by Django 3.1.1 on 2020-10-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoodnessGroceries', '0002_auto_20201026_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreviews',
            name='price_checkbox_selected',
            field=models.BooleanField(),
        ),
    ]
