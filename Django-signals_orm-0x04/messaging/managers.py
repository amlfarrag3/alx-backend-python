from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('message_body', 'sender', 'sent_at')   
