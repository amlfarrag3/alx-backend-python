import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by user ID
    sender_id = django_filters.UUIDFilter(field_name="sender__id")

    # Filter by date range
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_id', 'sent_after', 'sent_before']
