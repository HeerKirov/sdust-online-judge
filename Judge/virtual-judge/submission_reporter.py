from models.redis_models import Submission
from models.utils import AlchemyUtils
from models import pg_models
from sqlalchemy.orm import sessionmaker
from functions import hdu, poj
from datetime import datetime
import conf

# 轮询解析队列并处理提交回填
PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()

reporter_functions = {
    'hdu': hdu.update_submit,
    'poj': poj.update_submit
}


def handler(sid):
    status = Submission.get_status(sid)  # 获得该提交的数据。
    oj = status['oj'] if status is not None and 'oj' in status else None
    if oj is not None:
        print("Report Submission: sid=%s, oj=%s" % (sid, oj))
        is_ok, new_status, update = reporter_functions[oj](sid, status)
        # 回执的ret为(isOk, status, update)。包括轮询完成标志和新的status，以及做出的修改。
        # update包括如下内容：
        # status, score, time, memory, finished
        if is_ok and status is not None:
            Submission.unmark(sid)
        else:
            Submission.push(sid)
            Submission.mark(sid, new_status)
        if update is not None:  # 该项不为None时，需要对sdustoj的提交做出修改。
            submission = pg_session.query(pg_models.Submission).filter_by(id=sid).first()
            AlchemyUtils.update_submission(submission, update)
            pg_session.commit()
    else:
        Submission.unmark(sid)

Submission.analyse_mark_submissions(handler)
