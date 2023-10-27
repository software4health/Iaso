import datetime
import time_machine
import uuid

from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from iaso.api.org_unit_change_requests.serializers import (
    InstanceForChangeRequestSerializer,
    MobileOrgUnitChangeRequestListSerializer,
    OrgUnitChangeRequestListSerializer,
    OrgUnitChangeRequestWriteSerializer,
    OrgUnitForChangeRequestSerializer,
    OrgUnitChangeRequestReviewSerializer,
    OrgUnitChangeRequestRetrieveSerializer,
)
from iaso.models import OrgUnitChangeRequest
from iaso.test import TestCase
from iaso import models as m


class InstanceForChangeRequestSerializerTestCase(TestCase):
    """
    Test nested Instance serializer.
    """

    @classmethod
    def setUpTestData(cls):
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(org_unit_type=org_unit_type)
        form = m.Form.objects.create(name="Vaccine form")
        instance = m.Instance.objects.create(form=form, org_unit=org_unit, json={"key1": "value1", "key2": "value2"})

        cls.form = form
        cls.instance = instance

    def test_serialize_instance(self):
        serializer = InstanceForChangeRequestSerializer(self.instance)
        self.assertEqual(
            serializer.data,
            {
                "id": self.instance.pk,
                "form_id": self.form.pk,
                "form_name": "Vaccine form",
                "values": {
                    "key1": "value1",
                    "key2": "value2",
                },
            },
        )


class OrgUnitForChangeRequestSerializerTestCase(TestCase):
    """
    Test nested OrgUnit serializer.
    """

    @classmethod
    def setUpTestData(cls):
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(
            org_unit_type=org_unit_type,
            location=Point(-2.4747713, 47.3358576, 10.0),
            opening_date=datetime.date(2023, 10, 27),
            closed_date=datetime.date(2025, 10, 27),
        )
        group1 = m.Group.objects.create(name="Group 1")
        group2 = m.Group.objects.create(name="Group 2")
        org_unit.groups.set([group1, group2])
        form = m.Form.objects.create(name="Vaccine form")
        instance = m.Instance.objects.create(form=form, org_unit=org_unit, json={"key1": "value1", "key2": "value2"})
        # Mark `instance` as a reference instance of `form` for `org_unit`.
        m.OrgUnitReferenceInstance.objects.create(org_unit=org_unit, instance=instance, form=form)

        cls.form = form
        cls.group1 = group1
        cls.group2 = group2
        cls.instance = instance
        cls.org_unit = org_unit
        cls.org_unit_type = org_unit_type

    def test_serialize_org_unit(self):
        serializer = OrgUnitForChangeRequestSerializer(self.org_unit)
        self.assertEqual(
            serializer.data,
            {
                "id": self.org_unit.pk,
                "parent": "",
                "name": "",
                "org_unit_type_id": self.org_unit_type.pk,
                "org_unit_type_name": "Org unit type",
                "groups": [
                    {"id": self.group1.id, "name": "Group 1"},
                    {"id": self.group2.id, "name": "Group 2"},
                ],
                "location": {
                    "latitude": 47.3358576,
                    "longitude": -2.4747713,
                    "altitude": 10.0,
                },
                "opening_date": "2023-10-27",
                "closed_date": "2025-10-27",
                "reference_instances": [
                    {
                        "id": self.instance.pk,
                        "form_id": self.form.pk,
                        "form_name": "Vaccine form",
                        "values": {
                            "key1": "value1",
                            "key2": "value2",
                        },
                    }
                ],
            },
        )


