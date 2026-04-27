from rest_framework import mixins, generics

from task_manager.models import ProjectsDetails
from task_manager.v1.serializers.project_details import ProjectsDetailsSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['ProjectsDetails'])
class ProjectsDetailsApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = ProjectsDetails.objects.all()
    serializer_class = ProjectsDetailsSerializer

    @extend_schema(
        summary='Get all details',
        description='Get all details',
        responses={200: ProjectsDetailsSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create details',
        description='Create details',
        request=ProjectsDetailsSerializer,
        responses={201: ProjectsDetailsSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        request=ProjectsDetailsSerializer,
        responses={200: ProjectsDetailsSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)