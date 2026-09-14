from django.db import models

# Create your models here.



class Location(models.Model):
    location_code = models.CharField(max_length=255, unique=True)
    org = models.CharField(max_length=255)

    def __str__(self):
        return self.location_code


class SystemARecord(models.Model):
    record_id = models.CharField(max_length=255, unique=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    value = models.CharField(max_length=255, blank=True, null=True)

    raw_data = models.JSONField(default=dict)

    imported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_id


class SystemBEntry(models.Model):
    record_ref = models.CharField(max_length=255, blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    value = models.CharField(max_length=255, blank=True, null=True)

    raw_data = models.JSONField(default=dict)

    imported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.record_ref)
class ImportErrorRow(models.Model):

    source = models.CharField(max_length=50)

    row_number = models.IntegerField()

    raw_data = models.JSONField(default=dict)

    error = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )