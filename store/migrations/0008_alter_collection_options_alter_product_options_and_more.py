# Generated by Django 4.1.4 on 2022-12-10 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_rename_collection_id_product_collection"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["title"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(null=True),
        ),
    ]
