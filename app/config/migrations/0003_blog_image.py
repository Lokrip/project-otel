# Generated by Django 5.0.6 on 2024-07-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_alter_messageblog_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog-image/%Y/%m/%d/'),
        ),
    ]