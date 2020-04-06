# Generated by Django 3.0.3 on 2020-03-18 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200312_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(upload_to='product_images')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('main', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='api.Product')),
            ],
        ),
    ]