from baseModel import BaseModel
import re
from tornado import gen
import tornado
import utils
from psycopg2 import TimestampFromTicks

class LogModel(BaseModel):

	r_time = re.compile('^\d+$')

	@staticmethod
	@gen.coroutine
	def getLogFromTimeStamp(start_timestamp, order = 'time', desc = 'desc'):

		if LogModel.r_time.match(start_timestamp) == None or \
		not (desc in ('desc', 'asc')) or \
		not (order in ('time', 'object_type', 'object', 'action')):
			raise gen.Return([{'time' : 'error', 
								'object_type' : '',
								'object' : '',
								'action' : 'Wrong input params'}])

		end_timestamp = float(int(start_timestamp) + 1000*60*60*24)/1000
		start_timestamp = float(start_timestamp)/1000



		ret = yield LogModel.sql('SELECT cast(extract(epoch from time) as integer) as time, object_type, object, action, old_val, new_val FROM "log" WHERE time>=%s AND time<%s ORDER BY ' + order + ' ' + desc, TimestampFromTicks(start_timestamp), TimestampFromTicks(end_timestamp))

		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def write(obj_type, obj, action, old_val = None, new_val = None):

		if not old_val:
			old_val = {'empty' : 'no data available'}
		if not new_val:
			new_val = {'empty' : 'no data available'}

		for key in old_val.keys():
			old_val[key] = str(old_val[key])
		for key in new_val.keys():
			new_val[key] = str(new_val[key])
		
		yield LogModel.sql('INSERT INTO "log" (object_type, object, action, old_val, new_val) VALUES (%s, %s, %s, %s, %s)', obj_type, obj, action, tornado.escape.json_encode(old_val), tornado.escape.json_encode(new_val))