@time_machine.travel("2023-10-09T13:00:00.000Z", tick=False)
class OrgUnitChangeRequestListSerializerTestCase(TestCase):
    """
    Test list for web serializer.
    """

    @classmethod
    def setUpTestData(cls):
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(org_unit_type=org_unit_type)

        group = m.Group.objects.create(name="Group")
        org_unit.groups.set([group])

        account = m.Account.objects.create(name="Account")
        user = cls.create_user_with_profile(username="user", account=account)

        cls.group = group
        cls.org_unit = org_unit
        cls.org_unit_type = org_unit_type
        cls.user = user

    def test_serialize_change_request(self):
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
                "uuid": str(change_request.uuid),
                "org_unit_id": self.org_unit.pk,
                "org_unit_uuid": self.org_unit.uuid,
                "org_unit_name": self.org_unit.name,
                "org_unit_type_id": self.org_unit.org_unit_type.pk,
                "org_unit_type_name": self.org_unit.org_unit_type.name,
                "status": change_request.status.value,
                "groups": [
                    {"id": self.group.id, "name": "Group"},
                ],
                "requested_fields": serializer.data["requested_fields"],
                "approved_fields": serializer.data["approved_fields"],
                "rejection_comment": "",
                "created_by": "user",
                "created_at": 1696856400.0,
                "updated_by": "",
                "updated_at": None,
            },
        )
        self.assertCountEqual(serializer.data["requested_fields"], ["new_org_unit_type", "new_location"])
        self.assertCountEqual(serializer.data["approved_fields"], ["new_org_unit_type"])


@time_machine.travel("2023-10-13T13:00:00.000Z", tick=False)
class MobileOrgUnitChangeRequestListSerializerTestCase(TestCase):
    """
    Test list for mobile serializer.
    """

    @classmethod
    def setUpTestData(cls):
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(org_unit_type=org_unit_type)

        form = m.Form.objects.create(name="Vaccine form")
        account = m.Account.objects.create(name="Account")
        user = cls.create_user_with_profile(username="user", account=account)

        cls.form = form
        cls.org_unit = org_unit
        cls.org_unit_type = org_unit_type
        cls.user = user

    def test_serialize_ok(self):
        kwargs = {
            "org_unit": self.org_unit,
            "created_by": self.user,
            "new_org_unit_type": self.org_unit_type,
            "new_location": Point(-2.4747713, 47.3358576, 10.0),
            "new_opening_date": datetime.date(2022, 10, 27),
            "new_closed_date": datetime.date(2024, 10, 27),
            "approved_fields": ["new_org_unit_type"],
        }
        change_request = m.OrgUnitChangeRequest.objects.create(**kwargs)
        new_group = m.Group.objects.create(name="new group")
        change_request.new_groups.set([new_group])
        new_instance = m.Instance.objects.create(form=self.form, org_unit=self.org_unit)
        change_request.new_reference_instances.set([new_instance])

        serializer = MobileOrgUnitChangeRequestListSerializer(change_request)

        self.assertEqual(
            serializer.data,
            {
                "id": change_request.pk,
                "uuid": str(change_request.uuid),
                "org_unit_id": self.org_unit.pk,
                "org_unit_uuid": self.org_unit.uuid,
                "status": change_request.status.value,
                "approved_fields": ["new_org_unit_type"],
                "rejection_comment": "",
                "created_at": 1697202000.0,
                "updated_at": None,
                "new_parent_id": None,
                "new_name": "",
                "new_org_unit_type_id": self.org_unit_type.pk,
                "new_groups": [new_group.pk],
                "new_location": {
                    "latitude": 47.3358576,
                    "longitude": -2.4747713,
                    "altitude": 10.0,
                },
                "new_location_accuracy": None,
                "new_opening_date": "2022-10-27",
                "new_closed_date": "2024-10-27",
                "new_reference_instances": [new_instance.pk],
            },
        )


