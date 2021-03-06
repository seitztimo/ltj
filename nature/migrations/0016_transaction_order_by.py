# Generated by Django 2.1.7 on 2019-04-15 06:44

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ("nature", "0015_historicalfeature_feature_field_change"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="transaction",
            options={
                "ordering": [
                    django.db.models.expressions.OrderBy(
                        django.db.models.expressions.F("date"),
                        descending=True,
                        nulls_last=True,
                    )
                ],
                "verbose_name": "transaction",
                "verbose_name_plural": "transactions",
            },
        ),
    ]
