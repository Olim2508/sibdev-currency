from drf_yasg import openapi

from main.serializers import AnalyticsRatesSerializer

ordering_rates_parameter = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="Ordering",
    type=openapi.TYPE_STRING,
    enum=["value", "-value"],
    enum_names=["Ascending", "Descending"],
)

analytics_params = [
    openapi.Parameter('id', openapi.IN_PATH, description='Currency ID', type=openapi.TYPE_INTEGER),
    openapi.Parameter('threshold', openapi.IN_QUERY, description='Example : 100', type=openapi.TYPE_NUMBER, required=True),
    openapi.Parameter('date_from', openapi.IN_QUERY, description='Example : 2007-03-09T00:00:00.000Z', type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
    openapi.Parameter('date_to', openapi.IN_QUERY, description='Example : 2007-03-09T00:00:00.000Z', type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
]

analytics_response = {
    '200': openapi.Response('Successful response', schema=AnalyticsRatesSerializer),
}

