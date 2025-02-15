from .models import CustomUser, BlogPost  # Assuming you have a Blog model
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.utils.http import urlencode


def send_email_to_all_users(blog_title, blog_author, blog_id):
    # Fetch all users' emails and usernames
    emails = list(CustomUser.objects.values_list("email", flat=True))
    usernames = list(CustomUser.objects.values_list("username", flat=True))

    # Construct the blog URL
    full_blog_url = f"http://yourdomain.com"  # Replace with your actual domain

    # Email subject and message
    subject = f"A New Blog Dropped from Vblog: {blog_title}"
    message = f"""
    Hi there!

    A new blog titled "{blog_title}" by {blog_author} has just been published on Vblog.

    Click the link below to read the blog:
    {full_blog_url}

    Happy reading!
    The Vblog Team
    """
    from_email = "vblog@example.com"

    # Prepare messages for all users
    messages = [(subject, message, from_email, [email]) for email in emails]

    # Send all emails in one go
    send_mass_mail(messages)
