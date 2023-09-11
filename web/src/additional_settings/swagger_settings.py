
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # 'basic': {
        #     'type': 'basic'
        # },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Value example: Bearer ******************',
            'in': 'header'
        },
    },
    # 'USE_SESSION_AUTH': True,
    'JSON_EDITOR': False,
    'LOGOUT_URL': 'rest_framework:logout',
    'DEFAULT_MODEL_RENDERING': 'example'
}
