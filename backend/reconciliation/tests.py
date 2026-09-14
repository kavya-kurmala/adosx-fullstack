
from django.test import TestCase

from .models import (
    Location,
    SystemARecord,
    SystemBEntry
)

from .comparison import compare_records


class ComparisonTests(TestCase):

    def setUp(self):

        Location.objects.create(
            location_code="LOC1",
            org="ORG1"
        )

    def test_missing_system_b(self):

        SystemARecord.objects.create(
            record_id="A1",
            location="LOC1",
            value="100",
            raw_data={}
        )

        results = compare_records()

        reasons = [
            item["reason"]
            for item in results
        ]

        self.assertIn(
            "missing_in_system_b",
            reasons
        )

    def test_missing_system_a(self):

        SystemBEntry.objects.create(
            record_ref="A999",
            location="LOC1",
            value="100",
            raw_data={}
        )

        results = compare_records()

        reasons = [
            item["reason"]
            for item in results
        ]

        self.assertIn(
            "missing_in_system_a",
            reasons
        )

    def test_duplicate_system_b(self):

        SystemARecord.objects.create(
            record_id="A1",
            location="LOC1",
            value="100",
            raw_data={}
        )

        SystemBEntry.objects.create(
            record_ref="A1",
            location="LOC1",
            value="100",
            raw_data={}
        )

        SystemBEntry.objects.create(
            record_ref="A1",
            location="LOC1",
            value="100",
            raw_data={}
        )

        results = compare_records()

        reasons = [
            item["reason"]
            for item in results
        ]

        self.assertIn(
            "duplicate_in_system_b",
            reasons
        )

    def test_value_mismatch(self):

        SystemARecord.objects.create(
            record_id="A1",
            location="LOC1",
            value="100",
            raw_data={}
        )

        SystemBEntry.objects.create(
            record_ref="A1",
            location="LOC1",
            value="200",
            raw_data={}
        )

        results = compare_records()

        reasons = [
            item["reason"]
            for item in results
        ]

        self.assertIn(
            "value_mismatch",
            reasons
        )
    def test_location_belongs_to_correct_org(self):

        Location.objects.create(
            location_code="LOC2",
            org="ORG2"
        )

        SystemARecord.objects.create(
            record_id="A2",
            location="LOC2",
            value="500",
            raw_data={}
        )

        SystemBEntry.objects.create(
            record_ref="A2",
            location="LOC2",
            value="600",
            raw_data={}
        )

        results = compare_records()

        mismatch = [
            item
            for item in results
            if item["record_id"] == "A2"
        ][0]

        self.assertEqual(
            mismatch["org"],
            "ORG2"
        )

