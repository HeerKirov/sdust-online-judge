# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import LargeBinary, BigInteger, String
from sqlalchemy.dialects.postgresql import JSONB

from conf import local_pg_db

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (  # psql的engine
    local_pg_db['user'],
    local_pg_db['password'],
    local_pg_db['host'],
    local_pg_db['database']
), pool_size=20)

_Base = declarative_base()


class HduSubmission(_Base):
    __tablename__ = 'hdusubmission'

    id = Column(BigInteger, primary_key=True)
    run_id = Column(BigInteger, unique=True)
    pid = Column(String)
    time = Column(Integer)
    memory = Column(Integer)
    length = Column(Integer)
    language = Column(String)
    status = Column(String)

    submission_id = Column(BigInteger, unique=True)

    submit_time = Column(DateTime)
    update_time = Column(DateTime)

    finished = Column(Boolean)


class PojSubmission(_Base):
    __tablename__ = 'pojsubmission'

    id = Column(BigInteger, primary_key=True)
    run_id = Column(BigInteger, unique=True)
    pid = Column(String)
    time = Column(Integer)
    memory = Column(Integer)
    length = Column(Integer)
    language = Column(String)
    status = Column(String)

    submission_id = Column(BigInteger, unique=True)

    submit_time = Column(DateTime)
    update_time = Column(DateTime)

    finished = Column(Boolean)
