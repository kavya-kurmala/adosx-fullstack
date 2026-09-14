from rest_framework import serializers


class DisagreementSerializer(serializers.Serializer):

    reason = serializers.CharField()

    record_id = serializers.CharField()

    system_a_value = serializers.JSONField(
        allow_null=True
    )

    system_b_value = serializers.JSONField(
        allow_null=True
    )

    location = serializers.CharField(
        allow_blank=True
    )

    org = serializers.CharField()