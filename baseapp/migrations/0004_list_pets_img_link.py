# Generated by Django 5.0.4 on 2024-05-05 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_list_pets'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_pets',
            name='img_link',
            field=models.CharField(default='noLink', max_length=500),
            preserve_default=False,
        ),
    ]