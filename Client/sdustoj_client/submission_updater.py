from data_updater.functions.submission import update_submissions
from data_updater.functions.rank import update_ranks
from data_updater.functions.utils import timestamp_cur
import time
import sys

if __name__ == '__main__':
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 2
    rank_interval = float(sys.argv[2]) if len(sys.argv) > 2 else 5

    time_submission = 0
    time_rank = 0

    while True:
        if time_submission <= 0:
            update_submissions(False)
            time_submission = interval
        if time_rank <= 0:
            update_ranks(False)
            time_rank = rank_interval
        time_submission -= 1
        time_rank -= 1
        time.sleep(1)

