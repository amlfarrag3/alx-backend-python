from django.shortcuts import render
from rest_framework import viewsets, status ,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)



# === Conversation ViewSet ===
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related('participants', 'messages__sender').all()
    serializer_class = ConversationSerializer 
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids')
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "participant_ids must be a list of user IDs"}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() < 2:
            return Response({"error": "At least two valid participants are required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
# === Message ViewSet ===
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not sender_id or not message_body:
            return Response({"error": "conversation_id, sender_id, and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        if sender not in conversation.participants.all():
            return Response({"error": "Sender is not a participant of the conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)