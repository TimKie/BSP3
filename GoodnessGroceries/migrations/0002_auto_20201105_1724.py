# Generated by Django 3.1.1 on 2020-11-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoodnessGroceries', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='product_type_preference',
        ),
        migrations.AddField(
            model_name='users',
            name='product_category_1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='product_category_2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(default='requested', max_length=100),
        ),
    ]