from celery import shared_task
from .views import *

# in order for celery to work, one has to run these commands simultaneously in two different terminals:
# celery -A GoodnessGroceries_Project worker -l info
# celery -A GoodnessGroceries_Project beat -l info


@shared_task
def test_task():
    check_for_files(o_path)
