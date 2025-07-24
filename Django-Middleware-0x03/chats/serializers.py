from rest_framework import serializers
from rest_framework.exceptions import ValidationError  # For custom validation
from .models import User, Conversation, Message


# === User Serializer ===
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email','phone_number','role','created_at',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_name'] = f"{instance.first_name} {instance.last_name}"
        return data


# === Message Serializer ===
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_name',
            'message_body',
            'sent_at',
        ]

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"
    

# === Conversation Serializer (with nested messages + participants) ===
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("At least two participants are required.")
        return value


