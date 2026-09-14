from .models import (
    Location,
    SystemARecord,
    SystemBEntry
)
FIELDS_TO_COMPARE = [
    "value",
]

def normalize_reference(value):

    if value is None:
        return ""

    value = str(value).strip().lower()

    for character in [
        " ",
        "-",
        "_",
        "/"
    ]:
        value = value.replace(
            character,
            ""
        )

    return value


def compare_records():

    disagreements = []

    locations = {
        normalize_reference(location.location_code): location.org
        for location in Location.objects.all()
    }

    system_a = list(SystemARecord.objects.all())
    system_b = list(SystemBEntry.objects.all())

    a_by_id = {}

    for record in system_a:
        key = normalize_reference(record.record_id)

        a_by_id[key] = record

    b_by_ref = {}

    for entry in system_b:

        key = normalize_reference(entry.record_ref)

        if key not in b_by_ref:
            b_by_ref[key] = []

        b_by_ref[key].append(entry)

    # ----------------------------------
    # System A -> System B comparison
    # ----------------------------------

    for record in system_a:

        record_key = normalize_reference(record.record_id)

        entries = b_by_ref.get(record_key, [])

        org = locations.get(
            normalize_reference(record.location),
            "Unknown"
        )

        # No System B entry
        if len(entries) == 0:

            disagreements.append({
                "reason": "missing_in_system_b",
                "record_id": record.record_id,
                "system_a_value": record.value,
                "system_b_value": None,
                "location": record.location,
                "org": org
            })

            continue

        # Duplicate System B entries
        if len(entries) > 1:

            disagreements.append({
                "reason": "duplicate_in_system_b",
                "record_id": record.record_id,
                "system_a_value": record.value,
                "system_b_value": [
                    entry.value for entry in entries
                ],
                "location": record.location,
                "org": org
            })

        # Compare values
        for entry in entries:

            for field in FIELDS_TO_COMPARE:

                a_value = getattr(record, field)
                b_value = getattr(entry, field)

                if a_value != b_value:

                    disagreements.append({
                "reason": f"{field}_mismatch",
                "record_id": record.record_id,
                "system_a_value": a_value,
                "system_b_value": b_value,
                "location": record.location,
                "org": org
            })

    # ----------------------------------
    # System B references nonexistent A
    # ----------------------------------

    for entry in system_b:

        entry_key = normalize_reference(
            entry.record_ref
        )

        if entry_key not in a_by_id:

            org = locations.get(
                normalize_reference(entry.location),
                "Unknown"
            )

            disagreements.append({
                "reason": "missing_in_system_a",
                "record_id": entry.record_ref,
                "system_a_value": None,
                "system_b_value": entry.value,
                "location": entry.location,
                "org": org
            })

    return disagreements