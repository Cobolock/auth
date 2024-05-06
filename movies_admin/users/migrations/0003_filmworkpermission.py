# Generated by Django 4.2.9 on 2024-05-06 18:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_delete_profile'),
        ('users', '0002_userpermission_userrole_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmworkPermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userrole')),
            ],
            options={
                'verbose_name': 'film_permission',
                'verbose_name_plural': 'film_permissions',
            },
        ),
    ]
