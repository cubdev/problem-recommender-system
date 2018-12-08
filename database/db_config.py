from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = None
Base = None

def db_init(user, passwd, db_name, ip='localhost'):
	global db_session
	global Base

	engine = create_engine('mysql://%s:%s@%s/%s'
		% (user, passwd, ip, db_name), convert_unicode=True)
	Session = scoped_session(sessionmaker(autocommit=False,
		autoflush=False, bind=engine))
	Base = declarative_base()
	Base.query = Session.query_property()

	# Create tables in not created.
	from models import Problems
	Base.metadata.create_all(bind=engine)

def mysql_user_info():
	'''Need user, passwd and db_name entry
	in ~/.mysql.user file.
	'''
	import os, json
	file = os.getenv('HOME') + '/.mysql.user'
	user, passwd, db_name = (None, None, None)
	if os.path.isfile(file):
		with open(file) as f:
			data = json.load(f)
			user = data['user'] if 'user' in data.keys() else None
			passwd = data['passwd'] if 'passwd' in data.keys() else None
			db_name = data['db_name'] if 'db_name' in data.keys() else None
	return (user, passwd, db_name)

if __name__ == '__main__':
	user, passwd, db_name = mysql_user_info()
	if user is None or passwd is None or db_name is None:
		print "User info is missing. make ~/.mysql.user file."
		exit(1)
	print user, passwd, db_name