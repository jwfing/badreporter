from datetime import datetime, date, time
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
        self.createTime = datetime.today()
        self.updateTime = datetime.today()
        self.status = 'A'

    def __str__(self):
        urlString = ('"' + self.url + '"') if self.url else "\"\""
        createString = ('"' + str(self.createTime) + '"') if (self.createTime) else "\"\""
        updateString = ('"' + str(self.updateTime) + '"') if (self.updateTime) else "\"\""
        idString = ('"' + str(self.id) + '"') if (self.id) else "\"\""
        statusString = ('"' + str(self.status) + '"') if self.status else "\"\""
        descString = ('"' + str(self.description) + '"') if self.description else "\"\""
        return "{\"id\":" + idString + ", \"url\":" + urlString + ", \"description\":" + descString \
                + ", \"createTime\":" +  createString \
                + ", \"updateTime\":" + updateString \
                + ", \"status\":"+ statusString + "}"

def createCase(url, desc):
    case = BadCase(url, desc)
    DBSession.add(case)
    pass

def listAllCases(offset, limit, status):
    query = None
    if status == 'A' or status == 'C':
        query = DBSession.query(BadCase).filter(BadCase.status==status)
    else:
        query = DBSession.query(BadCase)
    return query.order_by("updateTime desc")[int(offset):int(limit) + int(offset)]

def getCaseById(id):
    return DBSession.query(BadCase).filter(BadCase.id==id).first()

def closeCase(id):
    case = getCaseById(id)
    if case:
        case.status = 'C'
        DBSession.save(case)

def reopenCase(id):
    case = getCaseById(id)
    if case:
        case.status = 'A'
        DBSession.save(case)

