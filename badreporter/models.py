from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class BadCase(Base):
    __tablename__ = 'av_badcases'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    description = Column(Text)
    status = Column(String)
    createTime = Column(DateTime)
    updateTime = Column(DateTime)

    def __init__(self, url, description=""):
        self.url = url
        self.description = description

