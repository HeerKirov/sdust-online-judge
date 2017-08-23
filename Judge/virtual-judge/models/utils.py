from sqlalchemy.orm import sessionmaker
import conf
from datetime import datetime
from models.local_pg_models import engine as local_engine


class SessionBuilder(object):
    __session = None
    __maker = None

    def __init__(self, **kwargs):
        self.__maker = sessionmaker(**kwargs)

    def session(self):
        if self.__session is None:
            self.__session = self.__maker()
        return self.__session


class RemainList(object):
    __content = None

    def __init__(self, iterator=None):
        if iter is None:
            self.__content = list()
        else:
            self.__content = list(iterator)

    def is_empty(self):
        return len(self.__content) <= 0

    def pop(self, match):
        for i in range(0, len(self.__content)):
            it = self.__content[i]
            if match(it):
                del self.__content[i]
                return it
        return None


class AlchemyUtils(object):
    @staticmethod
    def update_submission(submission, update):
        submission.time = update['time'] if 'time' in update else submission.time
        submission.memory = update['memory'] if 'memory' in update else submission.memory
        submission.status = update['status'] if 'status' in update else submission.status
        submission.finished = update['finished'] if 'finished' in update else submission.finished
        submission.score_info = update['score'] if 'score' in update else submission.score_info
        submission.judge_id = conf.judger_id
        submission.update_time = datetime.now()


local_psql = SessionBuilder(bind=local_engine)
