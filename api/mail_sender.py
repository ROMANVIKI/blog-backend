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
    site_url = f"https://vblog-tan.vercel.app/"  # Replace with your actual domain

    message = f"""Thank you for subscribing to our newsletter. We will keep you updated with our latest posts.

    Visit Our Site by clicking the following link!

    {site_url}
     """
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [email])


def send_email_to_all_users(blog_title, blog_author, blog_id):
    emails = list(CustomUser.objects.values_list("email", flat=True))
    usernames = list(CustomUser.objects.values_list("username", flat=True))
    subscribed_emails = list(SubscriptionMail.objects.values_list("email", flat=True))
    slugged_title = slugify(blog_title)

    all_emails = set(emails + subscribed_emails)

    full_blog_url = f"https://vblog-tan.vercel.app/blogs/${slugged_title}"  # Replace with your actual domain

    subject = f"A New Blog Dropped from Vblog: {blog_title}"
    message = f"""
    Hi there!

    A new blog titled "{blog_title}" by {blog_author} has just been published on Vblog.

    Click the link below to read the blog:

    {full_blog_url}

    Happy reading!
    The Vblog Team
    """
    from_email = "vikramanm.py@gmail.com"

    messages = [(subject, message, from_email, [email]) for email in all_emails]

    send_mass_mail(messages)
