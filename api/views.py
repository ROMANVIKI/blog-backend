from os import stat
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework.views import APIView, Response
from .models import (
    CustomUser,
    BlogPost,
    BlgoDraft,
    Comment,
    Like,
    SavedBlog,
    SubscriptionMail,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import (
    CustomUserSerializer,
    BlogPostSerializer,
    SavedBlogSerializer,
    UserCreateSerailizer,
    LikeSerializer,
    CommentSerializer,
    SubscribedEmailSerializer,
)
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework import status
from api import serializers

from .mail_sender import send_email_to_all_users, send_subscription_email
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerailizer
    permission_classes = [AllowAny]


class BlogCreateView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class BlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class RetrieveUserView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveBlogView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class RetrieveBlogViewForNewUser(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class RetrieveEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=HTTP_400_BAD_REQUEST)
        exists = CustomUser.objects.filter(email=email).exists()
        return Response({"exists": exists}, status=HTTP_200_OK)


class RetrieveUserNameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response(
                {"error": "Username is required"}, status=HTTP_400_BAD_REQUEST
            )
        exists = CustomUser.objects.filter(username=username).exists()
        return Response({"exists": exists}, status=HTTP_200_OK)


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # print("Request Data: ", self.request.data)
        # print("Authenticated User:", self.request.user)
        blog_id = self.request.data.get("blog")
        comment_text = self.request.data.get("comment")

        if not blog_id or not comment_text:
            raise ValidationError(
                {"error": "Both blog ID and comment text are required"}
            )

        try:
            blog = BlogPost.objects.get(id=blog_id)

        except Blog.DoesNotExist:
            raise ValidationError({"error": "Blog not found"})
        serializer.save(commented_by=self.request.user, blog=blog)


class SavedBlogCreateView(CreateAPIView):
    queryset = SavedBlog.objects.all()
    serializer_class = SavedBlogSerializer
    permission_classes = [IsAuthenticated]


class SavedBlogListView(ListAPIView):
    # queryset = SavedBlog.objects.all()
    serializer_class = SavedBlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SavedBlog.objects.filter(saved_by=user)


class UpdateUserAPIView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class CreateLikeAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]


class DeleteLikeAPIView(DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class DeleteBlogAPIView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class DeleteCommentAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class DeleteSavedBlogAPIView(DestroyAPIView):
    queryset = SavedBlog.objects.all()
    serializer_class = SavedBlogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class CurrentBlogListAPIView(ListAPIView):
    # queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


@receiver(post_save, sender=BlogPost)
def send_email_on_blog_creation(sender, instance, created, **kwargs):
    if created:
        send_email_to_all_users(instance.title, instance.author.username, instance.id)


@receiver(post_save, sender=SubscriptionMail)
def send_subscribe_email(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        send_subscription_email(email)


class CreateSubscriptionEmail(CreateAPIView):
    queryset = SubscriptionMail.objects.all()
    serializer_class = SubscribedEmailSerializer
    permission_classes = [AllowAny]
