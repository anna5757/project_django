from rest_framework import serializers
from task_manager.models import Tags


class TagsSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Tags
        fields = ("id", "name", "tasks")
