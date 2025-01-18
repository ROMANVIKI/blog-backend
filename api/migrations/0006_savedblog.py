# Generated by Django 5.1.4 on 2025-01-13 04:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_comment_parent_comment"),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedBlog",
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
                    "saved_blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.blogpost"
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
