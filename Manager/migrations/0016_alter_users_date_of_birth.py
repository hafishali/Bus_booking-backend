# Generated by Django 5.0.2 on 2024-03-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0015_alter_users_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='date_of_birth',
            field=models.CharField(max_length=100, null=True),
        ),
    ]