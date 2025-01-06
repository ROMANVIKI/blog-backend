from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import CustomUser, BlogPost, BlgoDraft
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, BlogPostSerializer, UserCreateSerailizer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

# Create your views here.


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerailizer
    permission_classes = [AllowAny]


class BlogCreateView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class BlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class RetrieveUserView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class RetrieveBlogView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


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
