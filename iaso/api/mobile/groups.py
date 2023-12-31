from django.db.models.query import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from iaso.api.query_params import APP_ID
from iaso.api.serializers import AppIdSerializer
from iaso.models import Group, Project


class MobileGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class MobileGroupsViewSet(ListModelMixin, GenericViewSet):
    """Groups API for Mobile.

    Allows to retrieve a list of groups from the API.

    Returns a lighter payload adapted for the mobile application.

    `GET /api/mobile/groups/?app_id=some.app.id`
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = MobileGroupSerializer

    app_id_param = openapi.Parameter(
        name=APP_ID,
        in_=openapi.IN_QUERY,
        required=True,
        description="Application id (`Project.app_id`)",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        responses={
            200: f"List of groups for the given '{APP_ID}'.",
            400: f"Parameter '{APP_ID}' is required.",
            404: f"Project for given '{APP_ID}' doesn't exist.",
        },
        manual_parameters=[app_id_param],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        app_id = AppIdSerializer(data=self.request.query_params).get_app_id(raise_exception=True)
        project_qs = Project.objects.select_related("account__default_version")
        project = get_object_or_404(project_qs, app_id=app_id)
        return Group.objects.filter(source_version=project.account.default_version)
