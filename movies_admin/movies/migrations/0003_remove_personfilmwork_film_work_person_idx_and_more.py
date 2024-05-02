# Generated by Django 4.2.9 on 2024-02-03 13:05

from django.db import migrations
import psqlextra.indexes.unique_index


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_alter_genrefilmwork_options_and_more"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="personfilmwork",
            name="film_work_person_idx",
        ),
        migrations.AddIndex(
            model_name="personfilmwork",
            index=psqlextra.indexes.unique_index.UniqueIndex(
                fields=["film_work", "person", "role"], name="film_work_person_role_idx"
            ),
        ),
    ]
