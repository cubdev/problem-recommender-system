from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.schema import Sequence
from sqlalchemy.dialects.mysql import INTEGER, TEXT, TINYTEXT
from db_config import Base

class Problems(Base):
	__tablename__ = 'problems'
	__table_args__ = {
		'mysql_engine' : 'InnoDB',
		'mysql_charset' : 'utf8'
	}

	id = Column(INTEGER(unsigned=True, zerofill=False),
		Sequence('article_aid_seq', start=0, increment=1),primary_key=True)
	url = Column(String(20), nullable=False, unique=True)
	site = Column(TINYTEXT, nullable=False)
	title = Column(TINYTEXT, nullable=False)
	statement = Column(TEXT, nullable=False)
	tags = Column(TEXT, nullable=True)
	date = Column(DateTime, nullable=False)

	def __init__(self, site, url, title, statement, tags, date):
		self.url = url
		self.site = site
		self.title = title
		self.statement = statement
		self.tags = tags
		self.date = date

	def __repr__(self):
		return "%s[url=%s]" % (self.__class__.__name__, self.url)

class Submissions(Base):
	__tablename__ = 'submissions'
	__table_args__ = {
		'mysql_engine' : 'InnoDB',
		'mysql_charset' : 'utf8'
	}

	id = Column(INTEGER(unsigned=True, zerofill=False),
		Sequence('article_aid_seq', start=0, increment=1), primary_key=True)
	url = Column(String(20), ForeignKey(Problems.url), nullable=False)
	user = Column(TINYTEXT, nullable=False)
	lang = Column(TINYTEXT, nullable=False)
	date = Column(DateTime, nullable=False)

	def __init__(self, url, user, lang, date):
		self.url = url
		self.user = user
		self.lang = lang
		self.date = date

	def __repr__(self):
		return "%s[url=%s]" % (self.__class__.__name__, self.url)