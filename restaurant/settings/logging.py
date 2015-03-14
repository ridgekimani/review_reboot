import os
from restaurant.settings import DEBUG, BASE_DIR

if not DEBUG:
    log_path = os.path.join(BASE_DIR, 'logs/log.log')
    if os.access(log_path, os.W_OK):
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                # Include the default Django email handler for errors
                # This is what you'd get without configuring logging at all.
                'mail_admins': {
                    'class': 'django.utils.log.AdminEmailHandler',
                    'level': 'ERROR',
                     # But the emails are plain text by default - HTML is nicer
                    'include_html': True,
                },
                # Log to a text file that can be rotated by logrotate
                'logfile': {
                    'class': 'logging.handlers.WatchedFileHandler',
                    'filename': log_path
                },
            },
            'loggers': {
                # Again, default Django configuration to email unhandled exceptions
                'django.request': {
                    'handlers': ['mail_admins'],
                    'level': 'ERROR',
                    'propagate': True,
                },
                # Might as well log any errors anywhere else in Django
                'django': {
                    'handlers': ['logfile'],
                    'level': 'ERROR',
                    'propagate': False,
                },
                # Your own app - this assumes all your logger names start with "myapp."
                'app': {
                    'handlers': ['logfile'],
                    'level': 'WARNING', # Or maybe INFO or DEBUG
                    'propagate': False
                },
            },
        }