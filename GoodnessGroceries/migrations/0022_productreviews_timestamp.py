# Generated by Django 3.1.3 on 2020-11-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoodnessGroceries', '0021_users_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreviews',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
