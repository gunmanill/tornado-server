from baseModel import BaseModel
import re
from tornado import gen
import utils
from logModel import LogModel


class NodeModel(BaseModel):

	r_name = re.compile('^[\w\-]{3,20}$')
	r_ip = re.compile('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$')
	r_id = re.compile('^\d+$')

	@staticmethod
	@gen.coroutine
	def getNodes():
		ret = yield NodeModel.sql('SELECT * from "nodes"')

		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def addNode(name, ip):
		if NodeModel.r_name.match(name) == None or NodeModel.r_ip.match(ip) == None:
			raise gen.Return('Wrong name or ip')

		ret = yield NodeModel.sql('SELECT * from "nodes" WHERE ip=%s OR name=%s', utils.ipToInt(ip), name)
		if ret:
			raise gen.Return('Node with this name or ip already exists')

		yield LogModel.write('node', name, 'create', None, {'name' : name, 'ip' : utils.ipToInt(ip), 'ip_str' : ip})
		yield NodeModel.sql('INSERT INTO "nodes" (name, ip, ip_str) VALUES (%s, %s, %s)', name, utils.ipToInt(ip), ip)
		raise gen.Return(False) #false means no error

	@staticmethod
	@gen.coroutine
	def getNode(id):
		ret = yield NodeModel.sql('SELECT * FROM "nodes" WHERE id=%s', id)
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def updateNode(id, name, ip):
		if NodeModel.r_name.match(name) == None or NodeModel.r_ip.match(ip) == None:
			raise gen.Return('Wrong name or ip')

		ret = yield NodeModel.sql('SELECT * from "nodes" WHERE ip=%s OR name=%s', utils.ipToInt(ip), name)
		if ret:
			raise gen.Return('Node with this name or ip already exists')

		old_val = yield NodeModel.getNode(id)
		
		yield NodeModel.sql('UPDATE "nodes" SET name=%s, ip=%s, ip_str=%s WHERE id=%s', name, utils.ipToInt(ip), ip, id)
		yield LogModel.write('node', name, 'edit', utils.toDict(old_val[0]), {'name' : name, 'ip' : utils.ipToInt(ip), 'ip_str' : ip})
		raise gen.Return(False)

	@staticmethod
	@gen.coroutine
	def deleteNode(id):
		ret = yield NodeModel.sql('SELECT * FROM "classes" WHERE list ~ %s', r'(?:^|,)' + id + r'(?:$|,)')
		if ret:
			raise gen.Return('This node is a part of ' + ret[0]['name'] + ' class, u need first remove it from there')

		reg = r'(?:^|,)' + id + r'(?:$|,)'
		ret = yield NodeModel.sql('SELECT description  FROM "user" WHERE node_user_access_list ~ %s OR node_sudo_access_list ~ %s', reg, reg)
		if ret:
			raise gen.Return('This node is in access list of ' + ret[0]['description'] + ' user, u need first remove it from there')	

		old_val = yield NodeModel.getNode(id)
		yield NodeModel.sql('DELETE FROM "nodes" WHERE id=%s', id)
		yield LogModel.write('node', old_val[0]['name'], 'delete', utils.toDict(old_val[0]), None)
		raise gen.Return(False)

	@staticmethod
	@gen.coroutine
	def getClasses():
		ret = yield NodeModel.sql('SELECT * FROM "classes"')
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def getClass(id):
		ret = yield NodeModel.sql('SELECT * FROM "classes" WHERE id=%s', id)
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def addClass(name, list = None):
		if not list:
			list = []
		if NodeModel.r_name.match(name) == None:
			raise gen.Return('Wrong name')
		for id in list:
			if NodeModel.r_id.match(id) == None:
				raise gen.Return('Wrong id of list')
		list = ','.join(list)

		ret = yield NodeModel.sql('SELECT * from "classes" WHERE name=%s',name)
		if ret:
			raise gen.Return('Class with this name already exists')

		yield NodeModel.sql('INSERT INTO "classes" (name, list) VALUES (%s, %s)', name, list)
		yield LogModel.write('group', name, 'create', None, {'name' : name, 'list' : list})
		raise gen.Return(False)

	@staticmethod
	@gen.coroutine
	def updateClass(class_id, name, list = None):
		if not list:
			list = []
		if NodeModel.r_name.match(name) == None or NodeModel.r_id.match(class_id) == None:
			raise gen.Return('Wrong name')
		for id in list:
			if NodeModel.r_id.match(id) == None:
				raise gen.Return('Wrong id')

		ret = yield NodeModel.sql('SELECT * from "classes" WHERE name=%s AND id!=%s', name, class_id)
		if ret:
			raise gen.Return('Class with this name already exists')

		list = ','.join(list)

		old_val = yield NodeModel.getClass(class_id)
		
		yield NodeModel.sql('UPDATE "classes" SET name=%s, list=%s WHERE id=%s', name, list, class_id)
		yield LogModel.write('group', name, 'edit', utils.toDict(old_val[0]), {'name' : name, 'list' : list})
		raise gen.Return(False)

	@staticmethod
	@gen.coroutine
	def deleteClass(id):
		reg = r'(?:^|,)' + id + r'(?:$|,)'
		ret = yield NodeModel.sql('SELECT description  FROM "user" WHERE class_user_access_list ~ %s OR class_sudo_access_list ~ %s', reg, reg)
		if ret:
			raise gen.Return('This class is in access list of ' + ret[0]['description'] + ' user, u need first remove it from there')	

		old_val = yield NodeModel.getClass(id)
		print id

		yield NodeModel.sql('DELETE FROM "classes" WHERE id=%s', id)
		yield LogModel.write('group', old_val[0]['name'], 'delete', utils.toDict(old_val[0]), None)
