from rest_framework import serializers

from account.models import User
from task_manager.models import Comments, Tasks


class CommentSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'message')

class CommentUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user"
    )
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Tasks.objects.all(),
        source="task"
    )
    class Meta:
        model = Comments
        fields = (
            "id",
            "message",
            "user_id",
            "task_id",
        )