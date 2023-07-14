# Generated by Django 4.2.2 on 2023-06-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipparams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ship_params',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='ship_params',
            name='extracost',
        ),
        migrations.RemoveField(
            model_name='ship_params',
            name='price',
        ),
        migrations.RemoveField(
            model_name='ship_params',
            name='volume_item',
        ),
        migrations.RemoveField(
            model_name='ship_params',
            name='volume_journey',
        ),
        migrations.RemoveField(
            model_name='ship_params',
            name='volume_origin_center',
        ),
        migrations.AddField(
            model_name='ship_params',
            name='zone',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='ship_params',
            name='carrier',
            field=models.IntegerField(default=1),
        ),
    ]