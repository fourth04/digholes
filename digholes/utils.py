def get_settings(settings):
    return {tmp:getattr(settings, tmp) for tmp in dir(settings) if tmp.isupper()}
