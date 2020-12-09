import requests
from config import Bot_conf, Api_conf
from faker import Faker
from random import randint
from django.contrib.auth.hashers import make_password
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_network.settings")



class Bot():
    def __init__(self):
        self.faker = Faker('en_US')
        self.number_of_users = Bot_conf.number_of_users
        self.max_posts_per_user = Bot_conf.max_posts_per_user
        self.max_likes_per_user = Bot_conf.max_likes_per_user
        self.urls = Api_conf.urls
        self.token = None

    def create_user(self):
        user = self.faker.simple_profile()
        url = self.urls['root_url'] + self.urls['create_user']
        username = user['username']
        email = user['mail']
        password = self.faker.password()
        hash_password = make_password(password)
        r = requests.post(url, data={
            'username': username,
            'email': email,
            'password': hash_password})
        if r.status_code == 201:
            first_name = r.json().get('first_name', "")
            last_name = r.json().get('last_name', "")
            return username, email, password, first_name, last_name

        if r.status_code == 400:
            return r.json()["username"]
        else:
            return False

    def create_post(self, username, password):
        token = self.get_token(username, password)
        headers = {'Authorization': 'Bearer ' + token}
        url = self.urls['root_url'] + self.urls['create_post']
        min_text = randint(10, 50)
        max_text = randint(100, 250)
        try:
            r = requests.post(url, data={
                'username': username, 'password': password,
                'text': self.faker.text()[min_text:max_text]},
                headers=headers)
            return r.json()
        except Exception as e:
            return e

    def get_posts(self, username, password):
        token = self.get_token(username, password)
        headers = {'Authorization': 'Bearer ' + token}
        url = self.urls['root_url'] + self.urls['create_post']
        try:
            r = requests.get(
                url,
                data={'username': username, 'password': password},
                headers=headers)
            return r.json()
        except Exception as e:
            return e

    def get_token(self, username, password):
        url = self.urls['root_url'] + self.urls['api_token']
        r = requests.post(url, data={'username': username, 'password': password})
        return r.json()['access']

    def like(self, post_id, username, password):
        token = self.get_token(username, password)
        url = self.urls['root_url'] + self.urls['like']
        headers = {'Authorization': 'Bearer ' + token}
        try:
            r = requests.post(
                url,
                data={
                    'username': username, 'password': password, 'post': post_id},
                headers=headers)
            return r.json()
        except Exception as e:
            return e

    def unlike(self, post_id, username, password):
        token = self.get_token(username, password)
        url = self.urls['root_url'] + self.urls['unlike']
        headers = {'Authorization': 'Bearer ' + token}
        try:
            r = requests.post(
                url,
                data={
                    'username': username, 'password': password, 'post': post_id},
                headers=headers)
            return r.json()
        except Exception as e:
            return e


class User():

    def __init__(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.token = ''

    def get_user(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'name': self.first_name,
            'last_name': self.last_name
        }

    def __str__(self):
        if len(self.first_name + self.last_name) != 0:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username


def main():
    bot = Bot()
    users = []
    number_of_users = Bot_conf.number_of_users
    max_posts_per_user = Bot_conf.max_posts_per_user
    max_likes_per_user = Bot_conf.max_likes_per_user

    for user_i in range(number_of_users):
        user_data = bot.create_user()
        if user_data:
            username, email, password, first_name, last_name = user_data
            user = User(username, email, password, first_name, last_name)
            users.append(user)
            for post_i in range(randint(0, max_posts_per_user)):
                bot.create_post(username, password)
        else:
            print(user_data)

    posts = bot.get_posts(username, password)

    for i in range(len(users)):
        for post in range(max_likes_per_user):
            post_index = randint(0, len(posts)-1)
            bot.like(posts[post_index].get('id'), user.username, user.password)


if __name__ == '__main__':
    main()
