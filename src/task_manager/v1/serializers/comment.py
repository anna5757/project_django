from rest_framework import serializers
from task_manager.models import Comments

class CommentSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'message')