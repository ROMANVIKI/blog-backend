# Generated by Django 5.1.4 on 2025-01-09 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_blogpost_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField(blank=True, max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.blogpost"
                    ),
                ),
                (
                    "commented_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="blogpost",
            name="comments",
            field=models.ManyToManyField(
                related_name="commented_posts",
                through="api.Comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.blogpost"
                    ),
                ),
                (
                    "liked_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("liked_by", "blog")},
            },
        ),
        migrations.AddField(
            model_name="blogpost",
            name="likes",
            field=models.ManyToManyField(
                related_name="liked_posts",
                through="api.Like",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
