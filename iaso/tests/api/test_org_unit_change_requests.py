import time_machine

from django.contrib.gis.geos import Point

from iaso.api.org_unit_change_requests import OrgUnitChangeRequestListSerializer
from iaso.test import TestCase
from iaso.test import APITestCase
from iaso import models as m


@time_machine.travel("2023-10-09T13:00:00.000Z", tick=False)
class OrgUnitChangeRequestListSerializerTestCase(TestCase):
    """
    Test list serializer.
    """

    @classmethod
    def setUpTestData(cls):
        cls.org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        cls.org_unit = m.OrgUnit.objects.create(org_unit_type=cls.org_unit_type)

        cls.form = m.Form.objects.create(name="Vaccine form")
        cls.instance = m.Instance.objects.create(form=cls.form, org_unit=cls.org_unit)

        cls.account = m.Account.objects.create(name="Account")
        cls.user = cls.create_user_with_profile(username="user", account=cls.account)

    def test_serialization_of_change_request(self):
        kwargs = {
            "org_unit": self.org_unit,
            "created_by": self.user,
            "new_org_unit_type": self.org_unit_type,
            "new_location": Point(-2.4747713, 47.3358576, 1.3358576),
            "approved_fields": ["new_org_unit_type"],
        }
        change_request = m.OrgUnitChangeRequest.objects.create(**kwargs)

        serializer = OrgUnitChangeRequestListSerializer(change_request)

        self.assertEqual(
            serializer.data,
            {
                "id": change_request.pk,
                "org_unit_id": self.org_unit.pk,
                "org_unit_uuid": self.org_unit.uuid,
                "org_unit_name": self.org_unit.name,
                "org_unit_type_id": self.org_unit.org_unit_type.pk,
                "org_unit_type_name": self.org_unit.org_unit_type.name,
                "status": change_request.status.value,
                "groups": [],
                "requested_fields": serializer.data["requested_fields"],
                "approved_fields": serializer.data["approved_fields"],
                "rejection_comment": "",
                "created_by": "user",
                "created_at": "2023-10-09T13:00:00Z",
                "updated_by": "",
                "updated_at": None,
            },
        )
        self.assertCountEqual(serializer.data["requested_fields"], ["new_org_unit_type", "new_location"])
        self.assertCountEqual(serializer.data["approved_fields"], ["new_org_unit_type"])


class OrgUnitChangeRequestAPITestCase(APITestCase):
    """
    Test ViewSet.
    """

    @classmethod
    def setUpTestData(cls):
        data_source = m.DataSource.objects.create(name="Data source")
        version = m.SourceVersion.objects.create(number=1, data_source=data_source)
        account = m.Account.objects.create(name="Account", default_version=version)
        project = m.Project.objects.create(name="Project", account=account, app_id="foo.bar.baz")

        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(org_unit_type=org_unit_type, version=version)

        user = cls.create_user_with_profile(username="user", account=account)

        data_source.projects.set([project])
        org_unit_type.projects.set([project])
        user.iaso_profile.org_units.set([org_unit])

        cls.org_unit = org_unit
        cls.project = project
        cls.user = user

    def test_list_ok(self):
        m.OrgUnitChangeRequest.objects.create(org_unit=self.org_unit, new_name="Foo")
        m.OrgUnitChangeRequest.objects.create(org_unit=self.org_unit, new_name="Bar")

        self.client.force_authenticate(self.user)

        with self.assertNumQueries(6):
            # OrgUnit.filter_for_user_and_app_id()
            #   1. SELECT OrgUnit
            # ViewSet.get_queryset
            #   2. COUNT(*)
            #   3. SELECT OrgUnitChangeRequest
            #   4. PREFETCH OrgUnit.groups
            #   5. PREFETCH OrgUnitChangeRequest.new_groups
            #   6. PREFETCH OrgUnitChangeRequest.new_reference_instances
            response = self.client.get("/api/orgunits/changes/")
            self.assertJSONResponse(response, 200)
            self.assertEqual(2, len(response.data))

    def test_list_without_auth(self):
        response = self.client.get("/api/orgunits/changes/")
        self.assertJSONResponse(response, 403)
