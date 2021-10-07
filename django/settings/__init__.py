try:
    from .local import *  # noqa
except ImportError:
    import os
    raise Exception(
        '%s is missing, please add this file manually' %
        os.path.join(os.path.dirname(__file__), 'local.py')
    )
