from data_updater.functions.submission import update_submissions
from data_updater.functions.utils import timestamp_cur
import time
import sys

if __name__ == '__main__':
    cnt = int(sys.argv[1]) if len(sys.argv) > 1 else None
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 2
    while cnt is None or cnt > 0:
        update_submissions(False)
        # print('Complete an updating action @%s' % (timestamp_cur(),))
        time.sleep(interval)
        if cnt is not None:
            cnt -= 1

