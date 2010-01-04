from django.db import models
from django.contrib.auth.models import User, UNUSABLE_PASSWORD

class TwitterTokenManager(models.Manager):
    def get_uid(self, uid):
        return self.get(uid=uid)

    def create_new_user(self, twitter_info, user_manager):
        username = 'tw$%s'%twitter_info['id']
        name = twitter_info['name'].split(' ',1)+['']
        user = user_manager.create(
            username=username,
            first_name=name[0],
            last_name=name[1],
            password=UNUSABLE_PASSWORD
        )
        return user

    def create_new_twitter_user(self, twitter_info, token, user_manager=User.objects):
        user = self.create_new_user(twitter_info, user_manager)
        return self.create(
                uid=int(twitter_info['id']),
                user=user,
                key=token.key,
                secret=token.secret
        )
