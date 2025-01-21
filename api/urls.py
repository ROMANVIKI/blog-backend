from django.urls import path
from . import views


urlpatterns = [
    path("create-user/", views.UserCreateView.as_view(), name="create-user"),
    path("create-blog/", views.BlogCreateView.as_view(), name="create-blog"),
    path("users/", views.UserListView.as_view(), name="users"),
    path("blogs/", views.BlogListView.as_view(), name="blogs"),
    path("user/", views.RetrieveUserView.as_view(), name="user"),
    path("blog/<str:slug>/", views.RetrieveBlogView.as_view(), name="blog"),
    path("check-email/", views.RetrieveEmailView.as_view(), name="check-email"),
    path(
        "check-username/", views.RetrieveUserNameView.as_view(), name="check-username"
    ),
    path("create-comment/", views.CommentCreateView.as_view(), name="create-comment"),
    path("save-blog/", views.SavedBlogCreateView.as_view(), name="save-blog"),
    path(
        "list-saved-blogs/", views.SavedBlogListView.as_view(), name="list-saved-blogs"
    ),
    path("edit-user/<int:id>/", views.UpdateUserAPIView.as_view(), name="edit-user"),
]
