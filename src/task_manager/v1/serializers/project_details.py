from rest_framework import serializers
from task_manager.models import ProjectsDetails


class ProjectsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsDetails
        fields = ("info", "project")
