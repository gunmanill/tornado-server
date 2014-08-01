from baseModel import BaseModel
import re
from hashlib import md5
from config import md5_salt
from config import max_login_try_count
from tornado import gen
import utils
from logModel import LogModel
from promiseModel import PromiseModel

class UserModel(BaseModel):

	r_log = re.compile('^[\w\-\@]{3,20}$')
	r_pass = re.compile('^[\w\-\@\$\%\#\&\!\"\']{8,20}$')
	r_acc = re.compile('^\d+$')
	r_desc = re.compile('[\w]{3}')
	r_id = re.compile('^\d+$')

	user = None
	

	def __new__(self, user):
		
		if not user: 
			return
		self.user = user

		return self

	def __init__(self):
		pass

	

	@staticmethod
	@gen.coroutine
	def getUsers():
		ret = yield UserModel.sql('SELECT * FROM "user" WHERE is_deleted=False')
		
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def login(login, password):

		if UserModel.r_log.match(login) == None or \
		UserModel.r_pass.match(password) == None:
			raise gen.Return(False)



		ret = yield UserModel.sql('SELECT id, password, interface_access, description FROM "user" WHERE login=%s AND is_deleted=FALSE', login.lower())	
		if len(ret) == 0 or \
		ret[0]['password'] != md5(md5_salt + password).hexdigest() or \
		not ret[0]['interface_access']:
			raise gen.Return(False)

		yield LogModel.write('user', ret[0]['description'], 'logged in', None, None)
		raise gen.Return(ret)

	
	def getUserProps(self):
		return self.user

	@staticmethod
	@gen.coroutine
	def addUser(login, 
				password, 
				password2, 
				interface_access = False, 
				description = '', 
				key = '', 
				nodeUserAccessList = [], 
				nodeSudoAccessList = [],
				classUserAccessList = [], 
				classSudoAccessList = []):
		
		if password != password2:
			raise gen.Return('password1 != password2')

		if UserModel.r_log.match(login) == None or \
		UserModel.r_pass.match(password) == None or \
		UserModel.r_desc.match(description) == None or \
		not (interface_access in (True, False)):
			raise gen.Return('description, login or password are wrong')

		ids = []
		ids.extend(nodeUserAccessList)
		ids.extend(nodeSudoAccessList)
		ids.extend(classUserAccessList)
		ids.extend(classSudoAccessList)

		for _id in ids:
			if UserModel.r_id.match(_id) == None:
				raise gen.Return('bad id')

		ret = yield UserModel.sql('INSERT INTO "user" (login, \
														password,\
														interface_access, \
														description, \
														key, \
														node_user_access_list, \
														node_sudo_access_list, \
														class_user_access_list, \
														class_sudo_access_list) VALUES (%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING *', 
														login.lower(), 
														md5_salt + password, 
														interface_access, 
														description,
														key,
														','.join(nodeUserAccessList),
														','.join(nodeSudoAccessList),
														','.join(classUserAccessList),
														','.join(classSudoAccessList))

		yield PromiseModel.createPromise(ret[0]['id'])
		yield LogModel.write('user', description, 'create', None, utils.toDict(ret[0]))

		raise gen.Return(False)

	@staticmethod
	@gen.coroutine
	def getUser(id):
		ret = yield UserModel.sql('SELECT * FROM "user" WHERE id=%s', id)
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def updateUser(	id, 
					login, 
					password, 
					password2, 
					interface_access = False, 
					description = '', 
					key = '',
					nodeUserAccessList = [], 
					nodeSudoAccessList = [],
					classUserAccessList = [], 
					classSudoAccessList = []):

		ids = []
		ids.extend(nodeUserAccessList)
		ids.extend(nodeSudoAccessList)
		ids.extend(classUserAccessList)
		ids.extend(classSudoAccessList)

		for _id in ids:
			if UserModel.r_id.match(_id) == None:
				raise gen.Return('bad id')

		old_val = yield UserModel.getUser(id)

		if password == 'leave old':
			password = old_val[0]['password']
			password2 = password
		else:
			password = md5(md5_salt + password).hexdigest()
			password2 = password


		if password != password2:
			raise gen.Return('password1 != password2')
		elif UserModel.r_id.match(id) == None or \
		(password != old_val[0]['password'] and UserModel.r_pass.match(password) == None) or \
		UserModel.r_log.match(login) == None or \
		UserModel.r_desc.match(description) == None or \
		not (interface_access in (True, False)):
			raise gen.Return('description, password or login are wrong')
		else:
			new_val = yield UserModel.sql('UPDATE "user" SET login=%s, \
													interface_access=%s, \
													description=%s, \
													password=MD5(%s), \
													key=%s,\
													node_user_access_list=%s, \
													node_sudo_access_list=%s, \
													class_user_access_list=%s, \
													class_sudo_access_list=%s \
													WHERE id=%s RETURNING *', 
													login, 
													interface_access, 
													description, 
													md5_salt + password, 
													key,
													','.join(nodeUserAccessList),
													','.join(nodeSudoAccessList),
													','.join(classUserAccessList),
													','.join(classSudoAccessList),
													id)

		yield LogModel.write('user', description, 'edit', utils.toDict(old_val[0]), utils.toDict(new_val[0]))

	@staticmethod
	@gen.coroutine
	def deleteUser(id):
		if UserModel.r_id.match(id) == None:
			raise gen.Return('wrong id')

		old_val = yield UserModel.getUser(id)

		yield UserModel.sql('UPDATE "user" SET is_deleted=True WHERE id=%s', id)
		yield LogModel.write('user', old_val[0]['description'], 'delete', utils.toDict(old_val[0]), None)

	@staticmethod
	@gen.coroutine
	def banIp(ip):
		ret = yield UserModel.setAttempts(ip, max_login_try_count)
		yield LogModel.write('ip', ip, 'ban', None, None)
		raise gen.Return(ret)
	
	@staticmethod
	@gen.coroutine
	def getAttempts(ip):
		
		ret = yield UserModel.sql('SELECT ip, attempts FROM "banned_ip" WHERE ip=%s', utils.ipToInt(ip))
		raise gen.Return(ret)
	
	

	@staticmethod
	@gen.coroutine
	def setAttempts(ip, attempts):
		at =  yield UserModel.getAttempts(ip)
		if at:
			ret = yield UserModel.sql('UPDATE "banned_ip" SET attempts=%s, date=CURRENT_TIMESTAMP WHERE ip=%s', attempts, utils.ipToInt(ip))
		else:
			ret = yield UserModel.sql('INSERT INTO "banned_ip" (ip, ip_str, attempts) VALUES (%s, %s, %s)', utils.ipToInt(ip), ip, attempts)

		raise gen.Return(ret)
	
	@staticmethod
	@gen.coroutine
	def delAttempts(ip):
		ret = yield UserModel.sql('DELETE FROM "banned_ip" WHERE ip=%s', utils.ipToInt(ip))
		raise gen.Return(ret)

	@staticmethod
	@gen.coroutine
	def increaseAttempts(ip):
		ret = yield UserModel.sql('UPDATE "banned_ip" SET attempts=(attempts+1) WHERE ip=%s', utils.ipToInt(ip))
		raise gen.Return(ret)
	