import json
import uuid
from random import choice, randint
from datetime import datetime
import requests


class AutomatedBot:
    def __init__(self, host):
        self.host = host
        self.post_ids = []

    @property
    def headers(self):
        return {"Content-Type": "application/json"}

    @property
    def users(self):
        return self._users

    @property
    def login_url(self):
        return self.host + '/api/account/login/'

    @property
    def signup_url(self):
        return self.host + '/api/account/signup/'

    @property
    def post_url(self):
        return self.host + '/api/posts/'

    def generate_usernames(self, number_of_users):
        self._users = set()
        for n in range(number_of_users):
            username = uuid.uuid4().hex
            self._users.add(username)
        return self._users

    def singup(self, username, password):
        print(f'Start sing up with username {username}')
        data = {'email': None,
                "username": None,
                'password': password,
                'password2': password,
                }
        email_suffix = '@gmail.com'
        email = f"{username}{email_suffix}"
        data['email'] = email
        data['username'] = username
        requests.post(self.signup_url, data=json.dumps(data), headers=self.headers)

    def login(self, username, password):
        print(f"Login with username {username}")
        data = {'username': username, 'password': password}
        r = requests.post(self.login_url, data=json.dumps(data), headers=self.headers)
        return r.json()['token']

    def make_post(self, token, posts_count):
        print('Start add posts')
        headers = self.headers
        headers['Authorization'] = 'JWT ' + token
        posts_count = randint(0, posts_count)
        post_template = {'title': '', 'content': ''}
        for n in range(posts_count):
            print("Start sending post")
            now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            post_template['title'] = f"Title {now}"
            post_template['content'] = f"Content {now}"
            r2 = requests.post(self.post_url, data=json.dumps(post_template), headers=headers)
            assert r2.status_code == 201
            self.post_ids.append(r2.json()['id'])
            print('Finish sending posts')

    def like_post(self, token, max_likes_per_user):
        print("Start add likes")
        if not self.post_ids:
            return
        headers = self.headers
        headers['Authorization'] = 'JWT ' + token
        for _ in range(randint(0, max_likes_per_user)):
            print("Start liking post")

            post_id = choice(self.post_ids)
            url = f"{self.post_url}{post_id}/like/"
            r = requests.put(url, headers=headers)
            assert r.status_code == 200
            print("Finish liking post")


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)
    bot = AutomatedBot(host='http://127.0.0.1:8000')
    usernames = bot.generate_usernames(config['number_of_users'])
    for username in usernames:
        bot.singup(username, config['user_password'])
        token = bot.login(username, config['user_password'])
        bot.make_post(token, config['max_posts_per_user'])

    for username in usernames:
        token = bot.login(username, config['user_password'])
        bot.like_post(token, config['max_likes_per_user'])
