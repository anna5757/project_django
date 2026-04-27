from rest_framework import mixins, generics

from task_manager.models import Projects
from task_manager.v1.serializers.project import ProjectSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Projects'])
class ProjectsApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    @extend_schema(
        summary='Get all projects',
        description='Get all projects',
        responses={200: ProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create project',
        description='Create project',
        request=ProjectSerializer,
        responses={201: ProjectSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Projects'])
class ProjectDetailApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


    @extend_schema(
        responses={200: ProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)