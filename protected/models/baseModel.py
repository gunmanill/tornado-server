import momoko
from os import _exit as exit
from config import db
from tornado import gen
import psycopg2.extras


class BaseModel(object):
	dbconn = momoko.Pool(dsn = db['dsn'], 
						cursor_factory = psycopg2.extras.DictCursor,
						size = db['size'],
						max_size = db['max_size'])
	
	def __new__():
		exit(1)

	def __init__():
		exit(1)

	@staticmethod
	@gen.coroutine
	def sql(query, *args):
		cursor = yield momoko.Op(BaseModel.dbconn.execute, query, args)
		try:
			ret = cursor.fetchall()
		except:
			ret = True
		finally:
			raise gen.Return(ret)

