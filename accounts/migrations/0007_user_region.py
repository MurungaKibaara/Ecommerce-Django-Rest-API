# Generated by Django 3.0.3 on 2020-03-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200301_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.CharField(default='Nairobi', max_length=20),
            preserve_default=False,
        ),
    ]