@time_machine.travel("2023-10-19T17:00:00.000Z", tick=False)
class OrgUnitChangeRequestRetrieveSerializerTestCase(TestCase):
    """
    Test retrieve serializer.
    """

    @classmethod
    def setUpTestData(cls):
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        org_unit = m.OrgUnit.objects.create(org_unit_type=org_unit_type)

        form = m.Form.objects.create(name="Vaccine form")
        account = m.Account.objects.create(name="Account")
        user = cls.create_user_with_profile(username="user", account=account)

        cls.form = form
        cls.org_unit = org_unit
        cls.org_unit_type = org_unit_type
        cls.user = user

    def test_serialize_ok(self):
        kwargs = {
            "org_unit": self.org_unit,
            "created_by": self.user,
            "new_org_unit_type": self.org_unit_type,
            "new_opening_date": datetime.date(2022, 10, 27),
            "new_closed_date": datetime.date(2024, 10, 27),
        }
        change_request = m.OrgUnitChangeRequest.objects.create(**kwargs)
        new_group = m.Group.objects.create(name="new group")
        change_request.new_groups.set([new_group])

        serializer = OrgUnitChangeRequestRetrieveSerializer(change_request)

        self.assertEqual(
            serializer.data,
            {
                "id": change_request.pk,
                "uuid": str(change_request.uuid),
                "status": "new",
                "created_by": "user",
                "created_at": 1697734800.0,
                "updated_by": "",
                "updated_at": None,
                "requested_fields": ["new_org_unit_type", "new_opening_date", "new_closed_date", "new_groups"],
                "approved_fields": [],
                "rejection_comment": "",
                "org_unit": {
                    "id": self.org_unit.pk,
                    "parent": "",
                    "name": "",
                    "org_unit_type_id": self.org_unit_type.pk,
                    "org_unit_type_name": self.org_unit_type.name,
                    "groups": [],
                    "location": None,
                    "opening_date": None,
                    "closed_date": None,
                    "reference_instances": [],
                },
                "new_parent": "",
                "new_name": "",
                "new_org_unit_type_id": self.org_unit_type.pk,
                "new_org_unit_type_name": "Org unit type",
                "new_groups": [
                    {
                        "id": new_group.pk,
                        "name": "new group",
                    },
                ],
                "new_location": None,
                "new_location_accuracy": None,
                "new_opening_date": "2022-10-27",
                "new_closed_date": "2024-10-27",
                "new_reference_instances": [],
            },
        )


