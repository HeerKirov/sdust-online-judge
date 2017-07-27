from data_updater.functions.environment import update_environments
from data_updater.functions.problem import update_problems
from data_updater.functions.category import update_categories
import time
import sys


if __name__ == '__main__':
    cnt = int(sys.argv[1]) if len(sys.argv) > 1 else None
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
    while cnt is None or cnt > 0:
        update_environments(True)
        update_problems(True)
        update_categories(True)
        # print('Complete an updating action @%s' % (timestamp_cur(),))
        if cnt is not None:
            cnt -= 1
        if cnt is None or cnt > 0:
            time.sleep(interval)
