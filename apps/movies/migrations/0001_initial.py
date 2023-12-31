# Generated by Django 4.2.3 on 2023-07-25 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50)),
                ("slug", models.SlugField()),
                ("image", models.ImageField(upload_to="")),
                ("color", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50)),
                ("publish_year", models.IntegerField()),
                (
                    "type",
                    models.CharField(
                        choices=[("Serial", "Serial"), ("Movie", "Movie"), ("Game", "Game")], max_length=10
                    ),
                ),
                ("description", models.TextField()),
                ("thumbnail", models.ImageField(upload_to="")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="MovieImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="")),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="images", to="movies.movie"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MovieComment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField(max_length=500)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="movies.movie"
                    ),
                ),
            ],
        ),
    ]
