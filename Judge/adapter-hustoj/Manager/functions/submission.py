# -*- coding: utf-8 -*-
from datetime import datetime

from models import pg_models, mysql_models
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from conf import language, user, try_max, judger, status as status_map, final_status, priority

from functions.problem import get_problem_title, update as update_problem

from models.redis_models import Submission

from .log import print_log

from conf import judger_id

PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()

MysqlSession = sessionmaker(bind=mysql_models.engine)
mysql_session = MysqlSession()


def update(**kwargs):
    global mysql_session, pg_session
    # 可以看出来该函数的作用是：根据获得的提交ID，将此提交同步到hustoj上进行评测。
    # 同时，还将这次提交的状态加入本地的解析队列，使问题等待被解析回填到sdustoj上。
    sid = int(kwargs['sid'])  # 获得本次提交的ID
    # 获得提交信息
    language_name = kwargs['language']
    language_id = language[language_name]  # 提交所使用的语言
    submission = pg_session.query(pg_models.Submission).filter_by(id=sid).first()  # 查询sdustoj数据库中的该submission
    code = pg_session.query(pg_models.SubmissionCode).filter_by(submission_id=sid).first().code['code']  # 查询该提交的代码

    # by hk in 2017.05.18======
    # 查询编程限制。
    limits = pg_session.query(pg_models.Limit).filter_by(problem_id=submission.problem_id).all()
    max_length = None
    for limit in limits:
        environment = pg_session.query(pg_models.Environment).filter_by(id=limit.environment_id).first()
        if environment.judge_id == language_name:  # 确认这是正在使用的编程环境
            max_length = limit.length_limit
            break

    code_length = len(code)
    if max_length is not None and code_length > max_length:  # 可以知道长度超出限制
        finished = True
        status = 'LLE'
        table = pg_models.Submission.__table__  # 测试数据状态的表本身？
        pg_session.execute(
            table.update().where(table.c.id == sid), {'status': status, 'finished': finished}
        )  # 看起来这句话的意思是更新该条提交在sdustoj数据库中的信息……
        submission.judge_id = judger_id  # 更新评测机的ID为本机ID。
        pg_session.commit()  # 提交更改
        return

    # 处理禁用单词
    invalid_words = pg_session.query(pg_models.InvalidWord).filter_by(problem_id=submission.problem_id).all()
    for invalid_word in invalid_words:
        if invalid_word.word in code:  # 代码包含该禁用单词
            finished = True
            status = 'IW'
            table = pg_models.Submission.__table__  # 测试数据状态的表本身？
            pg_session.execute(
                table.update().where(table.c.id == sid), {'status': status, 'finished': finished}
            )  # 看起来这句话的意思是更新该条提交在sdustoj数据库中的信息……
            submission.judge_id = judger_id  # 更新评测机的ID为本机ID。
            pg_session.commit()  # 提交更改
            return

    # ======================

    # 根据分拆的题目生成相应的HUSTOJ提交
    problem_test = pg_session.query(pg_models.ProblemTestData).filter_by(
        problem_id=submission.problem_id, deleted=False
    ).all()  # 查询全部sdustoj中的该提交的题目的测试数据。
    ok = False
    submission_create = []
    submission_mark = []
    tried = 0  # 定义为已经尝试的提交次数。
    while ok is False:
        # 查询题目，生成提交
        ok = True
        submission_create.clear()  # 按照规则，每一次重跑这个while循环都是一次从头开始尝试提交的过程，因此全部清空。
        submission_mark.clear()
        tried += 1
        for pt in problem_test:  # 循环遍历所有的测试数据。
            title = get_problem_title(pt.problem_id, pt.test_data_id)  # 按照规范获取该测试数据对应的题目的title
            try:
                problem = mysql_session.query(mysql_models.Problem).filter_by(title=title).first()
            except OperationalError:
                # MySQL数据库因为长连接断开。重连一次。
                mysql_session = MysqlSession()
                problem = None
            # 从hustoj数据库查询每一组测试数据对应的题目
            if problem is None:
                # 若未找到题目，可能是题目尚未更新，更新题目后重新生成
                update_problem(pid=pt.problem_id)
                ok = False  # 这代表将会跳出提交过程并从头开始尝试提交。
                break  # 将跳转到下面那个if

            solution = mysql_models.Solution(
                problem_id=problem.problem_id,
                user_id=user['user_id'],
                language=language_id,
                ip=str(submission.ip),
                code_length=submission.length,
                judger=judger,
                in_date=submission.submit_time
            )  # 构造一个hustoj的提交

            submission_create.append(solution)  # 这个列表记录了所有的提交。
            submission_mark.append((pt.test_data_id, solution))  # 这个列表记录了一个sdustoj测试数据ID与hustoj提交信息的元组。
            # 将这个提交记入列表。

        if (not ok) and tried > try_max:  # 如果不断跳出（即一直找不到更新的题目）
            # 若尝试一定次数后仍未找到题目，有可能此提交信息有问题，放弃生成
            break

    mysql_session.add_all(submission_create)
    mysql_session.commit()
    # 执行到这里就是已经成功生成了全部的提交，将它们同步到hustoj数据库

    code_create = []
    code_user_create = []
    sub_mark = []  # 标记的列表。内容为元组(测试数据ID,提交submission的ID).
    for tid, sub in submission_mark:  # 提取所有的测试数据ID与提交信息内容
        print_log('Submission Updated: %s' % (sub.solution_id,))
        # 向数据库中写入代码
        code_create.append(mysql_models.SourceCode(  # 似乎这个SourceCode是提交的代码
            solution_id=sub.solution_id,
            source=code
        ))
        code_user_create.append(mysql_models.SourceCodeUser(  # 这个SourceCodeUser是……？
            solution_id=sub.solution_id,
            source=code
        ))
        # 标记提交
        sub_mark.append((tid, sub.solution_id))
    mysql_session.add_all(code_create)
    mysql_session.add_all(code_user_create)  # 什么鬼……为什么hustoj有这么个表？
    mysql_session.commit()
    Submission.mark(submission.id, sub_mark)  # 向提交中传入这组标记。分别是(提交ID，标记数据(测试数据ID,提交submission的ID)).


