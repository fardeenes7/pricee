from ..models import User
# import requests
from django.core.files import File

from django.contrib.auth import authenticate
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def generate_profile_pic_url(id, url):
    # url = url if url else f"https://api.dicebear.com/6.x/bottts/{id}.png"
    # response = requests.get(url)
    # image_name = f"{id}.png"
    # with open(image_name, "wb") as f:
    #     f.write(response.content)
    image_name = 'default.png'
    return image_name
    


def register_social_user(provider, uid, email, name, image_url=None):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=uid)
            print(registered_user)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password':uid}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.name = name
        image = generate_profile_pic_url(user.id, image_url)
        user.profile_pic = File(open(image, "rb"))
        user.save()

        new_user = authenticate(
            email=email, password=uid)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }



def send_registration_email(email, name, uid):
    from django.core.mail import send_mail
    from django.conf import settings

    subject = "Welcome to Django React Blog"
    message = f"Hi {name}, Welcome to Django React Blog. Please click on the link below to verify your email. http://localhost:3000/verify-email/{uid}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


def register_email_user(provider, email, name, password, image_url=None, username=""):
    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=password)
            print(registered_user)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        uname = username if username else generate_username(name)
        user = {
            'username': uname, 'email': email,
            'password':password}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.name = name
        image = generate_profile_pic_url(user.id, image_url)
        user.profile_pic = File(open(image, "rb"))
        user.save()

        new_user = authenticate(
            email=email, password=password)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'id': new_user.id,
            'tokens': new_user.tokens()
        }
