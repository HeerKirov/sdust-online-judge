# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, TIMESTAMP, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text

from conf import mysql_db

engine = create_engine('mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (  # mysql的引擎
    mysql_db['user'],
    mysql_db['password'],
    mysql_db['host'],
    mysql_db['database']
), pool_size=20)

_Base = declarative_base()  # 一个基？


class CompileInfo(_Base):
    __tablename__ = 'compileinfo'

    solution_id = Column(Integer, primary_key=True)
    error = Column(Text)

    def __repr__(self):
        return '<CompileInfo %s>' % (self.solution_id, )

# 这一部分表似乎是在映射hustoj的表结构。


class Problem(_Base):
    __tablename__ = 'problem'
    problem_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    input = Column(Text)
    output = Column(Text)
    sample_input = Column(Text)
    sample_output = Column(Text)
    spj = Column(String)
    hint = Column(Text)
    source = Column(String)
    time_limit = Column(Integer)
    memory_limit = Column(Integer)


class Solution(_Base):
    __tablename__ = 'solution'
    solution_id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer)
    user_id = Column(String)
    time = Column(Integer, default=0)
    memory = Column(Integer, default=0)
    result = Column(Integer, default=0)
    language = Column(Integer, default=0)
    ip = Column(String)
    code_length = Column(Integer)
    in_date = Column(DateTime)
    judgetime = Column(TIMESTAMP, nullable=True)
    judger = Column(String)


class SourceCode(_Base):
    __tablename__ = 'source_code'
    solution_id = Column(Integer, primary_key=True)
    source = Column(Text)


class SourceCodeUser(_Base):
    __tablename__ = 'source_code_user'
    solution_id = Column(Integer, primary_key=True)
    source = Column(Text)


class User(_Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)

    def __repr__(self):
        return '<User %s: %s>' % (self.user_id, self.password)
