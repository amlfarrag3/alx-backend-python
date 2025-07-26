from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory  # Include MessageHistory
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only run on updates (not new message creation)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            return

        # Compare message body before and after change
        if old_message.message_body != instance.message_body:
            MessageHistory.objects.create(
                message=instance,
                previous_content=old_message.message_body
            )
            instance.edited = True
