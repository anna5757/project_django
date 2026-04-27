from rest_framework import mixins, generics

from task_manager.models import Comments
from task_manager.v1.serializers.comment import CommentUpdateSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Comments'])
class CommentApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Comments.objects.all()
    serializer_class = CommentUpdateSerializer

    @extend_schema(
        summary='Get all comments',
        description='Get all comments',
        responses={200: CommentUpdateSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create comment',
        description='Create comment',
        request=CommentUpdateSerializer,
        responses={201: CommentUpdateSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        request=CommentUpdateSerializer,
        responses={200: CommentUpdateSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)