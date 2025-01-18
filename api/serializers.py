from .models import BlogPost, CustomUser, Like, Comment, SavedBlog
from rest_framework import fields, serializers


class CommentSerializer(serializers.ModelSerializer):
    commented_by_name = serializers.CharField(
        source="commented_by.username", read_only=True
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "blog_id",
            "comment",
            "commented_by",
            "commented_by_name",
            "created_at",
            "replies",
        ]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class LikeSerializer(serializers.ModelSerializer):
    liked_by_name = serializers.CharField(source="liked_by.username", read_only=True)

    class Meta:
        model = Like
        fields = ["id", "liked_by", "liked_by_name", "created_at"]


class SavedBlogSerializer(serializers.ModelSerializer):
    saved_by_name = serializers.CharField(source="saved_by.username", read_only=True)

    class Meta:
        model = SavedBlog
        fields = ["id", "saved_by", "saved_by_name", "saved_blog", "created_at"]


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "created_at",
            "updated_at",
            "author",
            "author_name",
            "likes",
            "comments",
            "like_count",
            "comment_count",
        ]

    def get_likes(self, obj):
        return LikeSerializer(obj.like_set.all(), many=True).data

    def get_comments(self, obj):
        # Only get top-level comments (no parent)
        top_comments = obj.comment_set.filter(parent_comment=None)
        return CommentSerializer(top_comments, many=True).data

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comment_set.count()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "bio",
            "created",
        ]


class UserCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
