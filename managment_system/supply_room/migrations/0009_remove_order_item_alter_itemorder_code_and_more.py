# Generated by Django 5.0.4 on 2024-06-26 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supply_room", "0008_alter_order_item"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="item",
        ),
        migrations.AlterField(
            model_name="itemorder",
            name="code",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="itemorder",
            name="status",
            field=models.CharField(
                choices=[
                    ("Solicitado", "Solicitado"),
                    ("Prestado", "Prestado"),
                    ("Devuelto", "Devuelto"),
                    ("Denegado", "Denegado"),
                ],
                default="Solicitado",
                max_length=20,
            ),
        ),
    ]