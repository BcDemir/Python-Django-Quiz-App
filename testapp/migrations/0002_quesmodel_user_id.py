# Generated by Django 4.2.3 on 2023-08-14 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quesmodel',
            name='user_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]