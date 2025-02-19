import email
from .models import CustomUser, BlogPost, SubscriptionMail
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings


def send_subscription_email(email):
    subject = "Welcome to Our Newsletter!"
    message = f"Thank you for subscribing to our newsletter. We will keep you updated with our latest posts."
    from_email = settings.DEFAULT_FROM_EMAIL  # You can set this in your settings

    send_mail(subject, message, from_email, [email])


def send_email_to_all_users(blog_title, blog_author, blog_id):
    # Fetch all users' emails and usernames
    emails = list(CustomUser.objects.values_list("email", flat=True))
    usernames = list(CustomUser.objects.values_list("username", flat=True))
    subscribed_emails = list(SubscriptionMail.objects.values_list("email", flat=True))
    slugged_title = slugify(blog_title)

    all_emails = set(emails + subscribed_emails)

    # Construct the blog URL
    full_blog_url = f"https://vblog-tan.vercel.app/blogs/${slugged_title}"  # Replace with your actual domain

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
    # from_email = "vblog@example.com"

    # Prepare messages for all users
    messages = [(subject, message, [email]) for email in all_emails]

    # Send all emails in one go
    send_mass_mail(messages)
