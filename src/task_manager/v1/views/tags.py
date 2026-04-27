from rest_framework.decorators import api_view
from rest_framework.response import Response

from task_manager.models import Tags
from task_manager.v1.serializers.tags import TagsSerializer

from rest_framework import status


from rest_framework import mixins, generics
from drf_spectacular.utils import extend_schema
#
# @api_view(['GET'])
# def tags_list(request):
#     tags = Tags.objects.all()
#     serializer = TagsSerializer(tags, many=True)
#     return Response(serializer.data)
@extend_schema(tags=['Tags'])
class TagsApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    @extend_schema(
        summary='Get all tags',
        description='Get all tags',
        responses={200: TagsSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create tag',
        description='Create tag',
        responses={200: TagsSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        request=TagsSerializer,
        responses={200: TagsSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)