# Generated by Django 2.2.24 on 2021-11-24 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture_url',
            field=models.ImageField(default='source/static/img/default-profile-icon-16.png', upload_to='source/static/images/'),
        ),
    ]