def _handler(sid):  # 处理某个提交。
    status = Submission.get_status(sid)  # sdustoj上的提交ID -> 提交的内容字典(sdustoj上的测试数据ID,hustoj上的提交ID)
    if status is None:  # 如果字典不存在，也就是这个提交没有被标记处理，那么就离开。
        return

    print_log('Analysing submission %s' % (sid, ))

    test_status = pg_session.query(pg_models.TestDataStatus).filter_by(submission_id=sid).first()
    # 查询在sdustoj上的该提交的提交状态。
    info = test_status.status  # 获得这个提交状态。这个提交状态是一个json结构表的字典表。包含如下信息：
    # status： 提交状态
    # time：耗时
    # memory： 空间

    finished = True
    # 这一部分用来从所有的测试数据中得出最长用时/最大内存/最高优先级的结果状态。
    max_time = -1
    max_memory = -1
    max_status = 4
    for test_data_id, solution_id in status.items():  # 遍历查询所有测试数据的提交的测试数据ID和hustoj提交的ID。
        solution = mysql_session.query(mysql_models.Solution).filter_by(solution_id=solution_id).first()
        # 从hustoj查询这个提交。
        result = solution.result  # 获得提交的结果状态
        info[str(test_data_id)]['status'] = status_map[result]  # 这个map将hustoj的结果编号映射到sdustoj的缩写上去。
        info[str(test_data_id)]['time'] = solution.time
        info[str(test_data_id)]['memory'] = solution.memory
        # 上三行是将正在查看的测试数据的评测结果写到结果信息表中。

        if solution.time > max_time:
            max_time = solution.time
        if solution.memory > max_memory:
            max_memory = solution.memory
        if priority[result] > priority[max_status]:
            max_status = result
        # 上三行获得更高优先级的结果数据。 priority用来规定结果状态的优先级。

        print('\tGot solution %s, result is %s' % (solution_id, result))

        if result in final_status:  # 终止状态代号。
            Submission.remove_status(sid, test_data_id)  # 既然已经终止了就将此条测试数据删掉防止下次还用。
            print('\t\tSolution is judged, removed from mark.')
        else:
            finished = False  # 这个标记用来标记还没有完成全部的测试数据的评测。

    table = pg_models.TestDataStatus.__table__  # 测试数据状态的表本身？
    pg_session.execute(
        table.update().where(table.c.submission_id == sid), {'status': info}
    )  # 看起来这句话的意思是更新该条提交在sdustoj数据库中的信息……
    pg_session.commit()  # 提交更改

    submission = pg_session.query(pg_models.Submission).filter_by(id=sid).first()  # 查询该条提交。
    submission.judge_id = judger_id  # 更新评测机的ID为本机ID。
    if not finished:  # 还没有完成全部测试数据评测。
        Submission.push(sid)  # 将该提交放回分析队列等待下一次分析
        submission.status = status_map[max_status]  # 将sdustoj中的该题目的状态更新。
        print('\tNot finished, pushed.')
    else:
        submission.time = max_time
        submission.memory = max_memory  # 现在可以更新最大用时和最大空间占用了。
        submission.status = status_map[max_status]  # 与if中的一样。
        submission.finished = True  # 标记该提交为已完成。
        print('\tFinished, unmarked.')
    pg_session.commit()
    print('\tSubmission %s updated.' % (sid, ))


def analyse():  # 启动一项任务，从提交解析队列获取下一个待处理的提交，并使用上面的处理函数执行。
    Submission.analyse_mark_submissions(_handler)
