# Generated by Django 4.2.3 on 2023-07-30 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat_api", "0002_rename_server_id_channel_server_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="server",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
