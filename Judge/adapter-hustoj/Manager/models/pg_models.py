# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import LargeBinary, BigInteger, String
from sqlalchemy.dialects.postgresql import JSONB

from conf import pg_db

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (  # psql的engine
    pg_db['user'],
    pg_db['password'],
    pg_db['host'],
    pg_db['database']
), pool_size=20)

_Base = declarative_base()  # sqlalchemy 方面的一个base。

# 看起来下面的类都是映射了表结构。似乎是sdustoj的表结构。


class Judge(_Base):
    __tablename__ = 'rest_api_judge'

    id = Column(BigInteger, primary_key=True)
    last_update = Column(DateTime)


class MetaProblem(_Base):
    __tablename__ = 'rest_api_metaproblem'

    id = Column(BigInteger, primary_key=True)
    deleted = Column(Boolean)

    def __repr__(self):
        return '<MetaProblem %s>' % (self.id, )


class Problem(_Base):
    __tablename__ = 'rest_api_problem'

    id = Column(BigInteger, primary_key=True)
    meta_problem_id = Column(BigInteger)
    deleted = Column(Boolean)

    def __repr__(self):
        return '<Problem %s in MetaProblem %s>' % (self.id, self.meta_problem_id)


class SpecialJudge(_Base):
    __tablename__ = 'rest_api_specialjudge'

    id = Column(BigInteger, primary_key=True)
    problem_id = Column(BigInteger)

    code = Column(LargeBinary)
    available = Column(Boolean)
    deleted = Column(Boolean)


class ProblemTestData(_Base):
    __tablename__ = 'rest_api_problemtestdata'

    id = Column(BigInteger, primary_key=True)
    problem_id = Column(BigInteger)
    test_data_id = Column(BigInteger)
    deleted = Column(Boolean)

    def __repr__(self):
        return '<Relation of Problem %s and TestData %s>' % (self.problem_id, self.test_data_id)


class TestData(_Base):
    __tablename__ = 'rest_api_testdata'

    id = Column(BigInteger, primary_key=True)

    test_in = Column(LargeBinary, nullable=True)
    test_out = Column(LargeBinary, nullable=True)
    deleted = Column(Boolean)

    def __repr__(self):
        return '<TestData %s>' % (self.id, )


class Limit(_Base):
    __tablename__ = 'rest_api_limit'

    id = Column(BigInteger, primary_key=True)
    environment_id = Column(BigInteger)
    problem_id = Column(BigInteger)

    time_limit = Column(Integer)
    memory_limit = Column(Integer)
    length_limit = Column(Integer)

    deleted = Column(Boolean)


class Environment(_Base):
    __tablename__ = 'rest_api_environment'

    id = Column(BigInteger, primary_key=True)
    judge_id = Column(String)


class InvalidWord(_Base):
    __tablename__ = 'rest_api_invalidword'

    id = Column(BigInteger, primary_key=True)
    word = Column(String)
    problem_id = Column(BigInteger)


class Submission(_Base):
    __tablename__ = 'rest_api_submission'

    id = Column(BigInteger, primary_key=True)
    problem_id = Column(BigInteger)
    environment_id = Column(BigInteger)

    time = Column(Integer)
    memory = Column(Integer)
    length = Column(Integer)

    status = Column(String)
    finished = Column(Boolean)

    submit_time = Column(DateTime)
    judge_id = Column(BigInteger)

    ip = Column(INET)


class CompileInfo(_Base):
    __tablename__ = 'rest_api_compileinfo'

    submission_id = Column(BigInteger, primary_key=True)
    info = Column(JSONB)


class TestDataStatus(_Base):
    __tablename__ = 'rest_api_testdatastatus'

    submission_id = Column(BigInteger, primary_key=True)
    status = Column(JSONB)


class SubmissionCode(_Base):
    __tablename__ = 'rest_api_submissioncode'

    submission_id = Column(BigInteger, primary_key=True)
    code = Column(JSONB)
