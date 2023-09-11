from drf_yasg import openapi


ordering_rates_parameter = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="Ordering",
    type=openapi.TYPE_STRING,
    enum=["value", "-value"],
    enum_names=["Ascending", "Descending"],
)

