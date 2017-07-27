# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import LargeBinary, BigInteger, Float
from sqlalchemy.dialects.postgresql import INET, JSONB, ARRAY

from config import PG_SETTINGS

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (
    PG_SETTINGS['user'],
    PG_SETTINGS['password'],
    PG_SETTINGS['host'],
    PG_SETTINGS['db']
), pool_size=20)

_Base = declarative_base()


class Problem(_Base):
    __tablename__ = 'rest_api_problem'

    id = Column(BigInteger, primary_key=True)
    description = Column(String)
    sample = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    title = Column(String(128))
    introduction = Column(String(512), nullable=True)
    source = Column(String(256), nullable=True)
    author = Column(String(64), nullable=True)
    is_special_judge = Column(Boolean)
    number_test_data = Column(Integer)
    number_limit = Column(Integer)
    number_category = Column(Integer)
    number_invalid_word = Column(Integer)

    def __repr__(self):
        return '<Problem %s: %s>' % (self.id, self.title)


class Environment(_Base):
    __tablename__ = 'rest_api_environment'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=128))


class Limit(_Base):
    __tablename__ = 'rest_api_limit'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    problem_id = Column(BigInteger)
    environment_id = Column(BigInteger)
    env_name = Column(String(length=128))

    time_limit = Column(Integer, default=-1)
    memory_limit = Column(Integer, default=-1)
    length_limit = Column(Integer, default=-1)


class Category(_Base):
    __tablename__ = 'rest_api_category'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(128))
    introduction = Column(String(512), nullable=True)
    source = Column(String(256), nullable=True)
    author = Column(String(64), nullable=True)
    number_problem = Column(Integer, default=0)


class CategoryProblemRelation(_Base):
    __tablename__ = 'rest_api_categoryproblemrelation'

    id = Column(BigInteger, primary_key=True)
    category_id = Column(BigInteger)
    problem_id = Column(BigInteger)
    directory = Column(ARRAY(String(length=128)))


class Submission(_Base):
    __tablename__ = 'rest_api_submission'

    id = Column(BigInteger, primary_key=True)
    sid = Column(BigInteger, unique=True)
    time = Column(Integer)
    memory = Column(Integer)
    length = Column(Integer)
    status = Column(String(length=4))
    score = Column(Float, nullable=True)
    finished = Column(Boolean)
    update_time = Column(DateTime)


class CompileInfo(_Base):
    __tablename__ = 'rest_api_compileinfo'

    submission_id = Column(BigInteger, primary_key=True)
    info = Column(String)


class TestDataStatus(_Base):
    __tablename__ = 'rest_api_testdatastatus'

    submission_id = Column(BigInteger, primary_key=True)
    status = Column(JSONB)


class SubmissionCode(_Base):
    __tablename__ = 'rest_api_submissioncode'

    submission_id = Column(BigInteger, primary_key=True)
    code = Column(JSONB)
