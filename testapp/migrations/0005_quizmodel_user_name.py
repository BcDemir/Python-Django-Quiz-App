# Generated by Django 4.2.3 on 2023-08-14 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_quizmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='user_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
