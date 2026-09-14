import csv
import os

from django.core.management.base import BaseCommand

from reconciliation.models import (
    Location,
    SystemARecord,
    SystemBEntry,
    ImportErrorRow
)


class Command(BaseCommand):
    help = "Import System A, System B and location CSV files"

    def handle(self, *args, **kwargs):

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../../data")
        )

        locations_file = os.path.join(base_dir, "locations.csv")
        system_a_file = os.path.join(base_dir, "system_a.csv")
        system_b_file = os.path.join(base_dir, "system_b.csv")

        self.import_locations(locations_file)
        self.import_system_a(system_a_file)
        self.import_system_b(system_b_file)

        self.stdout.write(
            self.style.SUCCESS("Import completed successfully.")
        )

    def import_locations(self, file_path):

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                location = row.get("location", "").strip()

                if not location:
                    location = row.get("location_code", "").strip()

                org = row.get("org", "").strip()

                Location.objects.update_or_create(
                    location_code=location,
                    defaults={
                        "org": org
                    }
                )

    def import_system_a(self, file_path):

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                record_id = row.get("record_id", "").strip()

                if not record_id:

                    ImportErrorRow.objects.create(
                        source="system_a",
                        row_number=reader.line_num,
                        raw_data=dict(row),
                        error="Missing record_id"
                    )

                continue

                location = str(
                    row.get("location", "")
                ).strip()

                value = str(
                    row.get("value", "")
                ).strip()

                SystemARecord.objects.update_or_create(
                    record_id=record_id,
                    defaults={
                        "location": location,
                        "value": value,
                        "raw_data": row
                    }
                )

    def import_system_b(self, file_path):

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                record_ref = str(
                    row.get("record_ref", "")
                ).strip()

                location = str(
                    row.get("location", "")
                ).strip()

                value = str(
                    row.get("value", "")
                ).strip()

                SystemBEntry.objects.create(
                    record_ref=record_ref,
                    location=location,
                    value=value,
                    raw_data=row
                )