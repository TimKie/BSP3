from .views import *


def my_scheduled_job():
    check_for_files(o_path)
    print("Test print for crontab!")
    f = open('/Users/tim/Desktop/cronlogtest.txt', 'w')
    f.close()
