from rest_framework import mixins, generics

from task_manager.models import Attachments
from task_manager.v1.serializers.attachments import AttachmentsSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Attachments'])
class AttachmentApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer

    @extend_schema(
        summary='Get all attachments',
        description='Get all attachments',
        responses={200: AttachmentsSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create attachment',
        description='Create attachment',
        request=AttachmentsSerializer,
        responses={201: AttachmentsSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        request=AttachmentsSerializer,
        responses={200: AttachmentsSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)