from drf_yasg import openapi


logout_body_scheme = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['key'],
    properties={
        'key': openapi.Schema(type=openapi.TYPE_STRING)
    }
)