class OrgUnitChangeRequestWriteSerializerTestCase(TestCase):
    """
    Test write serializer.
    """

    @classmethod
    def setUpTestData(cls):
        cls.org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        cls.org_unit = m.OrgUnit.objects.create(
            org_unit_type=cls.org_unit_type, location=Point(-2.4747713, 47.3358576, 10.0)
        )

    def test_deserialize_ok(self):
        data = {
            "uuid": "e05933f4-8370-4329-8cf5-197941785a24",
            "org_unit_id": self.org_unit.id,
            "new_name": "Foo",
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_generate_uuid_if_not_provided(self):
        data = {
            "org_unit_id": self.org_unit.id,
            "new_name": "Foo",
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(isinstance(serializer.validated_data["uuid"], uuid.UUID))

    def test_validate(self):
        data = {
            "org_unit_id": self.org_unit.id,
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("You must provide at least one of the following fields", serializer.errors["non_field_errors"][0])

    def test_validate_new_parent_version(self):
        data_source = m.DataSource.objects.create(name="Data source")
        version1 = m.SourceVersion.objects.create(number=1, data_source=data_source)
        version2 = m.SourceVersion.objects.create(number=2, data_source=data_source)
        parent_org_unit = m.OrgUnit.objects.create(org_unit_type=self.org_unit_type, version=version2)
        self.org_unit.version = version1
        self.org_unit.save()
        data = {
            "org_unit_id": self.org_unit.id,
            "new_parent_id": parent_org_unit.id,
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "`new_parent_id` and `org_unit_id` must have the same version.", serializer.errors["non_field_errors"][0]
        )

    def test_validate_new_parent_hierarchy(self):
        child_org_unit = m.OrgUnit.objects.create(org_unit_type=self.org_unit_type, parent=self.org_unit)
        self.org_unit.save()
        data = {
            "org_unit_id": self.org_unit.id,
            "new_parent_id": child_org_unit.id,
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("`new_parent_id` is already a child of `org_unit_id`.", serializer.errors["non_field_errors"][0])

    def test_validate_new_org_unit_type_id(self):
        data_source = m.DataSource.objects.create(name="Data source")
        version = m.SourceVersion.objects.create(number=1, data_source=data_source)
        account = m.Account.objects.create(name="Account", default_version=version)
        project = m.Project.objects.create(name="Project", account=account, app_id="foo.bar.baz")
        org_unit_type = m.OrgUnitType.objects.create(name="Org unit type")
        data_source.projects.set([project])
        org_unit_type.projects.set([project])

        other_account = m.Account.objects.create(name="Other account")
        user = self.create_user_with_profile(username="user", account=other_account)

        request = APIRequestFactory().get("/")
        request.user = user

        data = {
            "org_unit_id": self.org_unit.id,
            "new_org_unit_type_id": org_unit_type.id,
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "`new_org_unit_type_id` is not part of the user account.", serializer.errors["new_org_unit_type_id"][0]
        )

    def test_validate_new_reference_instances(self):
        form = m.Form.objects.create(name="Vaccine form 1")
        instance1 = m.Instance.objects.create(form=form, org_unit=self.org_unit)
        instance2 = m.Instance.objects.create(form=form, org_unit=self.org_unit)
        data = {
            "org_unit_id": self.org_unit.id,
            "new_reference_instances": [instance1.id, instance2.id],
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Only one reference instance can exist by org_unit/form pair.",
            serializer.errors["new_reference_instances"][0],
        )

    def test_deserialize_ok_with_all_data(self):
        group1 = m.Group.objects.create(name="Group 1")
        group2 = m.Group.objects.create(name="Group 2")

        form1 = m.Form.objects.create(name="Vaccine form 1")
        instance1 = m.Instance.objects.create(form=form1, org_unit=self.org_unit)
        form2 = m.Form.objects.create(name="Vaccine form 2")
        instance2 = m.Instance.objects.create(form=form2, org_unit=self.org_unit)

        parent_org_unit = m.OrgUnit.objects.create(org_unit_type=self.org_unit_type)

        data = {
            "uuid": "e05933f4-8370-4329-8cf5-197941785a24",
            "org_unit_id": self.org_unit.id,
            "new_parent_id": parent_org_unit.id,
            "new_name": "Foo",
            "new_org_unit_type_id": self.org_unit_type.id,
            "new_groups": [group1.id, group2.id],
            "new_location": {
                "latitude": 47.3358576,
                "longitude": -2.4747713,
                "altitude": 10.0,
            },
            "new_location_accuracy": 4.0,
            "new_reference_instances": [instance1.id, instance2.id],
        }
        serializer = OrgUnitChangeRequestWriteSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        change_request = OrgUnitChangeRequest.objects.get(uuid=data["uuid"])
        self.assertEqual(change_request.org_unit, self.org_unit)
        self.assertEqual(change_request.new_parent, parent_org_unit)
        self.assertEqual(change_request.new_name, "Foo")
        self.assertEqual(change_request.new_org_unit_type, self.org_unit_type)
        new_groups = change_request.new_groups.all()
        self.assertIn(group1, new_groups)
        self.assertIn(group2, new_groups)
        self.assertEqual(change_request.new_location, Point(-2.4747713, 47.3358576, 10.0, srid=4326))
        self.assertEqual(change_request.new_location_accuracy, 4.0)
        new_reference_instances = change_request.new_reference_instances.all()
        self.assertIn(instance1, new_reference_instances)
        self.assertIn(instance2, new_reference_instances)


class OrgUnitChangeRequestReviewSerializerTestCase(TestCase):
    """
    Test review serializer.
    """

    @classmethod
    def setUpTestData(cls):
        cls.org_unit = m.OrgUnit.objects.create()
        cls.change_request = m.OrgUnitChangeRequest.objects.create(org_unit=cls.org_unit, new_name="Foo")

    def test_serialize_ok(self):
        data = {
            "status": self.change_request.Statuses.APPROVED,
            "approved_fields": ["new_name"],
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        data = {
            "status": self.change_request.Statuses.REJECTED,
            "rejection_comment": "Not good enough",
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_status(self):
        data = {
            "status": OrgUnitChangeRequest.Statuses.NEW,
            "approved_fields": ["new_name"],
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(error.exception.detail["status"][0], "Must be `approved` or `rejected`.")

    def test_validate_approved_fields(self):
        data = {
            "status": OrgUnitChangeRequest.Statuses.APPROVED,
            "approved_fields": ["new_name", "foo"],
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(error.exception.detail["approved_fields"][0], "Value foo is not a valid choice.")

    def test_validate(self):
        data = {
            "status": OrgUnitChangeRequest.Statuses.REJECTED,
            "rejection_comment": "",
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(error.exception.detail["non_field_errors"][0], "A `rejection_comment` must be provided.")

        data = {
            "status": OrgUnitChangeRequest.Statuses.APPROVED,
            "approved_fields": [],
        }
        serializer = OrgUnitChangeRequestReviewSerializer(data=data)
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            error.exception.detail["non_field_errors"][0], "At least one `approved_fields` must be provided."
        )
