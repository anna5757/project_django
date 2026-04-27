from rest_framework import serializers
from task_manager.models import Attachments


class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = ("name", "task")
