from django.apps import apps

def get_all_custom_models():
    default_models = [
        'ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'User', 'Upload'
    ]
    # try to get all the apps
    return [model.__name__ for model in apps.get_models() if model.__name__ not in default_models ]
