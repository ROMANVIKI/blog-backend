from django.urls import path
from . import views


urlpatterns = [
    path("create-user/", views.UserCreateView.as_view(), name="create-user"),
    path("create-blog/", views.BlogCreateView.as_view(), name="create-blog"),
    path("users/", views.UserListView.as_view(), name="users"),
    path("blogs/", views.BlogListView.as_view(), name="blogs"),
    path("user/<int:pk>/", views.RetrieveUserView.as_view(), name="user"),
    path("blog/<int:pk>/", views.RetrieveBlogView.as_view(), name="blog"),
    path("check-email/", views.RetrieveEmailView.as_view(), name="check-email"),
    path(
        "check-username/", views.RetrieveUserNameView.as_view(), name="check-username"
    ),
]
