# Generated by Django 4.2.3 on 2023-08-15 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_moviecomment_is_spoiler"),
        ("users", "0003_alter_user_groups_movierecommend"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movierecommend",
            name="user_from",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="movie_recommend", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="movierecommend",
            name="user_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="movie_got_recommend",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="MovieRecommendAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "answer_status",
                    models.CharField(
                        choices=[("Liked", "Liked"), ("Watched", "Watched"), ("NotLiked", "NotLiked")], max_length=10
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="answer_recommended", to="movies.movie"
                    ),
                ),
                (
                    "user_from",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_recommended",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_got_recommended",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
