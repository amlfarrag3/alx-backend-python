from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory  # Include MessageHistory
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models.signals import post_delete
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete related notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message histories of messages sent by this user
    MessageHistory.objects.filter(message__sender=instance).delete()


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            return

        if old_message.message_body != instance.message_body:
            MessageHistory.objects.create(
                message=instance,
                previous_content=old_message.message_body
            )
            instance.edited = True
            instance.edited_at = timezone.now()



