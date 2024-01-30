if not receiving the message of succeeded

do as below :

pip install gevent

celery -A awd_main worker -l info -P gevent


ngrok command :
ngrok http 8000
then replace response url in settings :
CSRF_TRUSTED_ORIGINS
BASE_URL