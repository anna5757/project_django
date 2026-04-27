from rest_framework import serializers #объект в json
from task_manager.models import Tasks, Projects, Comments
from account.models import User
from task_manager.v1.serializers.attachments import AttachmentsSerializer
from task_manager.v1.serializers.comment import CommentSerialazer
from task_manager.v1.serializers.project import ProjectSerializer
from task_manager.v1.serializers.tags import TagsSerializer
from task_manager.v1.serializers.project_details import ProjectsDetailsSerializer

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    priority = serializers.IntegerField()

    assignee = serializers.SerializerMethodField()

    def get_assignee(self, obj):
        user = obj.assignee
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username
        }
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
    )

    comments = CommentSerialazer(many=True, read_only=True)

    #______ M2M
    tags = TagsSerializer(many=True, read_only=True)

    project = ProjectSerializer(read_only=True)

    attachments = AttachmentsSerializer(many=True, read_only=True)

    project_details = ProjectsDetailsSerializer(many=True, read_only=True)

    def create(self, validated_data): #validated_data-данные после проверки сериализатором
        """
        Create and return a new `Tasks` instance, given the validated data.
        """
        return Tasks.objects.create(**validated_data) #распаковка словаря

    def update(self, instance, validated_data): #validated_data - новые данные
        """
        Update and return an existing `Tasks` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name) #взять "name" из новых данных, а если его нет — оставить старое значение
        instance.description = validated_data.get("description", instance.description)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.assignee = validated_data.get("assignee", instance.assignee)
        instance.save()
        return instance


