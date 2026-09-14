from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .comparison import compare_records
from .serializers import DisagreementSerializer


@api_view(["GET"])
def disagreements(request):

    results = compare_records()

    reason = request.GET.get("reason")

    if reason:
        results = [
            item
            for item in results
            if item["reason"] == reason
        ]

    org = request.GET.get("org")

    if org:
        results = [
            item
            for item in results
            if item["org"] == org
        ]

    sort = request.GET.get("sort")

    if sort == "value":
        results.sort(
            key=lambda x: str(
                x["system_a_value"] or ""
            )
        )

    serializer = DisagreementSerializer(
        results,
        many=True
    )

    return Response(serializer.data)