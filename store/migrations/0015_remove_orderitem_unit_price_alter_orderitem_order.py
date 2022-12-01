# Generated by Django 4.1.4 on 2022-12-18 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0014_alter_customer_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="unit_price",
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="items",
                to="store.order",
            ),
        ),
    ]
